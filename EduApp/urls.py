from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome'),
    path('home/', HomeView.as_view(), name='home'),
    
    path('user/', ProfilepageView.as_view(), name='user_page'),
    path('AdminDisplay/', AdminView.as_view(), name='Adminpage'),
    path('staff/<int:pk_test>/', StaffDetailView.as_view(), name='staff_detail'),
    path('update/<int:pk>/', PersonalUpdateView.as_view(), name='update_staff'),
    path('delete/<int:pk>/', PersonalDeleteView.as_view(), name='delete'),
    path('create_user/',PersonalWizardView.as_view(),name='create_staff'),
    
    path('ViewStaff/',StaffView.as_view(),name='view_staff'),
    
    path('complete_profile/', CompleteProfileView.as_view(), name='cprofile'),
    path('incomplete_profile/', IncompleteProfileView.as_view(), name='iprofile'),
    path('view-existing-profile/', ViewExistingProfile.as_view(), name='view_profile'),
    path('updateprofile/', UpdateProfileView.as_view(), name='update_profile'),
    path('profilenotcreated/', ProfileNotCreatedView.as_view(), name='profile_not_created'),
    
    
    path('Account Settings/', AccountSettingsView.as_view(), name='account_settings'),
    path('userprofile/', PersonalUserWizardView.as_view(), name='user_profile'),
    
    path('register/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_home/', UserhomepageView.as_view(), name='user_home'),
     
    
    
    path('settings/', AccountSettingsView.as_view(), name='account_settings')
    
    
       
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)