from django.urls import path
from .views import *

from .views import (
    login_view,
    register_view,
    logout_view,
    dashboard_admin,
    dashboard_user
)

urlpatterns = [

    path('', login_view, name='login'),

    path(
        'register/',
        register_view,
        name='register'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    path(
        'dashboard-admin/',
        dashboard_admin,
        name='dashboard_admin'
    ),

    path(
        'dashboard-user/',
        dashboard_user,
        name='dashboard_user'
    ),

]