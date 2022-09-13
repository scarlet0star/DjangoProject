from django import forms
from .models import User
from django.contrib.auth.forms import PasswordChangeForm,UserCreationForm

class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"아이디 입력", 'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"비밀번호 입력", 'class':'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    
    class Meta:
        model = User
        fields = ['username','password']

class SignUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"아이디 입력", 'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"비밀번호 입력", 'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"비밀번호 입력 확인", 'class':'form-control'}))
    nickname = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"닉네임 입력", 'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder":"이메일주소", 'class':'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    
    '''def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    '''
    class Meta:
        model = User
        fields = ['username','password1', 'password2','nickname', 'email']
        
class UpdateForm(forms.ModelForm):
    nickname = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"변경할 닉네임 입력", 'class':'form-control'}),label="변경할 닉네임")
    email = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"변경할 이메일 주소 입력", 'class':'form-control'}),label="변경할 이메일 주소")
    class Meta:
        model = User
        fields = ['nickname','email']
        
class UpdateFormOFF(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']

class UpdatePWForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder":"현재 비밀번호 입력", 'class':'form-control'}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder":"새로운 비밀번호 입력", 'class':'form-control'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder":"새로운 비밀번호 확인 입력", 'class':'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    
    def clean(self):
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password1")

        if old_password == new_password1:
            self.add_error(
                "old_password",
                forms.ValidationError("이전 비밀번호와 입력된 새로운 비밀번호이 같습니다.")
            )
        else:
            return self.cleaned_data