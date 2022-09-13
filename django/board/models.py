from django.db import models
from django.urls import reverse
from userinfo.models import User

# Create your models here.

class Board(models.Model):
    BoardID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='BID')
    subject = models.CharField(max_length=60, unique=True)
    context = models.CharField(max_length=100)
    principal = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    isActivate = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.pk} : {self.subject}'

    def get_absolute_url(self):
        return reverse('board-detail-view',args=[self.subject])
    

class Post(models.Model):
    PostID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='PID')
    PostAuthor = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    board = models.ForeignKey(Board,on_delete=models.CASCADE)
    
    title = models.CharField(max_length=50)
    contents = models.TextField()
    
    writeDate = models.DateTimeField(auto_now_add=True)
    modifyDate = models.DateTimeField(auto_now=True)
    
    views = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    
    like_user = models.ManyToManyField(User,through='Like',through_fields=('post','user'),related_name='likes')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail-view',args=[self.pk])
    
    def count_like(self):
        return self.like_user.count()
    
    @property
    def UpdateViews(self):
        self.views += 1
        self.save()
        return ""

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}이 {self.post} 게시물을 추천함'

class Comment(models.Model):
    CommentID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='CID')
    CommentAuthor = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    parent =  models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True)
    contents = models.TextField(max_length= 200)

    writeDate = models.DateTimeField(auto_now_add=True)
    modifyDate = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if len(self.contents) >= 20:
            return self.contents[:20]
        else:
            return self.contents