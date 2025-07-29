from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='connectpage'),
    path('users/', views.user_list, name='user_list'),
    path('send_request/<int:user_id>/', views.send_request, name='send_request'),
    path('received_requests/', views.received_requests, name='received_requests'),
    path('handle_request/<int:connection_id>/<str:action>/', views.handle_request, name='handle_request'),
]
