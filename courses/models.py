from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField

# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        ordering = ['title']
    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(User,related_name='courses_created',on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,related_name='courses',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,related_name='courses_joined',blank=True) # After users create an account, they should be able to enroll on courses. In order to store enrollments, you need to create a many-to-many relationship between the Course and User models.
    class Meta:
        ordering = ['-created']
        # ordering = ['order']
    def __str__(self):
        return self.title

    # owner: The instructor who created this course.
    # subject: The subject that this course belongs to. It is a ForeignKey field that
    # points to the Subject model.
    # title: The title of the course.
    # slug: The slug of the course. This will be used in URLs later.
    # overview: A TextField column to store an overview of the course.
    # created: The date and time when the course was created. It will be
    # automatically set by Django when creating new objects because of auto_now_
    # add=True.
    

class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course']) # You name the new field order, and specify that the ordering is calculated with respect to the course by setting for_fields=['course']. This means that the order for a new module will be assigned by adding 1 to the last module of the same Course object.
    def __str__(self):
        return f'{self.order}. {self.title}'
    class Meta:
        ordering = ['order']

# Each course is divided into several modules. Therefore, the Module model contains
# a ForeignKey field that points to the Course model.

class Content(models.Model):
    module = models.ForeignKey(Module,related_name='contents',on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,
                                    limit_choices_to={'model__in':(
                                    'text',
                                    'video',
                                    'image',
                                    'file')})
                                    # You add a limit_choices_to argument to limit the ContentType objects that can be
                                    # used for the generic relation. You use the model__in field lookup to filter the query
                                    # to the ContentType objects with a model attribute that is 'text', 'video', 'image',
                                    # or 'file'.
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module']) # Module contents also need to follow a particular order.
    class Meta:
        ordering = ['order']
   


# This is the Content model. A module contains multiple contents, so you define a
# ForeignKey field that points to the Module model. You also set up a generic relation
# to associate objects from different models that represent different types of content.
# Remember that you need three different fields to set up a generic relation. In your
# Content model, these are:
# • content_type: A ForeignKey field to the ContentType model
# • object_id: A PositiveIntegerField to store the primary key of the related
# object
# • item: A GenericForeignKey field to the related object combining the two
# previous fields
# Only the content_type and object_id fields have a corresponding column in the
# database table of this model. The item field allows you to retrieve or set the related
# object directly, and its functionality is built on top of the other two fields.

class ItemBase(models.Model): #define an abstract model named ItemBase.
    owner = models.ForeignKey(User,related_name='%(class)s_related',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # you define the owner, title, created, and updated fields. These common fields will be used for all types of content. 
    class Meta:
        abstract = True
    def __str__(self):
        return self.title
    def render(self): # You need to provide a way to render each type of content
        return render_to_string(
        f'courses/content/{self._meta.model_name}.html',{'item': self})
        # This method uses the render_to_string() function for rendering a template and
        # returning the rendered content as a string. Each kind of content is rendered using
        # a template named after the content model. You use self._meta.model_name to
        # generate the appropriate template name for each content model dynamically. The
        # render() method provides a common interface for rendering diverse content

class Text(ItemBase):
    content = models.TextField()
class File(ItemBase):
    file = models.FileField(upload_to='files')
class Image(ItemBase):
    file = models.FileField(upload_to='images')
class Video(ItemBase):
    url = models.URLField()

# The owner field allows you to store which user created the content. Since this field
# is defined in an abstract class, you need a different related_name for each submodel. Django allows you to specify a placeholder for the model class name in the
# related_name attribute as %(class)s. By doing so, related_name for each child
# model will be generated automatically. Since you use '%(class)s_related' as
# the related_name, the reverse relationship for child models will be text_related,
# file_related, image_related, and video_related, respectively.

# You have defined four different content models that inherit from the ItemBase
# abstract model. These are as follows:
# • Text: To store text content
# • File: To store files, such as PDFs
# • Image: To store image files
# • Video: To store videos; you use an URLField field to provide a video URL
# in order to embed it






STATUS_CHOICES= (('draft','Draft'),('published','Published'))

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    slug   = models.SlugField(max_length=255,unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTime Field (auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status  = models.CharField(max_length='10', choices='STATUS_CHOICES', default='draft')


    class Meta:
        ordering = ('-publish')
    def __str__(sef):
        return self.title

from django.contrib import admin
from .models imoort Post

admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin): ur model is registered using a custom class that inherits from the ModelAdmin
    list_display = ('title','author','slug','publish','status')
    list_filter  = ('status','publish','created')
    search_fields = ('body', 'title')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author')
    date_hierachy = 'pubish'
    ordering =('status','publish')

from django.contrib.auth.models import User
from blog.models import Post
user = User.objects.get(username='admin')
post = Post(title='yooo',slug='yooo',body='Yah mahn',author='user') 
post.save()

post= Post.objects.create(title='yoo',slug='yoo', body='kwkwkwk', author='user')
post.title = 'New title'
post.save()

all_posts = Post.objects.all|()

all_posts = Post.objects.all()
all_posts = Post.objects.filter(publish__year=2020, author__username='admin')
all_posts = Post.objects.filter(publish__year=2020).exclude(title_startswith='why')
all_posts = Post.objects.order_by('title')
all_posts  = Post.objects.get(id=1)

all_posts  = Post.objects.all()[:3]


class PublishedManager(models.Manager):
   def get_queryset(self):
       return(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()

from django.shortcuts import render, get_object_or_404

    all_posts = Post.published.filter(title_startswith='Who')  this is for the view

def post_list(request):
    posts = Post.published.all()
    return render(request,'blog/post/list.html',{'posts':posts})  

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,status='published',publish__year='year',publish__month='month',publish__day='day')
    return render(requuest,'blog/post/detail.html',{'post':post})

from django.urls import path
from  . import views
app_name = 'blog'

urlpatterns=[
    path('',views.post_list,name='post_list')
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail')

]

path('blog/',include('blog.urls', namespace='blog'))

from django.urls import reverse
class Post(models.Model):
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year,self.publish.month,self.publish.day,])

{% block extends " blog/base.html" %}
{% load static %}
{% block title %} My blog {% endblock %}
{% block content%}
{% for post in  posts %}
<h1><a href="post.get_absolute_url"> {{post.title}} </a><h1>
{% endfor %}
{% endblock%}


from django.core.paginator import Paginator,  EmptyPage, PageNotInteger

def post_list(request):
    object_list = Post.published.all()
    paginator   = Paginator(object_list,3) #You instatiate the Paginator class with the number of objects that u want to display on the page
    page        = request.GET.get('page') # You get the page GET parameter which indicates the current page
    try:
        posts  = paginator.page(page)    # You get the objects for the  desired page by calling the page () method of Paginator
    except PageNotInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)
    return render(request, 'blog/post/list.html','page':page,'posts':posts)


def post_list(request):
    object_list = Post.published.all()
    paginator   = Paginator(object_list,3)
    page        = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotInteger:
        posts = paginatpr.page(1)
    except EmptyPage:
        posts = pginaor.page(paginator.num_psge)

def post_list(request):
    object_list = Post.published.all()
    paginator   = Paginator(object_list, 3)
    page        = request.GET.get('page')
    try:

from django.views.generic import ListView

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name  = 'blog/post/list.html'

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name  = 'posts'
    paginate_by   = 3
    tempalte_name   = 'blog/post/list.html'

path('',views.PostListView.as_view(),name='post_list')
path('',views.PostListView.as_view(), name='post_list')

{% include "pagination.html" with page=page_obj %}


from django import forms
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to    = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.TextField)


def post_share(request,post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method=='POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form:form'})

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER  = 'your_account@gmail.com'
EMAIL_HOST_PASSWORD = 'your_password'
EMAIL_PORT =587
EMAIL_USE_TLS  = True

from django.core.mail import send_mail
def post_share(request,post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method=='POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject  = f"{cd['name']} recommends you read"f"{post.title}"
            message  = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments:{cd['comments']}"
            send_mail(subject, message,'admin@gmail.com',[cd['to']])  
            sent   = True

    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form, 'sent':sent})
    path('<int:post_id>/share/',views.post_share, name='post_shar')

    <a href="{% url  "blog:post_share" post.id %}"></a>
    <a href="{{ post.get_absolute_url }}">

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    active = models.BooleanField(defaul=True)

    class Meta:
        ordering = ('creating')
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

from .models import Comment 
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')


class Comment(models.Model):
  

from .forms import CommentForm
from .models import Post, Comment

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
    status='published',
    publish__year=year,
    publish__month=month,
    publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method =='POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = new_comment.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,'blog/post/detail.html',{'post':post,' comments':comments, 'new_comments':new_comments})









