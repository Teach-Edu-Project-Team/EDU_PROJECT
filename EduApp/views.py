from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth. models import Group

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from formtools.wizard.views import SessionWizardView
from .filters import *
from .forms import *
from .models import *
from .decorators import *



class WelcomeView(View):
    template_name = 'welcome.html'

    def get(self, request, *args, **kwargs):
        if not request.session.get('visited_before', False):
            request.session['visited_before'] = True
            return render(request, self.template_name, {'first_visit': True})
        else:
            return render(request, self.template_name, {'first_visit': False})

class ViewExistingProfile(TemplateView):
    template_name = 'viewprofile.html'
    
class ViewExistingAdminProfile(TemplateView):
    template_name = 'admin/view_profile(admin).html'
    
@unauthenticated_user
class RegisterView(CreateView):
    form_class = CreateUserForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        user = self.object

        # Assign user to the 'users' group
        group, created = Group.objects.get_or_create(name='users')
        self.object.groups.add(group)

        messages.success(self.request, 'Account was created for ' + username)
        return response
    
@unauthenticated_user  
class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        user = authenticate(request=self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('home')
        else:
            messages.info(self.request, "Username or Password is incorrect") 

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
class LogoutView(View):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
       
        logout(request)
        return render(request, self.template_name)
    
    
@method_decorator(login_required(login_url='login'), name='dispatch')        
class AccountSettingsView(View):
    template_name = 'account_settings.html'
    profile_pic_form_class = ProfilePicForm
    success_url = reverse_lazy('account_settings')

    def dispatch(self, request, *args, **kwargs):
        # Check if the user already has a profile
        existing_profile = Personal.objects.filter(user=request.user).first()

        if not existing_profile:
            return render(request, 'profilenotcreated.html')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        personal_instance = Personal.objects.get(user=request.user)
        profile_pic_form = self.profile_pic_form_class(instance=personal_instance)

        return render(request, self.template_name, {
            'profile_pic_form': profile_pic_form,
        })

    def post(self, request, *args, **kwargs):
        personal_instance = Personal.objects.get(user=request.user)
        profile_pic_form = self.profile_pic_form_class(request.POST, request.FILES, instance=personal_instance)

        if profile_pic_form.is_valid():
            profile_pic_form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'profile_pic_form': profile_pic_form,
        })
        
class AccountSettingsAdminView(View):
    template_name = 'admin/account_settings_admin.html'
    profile_pic_form_class = ProfilePicForm
    success_url = reverse_lazy('account_settings_admin')

    def get_object_or_404(self):
        return get_object_or_404(Personal, user=self.request.user)

    def get(self, request, *args, **kwargs):
        personal_instance = self.get_object_or_404()
        profile_pic_form = self.profile_pic_form_class(instance=personal_instance)
        return render(request, self.template_name, {'profile_pic_form': profile_pic_form})

    def post(self, request, *args, **kwargs):
        personal_instance = self.get_object_or_404()
        profile_pic_form = self.profile_pic_form_class(request.POST, request.FILES, instance=personal_instance)

        if profile_pic_form.is_valid():
            profile_pic_form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {'profile_pic_form': profile_pic_form})

@admin_only
class HomeView(TemplateView):
    template_name = 'home.html'
    
#@method_decorator(login_required(login_url='login'), name='dispatch')    
#@users_only
#class UserpageView(TemplateView):
    #template_name = 'user.html'
    
@method_decorator(login_required(login_url='login'), name='dispatch')    
@users_only 
class ProfilepageView(DetailView):
    model = Personal
    template_name = 'user.html'
    context_object_name = 'user_profile'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                personal_instance = Personal.objects.get(user=self.request.user)
                return super().get(request, *args, **kwargs)
            except Personal.DoesNotExist:
                return render(request, 'profilenotcreated.html')
        else:
            return render(request, 'profilenotcreated.html')

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            try:
                personal_instance = Personal.objects.get(user=self.request.user)
                return personal_instance
            except Personal.DoesNotExist:
                return None
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['work_info'] = Work.objects.filter(personal=self.object).first()
            context['nominal_data'] = Nominal.objects.filter(personal=self.object).first()
        return context
    
@allowed_users('Admin')   
class ProfileAdminpageView(DetailView):
    model = Personal
    template_name = 'admin/admin.html'
    context_object_name = 'admin_profile'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                personal_instance = Personal.objects.get(user=self.request.user)
                return super().get(request, *args, **kwargs)
            except Personal.DoesNotExist:
                return render(request, 'profilenotcreated(admin).html')
        else:
            return render(request, 'profilenotcreated(admin).html')

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            try:
                personal_instance = Personal.objects.get(user=self.request.user)
                return personal_instance
            except Personal.DoesNotExist:
                return None
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['work_info'] = Work.objects.filter(personal=self.object).first()
            context['nominal_data'] = Nominal.objects.filter(personal=self.object).first()
        return context
    
class ProfileNotCreatedView(View):
    template_name = 'profilenotcreated.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class ProfileNotCreatedAdminView(View):
    template_name = 'profilenotcreated(admin).html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    
@method_decorator(login_required(login_url='login'), name='dispatch')    
class UpdateProfileView(View):
    template_name = 'updateprofile.html'
    personal_form_class = PersonalForm
    work_form_class = WorkForm
    nominal_form_class = NominalForm
    success_url = reverse_lazy('user_page')

    

    def get(self, request, *args, **kwargs):
        personal_instance = Personal.objects.get(user=request.user)
        work_instance = Work.objects.get(personal=personal_instance)
        nominal_instance = Nominal.objects.get(personal=personal_instance)

        personal_form = self.personal_form_class(instance=personal_instance)
        work_form = self.work_form_class(instance=work_instance)
        nominal_form = self.nominal_form_class(instance=nominal_instance)

        user_nav_template = self.get_user_nav_template(request)

        return render(request, self.template_name, {
            'user_nav_template': user_nav_template,
            'personal_form': personal_form,
            'work_form': work_form,
            'nominal_form': nominal_form,
        })

    
    def post(self, request, *args, **kwargs):
        # Get the current user's Personal instance
        personal_instance = Personal.objects.get(user=request.user)
        work_instance = Work.objects.get(personal=personal_instance)
        nominal_instance = Nominal.objects.get(personal=personal_instance)

        personal_form = self.personal_form_class(request.POST, instance=personal_instance)
        work_form = self.work_form_class(request.POST, instance=work_instance)
        nominal_form = self.nominal_form_class(request.POST, instance=nominal_instance)

        if personal_form.is_valid() and work_form.is_valid() and nominal_form.is_valid():
            personal_form.save()
            work_form.save()
            nominal_form.save()

            # Dynamically set the success_url based on user status
            if request.user.is_staff:
                self.success_url = reverse_lazy('admin_page')
            else:
                self.success_url = reverse_lazy('user_page')

            return redirect(self.success_url)

        user_nav_template = self.get_user_nav_template(request)

        return render(request, self.template_name, {
            'user_nav_template': user_nav_template,
            'personal_form': personal_form,
            'work_form': work_form,
            'nominal_form': nominal_form,
        })

        
        
@method_decorator(login_required(login_url='login'), name='dispatch') 
@users_only
class CompleteProfileView(TemplateView):
    template_name = 'userhomepage_complete.html'
    
@method_decorator(login_required(login_url='login'), name='dispatch') 
@users_only   
class IncompleteProfileView(TemplateView):
    template_name = 'userhomepage_incomplete.html'
    
    
@method_decorator(login_required(login_url='login'), name='dispatch') 
@users_only
class UserhomepageView(TemplateView):
    template_name = 'userhomepage.html'        

    

    

@method_decorator(login_required(login_url='login'), name='dispatch')
@allowed_users('Admin')
class StaffView(TemplateView):
    template_name = 'ViewStaff.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        personals = Personal.objects.all()
        myFilter = PersonalFilter(self.request.GET, queryset=personals)
        filtered_personals = myFilter.qs

        total_males = filtered_personals.filter(gender='Male').count()
        total_females = filtered_personals.filter(gender='Female').count()

        context['total_males'] = total_males
        context['total_females'] = total_females
        context['personals'] = filtered_personals
        context['myFilter'] = myFilter

        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
@allowed_users('Admin')
class AdminView(TemplateView):
    template_name = 'AdminDisplay.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        personals = Personal.objects.all()
        myFilter = PersonalFilter(self.request.GET, queryset=personals)
        filtered_personals = myFilter.qs

        total_males = filtered_personals.filter(gender='Male').count()
        total_females = filtered_personals.filter(gender='Female').count()

        context['total_males'] = total_males
        context['total_females'] = total_females
        context['personals'] = filtered_personals
        context['myFilter'] = myFilter

        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
@allowed_users('Admin')  
class PersonalWizardView(SessionWizardView):
    form_list = [PersonalForm, WorkForm, NominalForm]
    file_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
    template_name = 'admin/create(admin).html'
    
    
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        section_names = {
            '0': 'Personal Information Section',
            '1': 'Work Information Section',
            '2': 'Nominal Information Section',
        }
        context['section_name'] = section_names[self.steps.current]
        return context

    def done(self, form_list, **kwargs):
        work_form = form_list[1]
        personal = form_list[0].save()
        work = work_form.save(commit=False)
        work.personal = personal
        work.save()

        nominal = form_list[-1].save(commit=False)
        nominal.personal = personal
        nominal.save()

        
        return HttpResponseRedirect(reverse('view_staff'))
    
@method_decorator(login_required(login_url='login'), name='dispatch')
@allowed_users('Admin')  
class PersonalAdminWizardView(SessionWizardView):
    form_list = [PersonalForm, WorkForm, NominalForm]
    file_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
    template_name = 'admin/create(admin).html'
    
    def dispatch(self, request, *args, **kwargs):
        # Check if the user already has a profile
        existing_profile = Personal.objects.filter(user=request.user).first()
        
        if existing_profile:
            # Redirect to view existing profile
            return HttpResponseRedirect (reverse('view_profile(admin)'))
            
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        section_names = {
            '0': 'Personal Information Section',
            '1': 'Work Information Section',
            '2': 'Nominal Information Section',
        }
        context['section_name'] = section_names[self.steps.current]
        return context

    def done(self, form_list, **kwargs):
        work_form = form_list[1]
        personal = form_list[0].save(commit=False)

        # Associate the user with the profile (for admin, assuming admin is the request user)
        personal.user = self.request.user
        personal.save()

        work = work_form.save(commit=False)
        work.personal = personal
        work.save()

        nominal = form_list[-1].save(commit=False)
        nominal.personal = personal
        nominal.save()

        return HttpResponseRedirect(reverse('admin_page'))
    
@method_decorator(login_required(login_url='login'), name='dispatch')
@users_only
class PersonalUserWizardView(SessionWizardView):
    form_list = [PersonalForm, WorkForm, NominalForm]
    file_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
    template_name = 'create.html'

    def dispatch(self, request, *args, **kwargs):
        # Check if the user already has a profile
        existing_profile = Personal.objects.filter(user=request.user).first()
        
        if existing_profile:
            # Redirect to view existing profile
            return HttpResponseRedirect (reverse('view_profile'))
            
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        section_names = {
            '0': 'Personal Information Section',
            '1': 'Work Information Section',
            '2': 'Nominal Information Section',
        }
        context['section_name'] = section_names[self.steps.current]
        return context

    def done(self, form_list, **kwargs):
        work_form = form_list[1]
        personal = form_list[0].save(commit=False)
        personal.user = self.request.user  # Associate the user with the profile
        personal.save()

        work = work_form.save(commit=False)
        work.personal = personal
        work.save()

        nominal = form_list[-1].save(commit=False)
        nominal.personal = personal
        nominal.save()

        return HttpResponseRedirect(reverse('user_page'))

        
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class StaffDetailView(DetailView):
    model = Personal
    template_name = 'staff.html'
    context_object_name = 'staff'
    pk_url_kwarg = 'pk_test'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the related Work instance for the current Personal object using id
        try:
            work_instance = Work.objects.get(personal_id=self.object.id)
        except Work.DoesNotExist:
            work_instance = None

        # Add the work_instance to the context
        context['work_instance'] = work_instance

        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class PersonalUpdateView(UpdateView):
    model = Personal
    form_class = PersonalForm
    template_name = 'update.html'
    success_url = reverse_lazy('view_staff')
    pk_url_kwarg = 'pk'  # Specify the name of the URL parameter for the primary key

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the primary key from the URL parameters
        user_id = self.kwargs.get(self.pk_url_kwarg)

        work_instance = get_object_or_404(Work, personal_id=user_id)
        nominal_instance = get_object_or_404(Nominal, personal_id=user_id)

        work_form = WorkForm(instance=work_instance, prefix='workform')
        nominal_form = NominalForm(instance=nominal_instance, prefix='nominalform')

        context.update({
            'workform': work_form,
            'nominalform': nominal_form,
        })
        return context

    def form_valid(self, form):
        # Save the main form
        response = super().form_valid(form)

        # Update the related instances with the form data
        work_instance = get_object_or_404(Work, personal=self.object)
        work_form = WorkForm(self.request.POST, instance=work_instance, prefix='workform')

        nominal_instance = get_object_or_404(Nominal, personal=self.object)
        nominal_form = NominalForm(self.request.POST, instance=nominal_instance, prefix='nominalform')

        if work_form.is_valid() and nominal_form.is_valid():
            work_form.save()
            nominal_form.save()

        return response
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class PersonalDeleteView(DeleteView):
    model = Personal
    template_name = 'delete.html'  
    success_url = reverse_lazy('view_staff')
    pk_url_kwarg = 'pk'  




















