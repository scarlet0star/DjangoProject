from cProfile import label
from django import forms
from .models import *

from django_summernote.widgets import SummernoteWidget

class boardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    
    class Meta:
        model = Board
        fields = ['subject','context']
        widgets = {
            'subject' : forms.TextInput(attrs={
                "placeholder":"게시판 이름을 입력해주세요",
                'class':'form-control',
                }),
            
            'context' : forms.Textarea(attrs={
                "placeholder":"게시판 설명을 입력해주세요", 
                'class':'form-control'
                })
        }
class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    
    class Meta:
        model = Post
        fields = ['title','contents']
        widgets = {
            'title' : forms.TextInput(attrs={
                "placeholder":"제목을 입력해주세요",
                'class':'form-control mb-3',
            }),
            'contents' : SummernoteWidget()
        }

class CommentForm(forms.ModelForm):
    contents = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"댓글을 입력해주세요", 'class':'form-control','rows': 3, 'style':'resize:none;'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    
    class Meta:
        model = Comment
        fields = ['contents']
        widgets = {
            'contents' : forms.Textarea(attrs={
                "placeholder":"댓글을 입력해주세요",
                'class':'form-control',
            }),
        }