from django.shortcuts import render, redirect, resolve_url

from .models import Post, Comment, Profile, Thread_Model, Message_Model, Notification

from .forms import Post_Form, Comment_form, Register_form, Profile_form, Thread_Form, Message_Form

from django.contrib.auth.decorators import login_required


from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login

#Send Mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

#Message
from django.contrib.auth.models import User
from django.views.generic import View
from django.db.models import Q

# Like and Dislike 
from django.http import HttpResponseRedirect, HttpResponse


@login_required(login_url="Index")
def Home(request):
    posts = Post.objects.all().order_by('-created_at')
        
    
    content = {
        'post_list': posts,
    }

    return render(request, 'pages/home.html', content)

@login_required(login_url="Index")
def Add_Post(request, pk):
    pk = request.user.pk

    posts = Post.objects.all()
    form =  Post_Form()
    post = Post.objects.all()

    if request.method == "POST":
        form = Post_Form(request.POST, request.FILES)

        if form.is_valid():
            post1 = form.save(commit=False)
        
            img = form.cleaned_data.get('picture')
            post1.picture = img
            post1.author = request.user
            post1.save()

            return redirect( 'Home')

    content = {
        'post_list': posts,
        'form': form,
        'post':post,
    }

    return render(request, 'pages/add_post.html', content)

@login_required(login_url="Index")
def Post_Detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = Comment_form(request.POST)
    comment = Comment.objects.all()


    if form.is_valid():
        new_comment = form.save(commit=False) 
        new_comment.author = request.user
        new_comment.post = post
        new_comment.save()

        if request.user.profile is True:
            h_user = request.user.profile.name

        else:
            h_user = request.user

        notification = Notification.objects.create(notification_type=2, from_user=h_user, to_user=post.author, post=post)

        return redirect('post-detail', pk=post.pk)


    comments = Comment.objects.filter(post=post).order_by('-created_at')

    
    content = {
        'post': post,
        'form': form,
        'comments': comments,
        'comment': comment,
    }

    return render(request, 'pages/post_detail.html', content)

@login_required(login_url="Index")
def Post_Edit(request, pk):
    post = Post.objects.get(pk=pk)
    form = Post_Form(instance=post)

    content = {
        'post': post,
        'form': form
    }
    if request.method == "POST":
        form = Post_Form( request.POST , instance=post)

        if form.is_valid():
            img = form.cleaned_data.get('picture')
            form.picture = img
            form.save()

            return redirect( 'post-detail', pk=post.pk)

    return render(request, 'pages/post_edit.html', content)


@login_required(login_url="Index")
def Post_Delete(request, pk):
    post = Post.objects.get(pk=pk)

    content = {
        'post': post
    }
    
    if request.method == "POST":

        post.delete()
        return redirect('Home')
    
    return render(request, 'pages/post_delete.html', content)


@login_required(login_url="Index")
def   Comment_Edit(request, pk):
    comment = Comment.objects.get(pk=pk)
    form = Comment_form(instance=comment)
    

    content = {
        'comment': comment,
        'form': form,
    }
    
    if request.method == "POST":
        form = Comment_form(request.POST, request.FILES, instance=comment)
        
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=comment.post.pk)

        
    return render(request, 'pages/comment_edit.html', content)

@login_required(login_url="Index")
def Comment_Delete(request, pk):

    comment = Comment.objects.get(pk=pk)

    content = {
        'comment': comment
    }

    if request.method == "POST":
        comment.delete()

        return redirect('post-detail', pk= comment.post.pk)
    
    return render(request, 'pages/comment_delete.html', content)


def Register(request):

    register_form = Register_form()

    if request.method == "POST":
        register_form = Register_form(request.POST)

        if register_form.is_valid():
            register_form.save()

            template = render_to_string('profiles/email.html',
            {   'name': request.user.username,
                'created_at': request.user.password
            })
            email = EmailMessage(
            'Thanks for Sing up in Karma',
            template,
            settings.EMAIL_HOST_USER,
            [request.user.email],)

            email.fail_silently = False
            email.send()
            
        return redirect('login')
            

    content = {
        'register_form': register_form
    }

    return render(request, 'profiles/register_page.html', content)

@login_required(login_url="Index")
def Profile_View(request, pk):

    profile = Profile.objects.get(pk=pk)
    user = profile.user
    posts = Post.objects.filter(author=user).order_by('-created_at')

    followers = profile.followers.all()

    if len(followers) == 0:
        is_following = False 
    
    for follower in followers:
        if follower == request.user:
            is_following = True
            break
        else:
            is_following = False

    number = len(followers)

    content = {
        'profile':profile,
        'posts': posts,
        'number':number,
        'is_following': is_following,
    }


    return render(request, 'profiles/profile.html', content)


def login(request):

    if request.user.is_authenticated:
        return redirect('Home')
    
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('Home')

            else:
                return redirect('login')

    return render(request, 'profiles/login_page.html')            

def logout_page(request):

    logout(request)
    return redirect('Index')


@login_required(login_url="Index")
def Create_Profile(request, pk):
    pk = request.user.pk
    profile = Profile.objects.all()
    
    form = Profile_form()

    content = {
        'form': form,
        'profile':profile,
    }

    if request.method == "POST":
        form  = Profile_form(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():

            user  = form.save()
            user.user = request.user
            user.save()

            return redirect('profile', pk=user.pk)          


    return render(request, 'profiles/create_profile.html', content)


def Profile_Edit(request, pk):
    profile = Profile.objects.get(pk=pk)
    form = Profile_form(instance=profile)

    content = {
        'profile': profile,
        'form': form,
    }

    if request.method == "POST":
        form = Profile_form(request.POST,request.FILES, instance=profile)

        if form.is_valid():
            form.save()

            return redirect('profile', pk=profile.pk)
    
    return render(request, 'profiles/profile_edit.html', content)


"""
At this point it is easier to work with classes but for my learning I think it will be better to work with functions
    since it is a bit more complicated for certain things ..... 
    also to later take this project to the next level with APIS it is easier for me ...

"""

class Create_Thread(View):

  def get(self, request, *args, **kwargs):
    form = Thread_Form()
    context = {
      'form': form
    }
    return render(request, 'messages/create_thread.html', context)

  def post(self, request, *args, **kwargs):
    form = Thread_Form(request.POST)
    username = request.POST.get('username')

    try:
      receiver = User.objects.get(username=username)
      if Thread_Model.objects.filter(user=request.user, receiver=receiver).exists():
        thread = Thread_Model.objects.filter(user=request.user, receiver=receiver)[0]
        return redirect('thread', pk=thread.pk)
      
      if form.is_valid():
        sender_thread = Thread_Model(
          user=request.user,
          receiver=receiver
        )
        sender_thread.save()
        thread_pk = sender_thread.pk
        return redirect('thread', pk=thread_pk)
    except:
      return redirect('create-thread')
    
class List_Threads(View):

  def get(self, request, *args, **kwargs):
    threads = Thread_Model.objects.filter(Q(user=request.user) | Q(receiver=request.user))
    
    context = {
    'threads': threads
    }
    return render(request, 'messages/thread_view.html', context)
   

class Create_Message(View):

  def post(self, request, pk, *args, **kwargs):

    thread = Thread_Model.objects.get(pk=pk)

    if thread.receiver == request.user:
      receiver = thread.user

    else:
      receiver = thread.receiver

    message = Message_Model(
        thread=thread,
        sender_user=request.user,
        receiver_user=receiver,
        content=request.POST.get('message'),
      )

    message.save()
    return redirect('thread', pk=pk)


class Thread_View(View):
  def get(self, request, pk, *args, **kwargs):

    form = Message_Form()
    thread = Thread_Model.objects.get(pk=pk)
    message_list = Message_Model.objects.filter(thread__pk__contains=pk)

    context = {
      'thread': thread,
      'form': form,
      'message_list': message_list
    }

    return render(request, 'messages/thread.html', context)


class Add_Follow(View):

    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.add(request.user)
        
        if request.user.profile is True:
        
            h_user = request.user.profile.name

        else:
            h_user = request.user

            notification = Notification.objects.create(notification_type=3, from_user=h_user, to_user=profile.user)

        return redirect('profile', pk=profile.pk)

class Remove_follow(View):
    
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('profile', pk=profile.pk)


class Add_like(View):
    
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():

            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)
            
            if request.user.profile is True:
        
                h_user = request.user.profile.name

            else:
                h_user = request.user

            notification = Notification.objects.create(notification_type=1, from_user=h_user, to_user=post.author, post=post)


        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class Dislike(View):

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():

            if like == request.user:
                is_like = True
                break
        
        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if not is_dislike:
            post.dislikes.add(request.user)
                    
        
        if is_dislike:
            post.dislikes.remove(request.user)


        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class Comment_like(View):

    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.c_dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if is_dislike:
            comment.c_dislikes.remove(request.user)

        is_like = False

        for like in comment.c_likes.all():

            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.c_likes.add(request.user)
            
            if request.user.profile is True:
        
                h_user = request.user.profile.name

            else:
                h_user = request.user

            notification = Notification.objects.create(notification_type=1, from_user=h_user, to_user=comment.author, comment=comment)


        if is_like:
            comment.c_likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class Comment_Dislike(View):

    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.c_likes.all():

            if like == request.user:
                is_like = True
                break
        
        if is_like:
            comment.c_likes.remove(request.user)

        is_dislike = False

        for dislike in comment.c_dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if not is_dislike:
            comment.c_dislikes.add(request.user)
                    
        
        if is_dislike:
            comment.c_dislikes.remove(request.user)


        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class Post_Notification(View):

    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post-detail', pk = post_pk)



class Follow_Noification(View):

    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = Profile.objects.get(pk=profile_pk)

        notification.user_has_seen = True
        notification.save()
        return redirect('profile', pk = profile_pk)


class Remove_Notification(View):

    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user.has_seen = True
        notification.save()

        return HttpResponse('success', content_type='text/plain')


    

