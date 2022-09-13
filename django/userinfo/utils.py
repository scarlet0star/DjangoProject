from django.shortcuts import redirect
from .models import User

def login_required(func):
    def wrapper(request,*arg,**kwargs):
        login_session = request.session.get('login_session',' ')
        
        if login_session == '':
            return redirect('user/login/')
        
        return func(request,*arg,**kwargs)
    return wrapper