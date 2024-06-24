from django.http import HttpResponse
from django.shortcuts import redirect

# create decorator to stop a user from viewing the login and registration page especially if they are already logged in

def unauthenticated_user(view_func):
    # then an inner function
    def wrapper_func(request, *args, **kwargs):
        #then we shall add some conditionals that should be executed in the wrapper function first before our view function is called
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_func
# to test if our wrapper function is working we use the printcode -> print('working:', allowed_roles)

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user')
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_func