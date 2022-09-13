from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib import messages

from .models import User
from .forms import *
from board.models import *
from django.views.generic import DetailView, ListView, UpdateView,CreateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

def userView(request):
    return render(request,'userinfo/user.html')

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'userinfo/login.html'
    
    def post(self,request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username = username, password = password)

        if user is not None and user.is_active:
            login(request,user)
            messages.success(request,f"환영합니다. {username}, 성공적으로 로그인 되었습니다.")
            return redirect("board:home")
        else:
            messages.error(request,"아이디와 비밀번호가 일치하지 않거나 존재하지 않습니다.")
            return redirect("user:login")
        

def logoutView(request):
    logout(request)
    messages.success(request,"성공적으로 로그아웃 되었습니다.")
    return redirect("user:login")

class UserSignUpView(SuccessMessageMixin,CreateView):
    model = User
    form_class = SignUserForm
    template_name = 'userinfo/signup.html'
    success_url= reverse_lazy('user:login')
    success_message = "계정이 성공적으로 생성되었습니다. 로그인 페이지로 이동합니다."

class UserUpdateInfo(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UpdateForm
    success_url = reverse_lazy('user:user')
    template_name = 'userinfo/update.html'
    context_object_name = "theUser"

    def form_valid(self,form):
        messages.success(self.request,"정보가 성공적으로 변경되었습니다.")
        return super().form_valid(form)
     
    def get_object(self):
        return get_object_or_404(User,username=self.kwargs["username"])

class UserUpdatePW(PasswordChangeView):
    template_name = 'userinfo/updatePW.html'
    form_class = UpdatePWForm
    success_url = reverse_lazy("user:user")
    
    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request,form.user)
        messages.success(self.request,"비밀번호가 성공적으로 변경되었습니다.")
        return super().form_valid(form)
    
class UserUpdateOFF(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UpdateFormOFF
    template_name = 'userinfo/updateOFF.html'
    
    def get_object(self):
        return get_object_or_404(User,username=self.kwargs["username"])
    
    def form_valid(self, form) :
        user = self.object
        user.is_activated = False
        user.save()
        messages.success(self.request,"해당 계정이 정지되었습니다. 이용해주셔서 감사합니다.")        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('user:logout')   

class UserInfoView(DetailView):
    model = User
    template_name = "userinfo/userinfo_base.html"
    pk_url_kwarg = "UID"
    context_object_name = "theUser"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        who = User.objects.get(nickname=self.kwargs["nickname"])
        post = Post.objects.filter(PostAuthor=who)
        comments = Comment.objects.filter(CommentAuthor=who)
        context["posts"] = post[::-1][:15]
        context["comments"] = comments[::-1][:15]
        return context
    
    def get_object(self):
        return get_object_or_404(User,nickname=self.kwargs["nickname"])


'''
def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username = username, password = password)

        if user is not None and user.is_active:
            login(request,user)
            return redirect("board:home")
        else:
            messages.error(request,"아이디와 비밀번호가 일치하지 않거나 존재하지 않습니다.")
            return redirect("user:login")
    else:
        form = LoginForm()
        return render(request,"userinfo/login.html", {'form' : form})

def signupView(request):
    if request.method == "POST":
        form = SignUserForm(request.POST)
          
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            return redirect("user:login")
        else:
            print("뭔가 잘못됨")
    else:
        form = SignUserForm()
        return render(request,"userinfo/signup.html",{'form' : form})
'''