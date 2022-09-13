from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView,TemplateView
from rest_framework.mixins import UpdateModelMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q,Count

from .models import Board
from .forms import *
from userinfo.models import User
from userinfo.utils import *
# Create your views here.

class BoardIndexView(ListView):
    model = Board
    context_object_name = 'BoardList'
    template_name = 'board/board_list.html'
    
    def get_queryset(self):
        return Board.objects.filter(isActivate = True)
    
class BoardListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 20
    template_name = 'board/board_View.html'
    ordering = ['-PostID']
    page_kwarg = 'page'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = Board.objects.get(subject = self.kwargs['boardName'])
        paginator = context['paginator']
        page_numbers_range = 10
        max_index = len(paginator.page_range)
        
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        
        start_index = int((current_page -1 ) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        
        return context
    
    def get_queryset(self):
        board = Board.objects.get(subject=self.kwargs['boardName'])
        
        return Post.objects.filter(board= board).order_by('-PostID')

class BoardCreateView(LoginRequiredMixin,CreateView):
    model = Board
    form_class = boardForm
    template_name = 'board/create.html'
    
    def form_valid(self, form):
        newBoard = form.save(commit=False)
        newBoard.principal = self.request.user   
        newBoard.save()
        messages.success(self.request, "게시판이 성공적으로 생성되었습니다")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('board:aboard',kwargs={'boardName':self.object.subject})

class BoardPostView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    context_object_name = 'Board'
    template_name = 'board/postCreate.html'
    
    def form_valid(self, form):
        form.instance.PostAuthor = self.request.user
        form.instance.board = Board.objects.get(subject=self.kwargs['boardName'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('board:detail', kwargs={'boardName':self.object.board.subject, 'postID':self.object.PostID})
    
class BoardSearchView(ListView):
    model = Post
    template_name = 'board/board_search.html'
    context_object_name = 'posts'
    paginate_by = 20
    
    def get_queryset(self):
        search_type = self.request.GET.get('t','')
        search_content = self.request.GET.get('c','')
        post_list = Post.objects.order_by('-PostID')
        
        if search_content :
            if search_type == 'wide':
                searched_list = post_list.filter(Q (title__icontains= search_content) 
                                               | Q (contents__icontains = search_content))
            elif search_type == 'title':
                searched_list = post_list.filter(Q (title__icontains= search_content))
            
            elif search_type == 'author':
                searched_list = post_list.filter(Q (PostAuthor__nickname= search_content))
            
            return searched_list
        else:
            messages.error(self.request,'잘못된 접근입니다')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = Board.objects.get(subject = self.kwargs['boardName'])
        search_type = self.request.GET.get('t','')
        search_content = self.request.GET.get('c','')
        
        paginator = context['paginator']
        page_numbers_range = 10
        max_index = len(paginator.page_range)
        
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        
        start_index = int((current_page -1 ) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        
        context['boardName'] = self.kwargs['boardName']
        context['type'] = search_type
        context['content'] = search_content
        
        return context
    
class PostLikeSearchView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 20
    template_name = 'board/board_View.html'
    ordering = ['-PostID']
    page_kwarg = 'page'
    
    def get_queryset(self):
        board = Board.objects.get(subject=self.kwargs['boardName'])
        return Post.objects.annotate(num_like=Count('like_user')).filter(board=board,num_like__gte=2)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = Board.objects.get(subject = self.kwargs['boardName'])

        paginator = context['paginator']
        page_numbers_range = 10
        max_index = len(paginator.page_range)
        
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        
        start_index = int((current_page -1 ) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        
        context['boardName'] = self.kwargs['boardName']
        return context
    
class PostDetailView(FormMixin,UpdateModelMixin,DetailView):
    model = Post
    template_name = "post/post_base.html"
    pk_url_kwarg = 'postID'
    context_object_name = 'thePost'
    form_class = CommentForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(post=self.object.PostID)
        context['comments'] = comments 
        return context
    
    def get_object(self):
        return get_object_or_404(Post,PostID=self.kwargs['postID'])
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self,form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.CommentAuthor = self.request.user
        comment.save()  
        self.object.comments += 1
        self.object.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('board:detail', kwargs={'boardName':self.object.board.subject, 'postID':self.object.PostID})
  

class PostLikeView(LoginRequiredMixin,TemplateView):
    model = Post
    template_name = 'post/post_base.html'
    
    def get_object(self):
        return get_object_or_404(Post,PostID=self.kwargs['postID'])
    
    def post(self,request,*arg,**kwargs):
        user = request.user
        self.object = self.get_object()
        if user in self.object.like_user.filter(pk=user.pk):
            self.object.like_user.remove(user)
        else:
            self.object.like_user.add(user)
        return redirect(request.META['HTTP_REFERER'])

 
class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = "board/postCreate.html"
    pk_url_kwarg = 'postID'
    
    def get_object(self):
        return get_object_or_404(Post,PostID=self.kwargs['postID'])
    
    def get_success_url(self):
        return reverse('board:detail', kwargs={'boardName':self.object.board.subject, 'postID':self.object.PostID})
    
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = "post/post_delete.html"
    pk_url_kwarg = 'postID'
    
    def get_success_url(self):
        return reverse('board:aboard', kwargs={'boardName':self.object.board.subject})
    
class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    form_class = CommentForm
    context_object_name = 'comment'
    template_name = 'comment/comment_base.html'
    
    def form_valid(self, form):
        form.instance.CommentAuthor = self.request.user
        form.instance.post = self.kwargs['postID']
        PP = Post.objects.get(postID= self.kwargs['postID'])
        PP.comments += 1
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('board:detail', kwargs={'boardName':self.kwargs['boardName'],'postID': self.kwargs['postID']})
    
class CommentUpdateView(LoginRequiredMixin,UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comment/comment_edit.html"
    
    def get_object(self):
        return get_object_or_404(Comment,CommentID=self.kwargs["commentID"])
    
    def get_success_url(self):
        return reverse('board:detail', kwargs={'boardName':self.kwargs['boardName'],'postID': self.kwargs['postID']})

class CommentDeleteView(LoginRequiredMixin,DeleteView):
    model = Comment
    template_name = "comment/comment_delete.html"
    
    def get_object(self):
        return get_object_or_404(Comment,CommentID=self.kwargs["commentID"])
    
    def get_success_url(self):
        post = Post.objects.get(pk=self.kwargs['postID'])
        post.comments -= 1
        post.save()
        return reverse('board:detail', kwargs={'boardName':self.kwargs['boardName'],'postID': self.kwargs['postID']})
    
'''def BoardIndexView(request):
    subjects = Board.objects.all()
    return render(request, "board/board_list.html", {'subjects':subjects})
    
def BoardCreateView(request):
    if request.method == "POST":
        form = boardForm(request.POST)
    
        if form.is_valid():
            uid = request.session.get("_auth_user_id")
            who = User.objects.get(pk=uid)
            
            board = Board()
            board.subject = form.cleaned_data['subject']
            board.context = form.cleaned_data['context']
            board.isActivate = True
            board.principal = who
            
            board.save()
            return redirect("board:home")
        else:
            print("실패!")
    else:
        form = boardForm()
    return render(request,'board/create.html',{'form':form, })
    
def CreatePost(request,boardName):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid:
            uid = request.session.get("_auth_user_id")
            who = User.objects.get(pk=uid)
            
            post = Post()
            post.author = who
            post.board = boardName
            
            post.save()
            return redirect("board:aboard",boardName = boardName)
            #return redirect("board:postDetail",boardName = boardPK, postid=post.postNumber)          
    else:
        form = PostForm()
    return render(request,'board/postCreate.html', {'form': form, 'boardName':boardName})
'''