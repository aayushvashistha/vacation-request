"""
URL configuration for vacation_request_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vacation.views import (WorkerRequestListView, AllRequestsOverviewView, IndividualRequestsOverviewView, OverlappingRequestsView, WorkerRemainingVacationDaysView, ProcessRequestView)

urlpatterns = [
    path('admin/', admin.site.urls),
    # GET API to see individual emp request
    path('worker/requests/<int:emp_id>/', WorkerRequestListView.as_view(), name='worker-request-list'),

    #POST API to create new vacation request
    path('worker/requests/create/', WorkerRequestListView.as_view(), name='worker-request-list'),
    
    # GET API to see the number of remaining days left
    path('worker/requests/remaining-days/<int:emp_id>', WorkerRemainingVacationDaysView.as_view(), name='worker-remaining-days'),

    # GET API to see an overview of individual employees request
    path('manager/requests/overview/<int:emp_id>/', IndividualRequestsOverviewView.as_view(), name='manager-all-requests-overview'),

    #GET API to see list of all requests
    path('manager/requests/overview/', AllRequestsOverviewView.as_view(), name='manager-all-requests-overview'),

    # GET API to see overlapping requests
    path('manager/requests/overlapping/', OverlappingRequestsView.as_view(), name='manager-overlapping-requests'),

    # PATCH API to approve or reject individual request
    path('manager/requests/<uuid:pk>/process/', ProcessRequestView.as_view(), name='manager-process-request'),

]
