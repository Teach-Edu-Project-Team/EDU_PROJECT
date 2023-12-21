from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied



def unauthenticated_user(view_class):
    class WrapperClass(view_class):
        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect('home')
            return super().dispatch(request, *args, **kwargs)

    return WrapperClass

def unauthenticated_profile(view_class):
    class WrapperClass(view_class):
        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect('home')
            return super().dispatch(request, *args, **kwargs)

    return WrapperClass

class AllowedUsersMixin:
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if any(role in self.allowed_roles for role in request.user.groups.values_list('name', flat=True)):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('user_home')  

def allowed_users(*allowed_roles):
    class DecoratorClass:
        def __call__(self, view_class):
            class WrappedView(AllowedUsersMixin, view_class):
                pass
            WrappedView.allowed_roles = allowed_roles
            return WrappedView
    return DecoratorClass()

class AdminOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated and request.user.groups.filter(name='Admin').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
           
            return redirect('user_home')

def admin_only(view_class):
    class WrappedView(AdminOnlyMixin, view_class):
        pass

    return WrappedView


class UsersOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated and request.user.groups.filter(name='users').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            # Redirect to user_page if the user is not an admin
            return redirect('home')

def users_only(view_class):
    class WrappedView(UsersOnlyMixin, view_class):
        pass

    return WrappedView

class PreventBackMixin:
    def dispatch(self, request, *args, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        allowed_referer = self.get_allowed_referer()
        
        if referer != allowed_referer:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_allowed_referer(self):
        # Override this method in your views to return the allowed referer
        # Example: return reverse('some_view_name')
        return None

def prevent_back(view_class):
    class WrappedView(PreventBackMixin, view_class):
        pass

    return WrappedView