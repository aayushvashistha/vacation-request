from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from datetime import datetime, date
from django.db.models import Q
from rest_framework import generics
from vacation.models import Request
from vacation.serializers import RequestSerializer
from django.utils import timezone
from django.core.exceptions import ValidationError


class WorkerRequestListView(generics.ListCreateAPIView):
    serializer_class = RequestSerializer
    
    def get_queryset(self, *args, **kwargs):
        worker_requests = Request.objects.all()

        # API allows to see worker's requests based on emp_id
        emp_id = self.kwargs['emp_id']
        status = self.request.query_params.get('status', None)
        worker_requests_emp = worker_requests.filter(emp_id=emp_id)
        try:
            # API allows to see worker's requests based on filter by status
            if status:
                worker_requests = worker_requests.filter(status=status, emp_id=emp_id)
            else:
                raise ValidationError({'error': "Please enter employee id and status"})
            return worker_requests
        except:
            return worker_requests_emp
        
    def get_remaining_vacation_days(self, request):

       # Calculate the total number of days taken by the worker in the current year

        start_date = datetime.strptime(self.request.data['vacation_start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(self.request.data['vacation_end_date'], "%Y-%m-%d")
        total_days_taken =  (end_date - start_date).days

        # Calculate the remaining vacation days for the worker in the current year
        remaining_days = 30 - total_days_taken

        return remaining_days
    
    def perform_create(self, serializer):
        worker_requests = Request.objects.all()

        # Method to save vacation request in db
        remaining_days = self.get_remaining_vacation_days(worker_requests)

        if remaining_days <= 0:
           raise ValidationError ('You have reached the maximum limit of vacation requests for this year.')
        serializer.save()


class WorkerRemainingVacationDaysView(generics.RetrieveAPIView):

    # BONUS --> Count number of vacation days left
    def retrieve(self, *args, **kwargs):
        current_year = timezone.now().year
        emp_id = self.kwargs['emp_id']
        requests_count = Request.objects.filter(created_at__year=current_year, emp_id=emp_id).count()
        remaining_days = 30 - requests_count  # 30 vacation days per year
        return Response({'remaining_days': remaining_days})
    

class IndividualRequestsOverviewView(generics.ListCreateAPIView):
    serializer_class = RequestSerializer

    def get_queryset(self, *args, **kwargs):
        manager_requests_overview = Request.objects.all()

        # overview of each individual request
        emp_id = self.kwargs['emp_id']
        if emp_id is not None:
            manager_requests_overview = manager_requests_overview.filter(emp_id=emp_id)
        return manager_requests_overview
        

class AllRequestsOverviewView(generics.ListCreateAPIView):
    serializer_class = RequestSerializer

    def get_queryset(self, *args, **kwargs):
        manager_requests_overview = Request.objects.all()

        # BONUS --> Overview of all requests with filter by status
        status = self.request.query_params.get('status', None)
        if status is not None:
            manager_requests_overview = manager_requests_overview.filter(status=status)
        return manager_requests_overview
    

class OverlappingRequestsView(generics.ListAPIView):
    serializer_class = RequestSerializer

    # Method for overlapping request with start and end date in query params
    def get_queryset(self):
        overlapping_requests = Request.objects.filter(
            Q(status='approved') | Q(status='pending')
        ).filter(
            Q(vacation_start_date=self.request.query_params.get('start_date')) & Q(vacation_end_date=self.request.query_params.get('end_date'))
        )
        return overlapping_requests
    

class ProcessRequestView(generics.UpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    #BONUS --> Method to update status of request
    def patch(self, request, *args, **kwargs):
        request_id = self.kwargs['pk']
        try:
            request_instance = Request.objects.get(pk=request_id)
        except Request.DoesNotExist:
            return Response({'error': 'Request not found'}, status=404)

        # Check if the manager is processing a request that belongs to them
        if request_instance.resolved_by != "Manager":
            return Response({'error': 'You are not authorized to process this request'}, status=403)

        request_data = request.data
        request_instance.status = request_data.get('status', request_instance.status)
        request_instance.save()
        
        return Response({'message': 'Request processed successfully'})