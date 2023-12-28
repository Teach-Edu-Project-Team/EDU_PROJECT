from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome'),
    path('home/', HomeView.as_view(), name='home'),
    
    path('pdf/<int:pk_test>/', PDFView.as_view(), name='staff_pdf_view'),
    
    
    path('user/', ProfilepageView.as_view(), name='user_page'),
    path('admin_view_profile/', ProfileAdminpageView.as_view(), name='admin_page'),
    
    path('AdminDisplay/', AdminView.as_view(), name='Adminpage'),
    path('staff/<int:pk_test>/', StaffDetailView.as_view(), name='staff_detail'),
    path('update/<int:pk>/', PersonalUpdateView.as_view(), name='update_staff'),
    path('delete/<int:pk>/', PersonalDeleteView.as_view(), name='delete'),
    path('create_user/',PersonalWizardView.as_view(),name='create_staff'),
    path('admin_user/',PersonalAdminWizardView.as_view(),name='admin_profile'),
    
    
    path('ViewStaff/',StaffView.as_view(),name='view_staff'),
    
    path('complete_profile/', CompleteProfileView.as_view(), name='cprofile'),
    path('incomplete_profile/', IncompleteProfileView.as_view(), name='iprofile'),
    
    path('view-existing-profile/', ViewExistingProfile.as_view(), name='view_profile'),
    path('view-existing-profile(admin)/', ViewExistingAdminProfile.as_view(), name='view_profile(admin)'),
    
    path('updateprofile/', UpdateProfileView.as_view(), name='update_profile'),
    path('profilenotcreated/', ProfileNotCreatedView.as_view(), name='profile_not_created'),
    path('profilenotcreated(admin)/', ProfileNotCreatedAdminView.as_view(), name='profile_not_created(admin)'),
    
    
    
    
    path('Account Settings/', AccountSettingsView.as_view(), name='account_settings'),
    path('Account_Settings_admin/', AccountSettingsAdminView.as_view(), name='account_settings_admin'),
    
    
    path('userprofile/', PersonalUserWizardView.as_view(), name='user_profile'),
    
    path('register/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_home/', UserhomepageView.as_view(), name='user_home'),
     
    
    
    path('settings/', AccountSettingsView.as_view(), name='account_settings'),
    
  
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    
    
    
    
       
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)