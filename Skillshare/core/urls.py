from django.urls import path,include
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path('',views.core_page,name='corepage'),
    path('settings/',views.settings,name='settings'),
    path('login/',LoginView.as_view(template_name ='registration/login.html'), name='login'),
    path('register/', views.SignUp_view, name='register'),
    path('profilepage/', views.profile_view, name='userprofile'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.profile_edit, name='profile_edit'),
    path('change-password/', views.custom_change_password, name='password_change'),
    path('message/', views.select_user_to_chat,name='chat_select'),
    path('message/<int:user_id>/', views.send_message,name='send'),
    path('search/',views.search_profile,name='search_profile'),
    # email conformation code 
    path('activate/<uid64>/<token>/', views.activate_account,name='activate'),
    path('inspect/<int:user_id>/', views.inspect_view, name='inspect_user'),

    path('profile/<str:username>/', views.userrating, name='profilerate'),


]
