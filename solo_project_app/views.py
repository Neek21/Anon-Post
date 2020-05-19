from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    if 'user' in request.session:
        return redirect('/dashboard')
    
    request.session['auth'] = 0
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def register_process(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')


    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


    new_user = User.objects.create(
        username = request.POST['username'],
        email = request.POST['email'],
        password = pw_hash  
    )

    request.session['user'] = new_user.username
    request.session['id'] = new_user.id
    return redirect('/dashboard')

def dashboard(request):
    if 'user' not in request.session:
        return redirect('/')
    
    request.session['auth'] = 0
    context = {
        'posts': Post.objects.all().order_by('-created_at')
    }

    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def login(request):
    logged_username = User.objects.filter(username=request.POST['username'])
    errors = {}
    if len(logged_username) == 0:
        errors['username_not_used'] = 'Username is not in use'
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    if len(logged_username) > 0:
        logged_username = logged_username[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_username.password.encode()):
            request.session['user'] = logged_username.username
            request.session['id'] = logged_username.id
            request.session['auth'] = 0
            return redirect('/dashboard')
        else:
            errors['no_match'] = "Username and password don't match"
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    return redirect('/')

def post_process(request):
    if 'user' not in request.session:
        return redirect('/')

    errors = Post.objects.post_validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard')

    Post.objects.create(
        post = request.POST['post'],
        poster = User.objects.get(id = request.session['id'])
    )

    return redirect('/dashboard')

    
def like(request, id):
    liked_post = Post.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_post.user_likes.add(user_liking)
    return redirect('/dashboard')

def like_prof(request, id):
    liked_post = Post.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_post.user_likes.add(user_liking)
    return redirect('/profile')

def like_post(request, id):
    liked_post = Post.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_post.user_likes.add(user_liking)
    return redirect(f'/view_post/{id}')

def unlike(request, id):
    liked_post = Post.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_post.user_likes.remove(user_liking)
    return redirect('/dashboard')

def unlike_prof(request, id):
    liked_post = Post.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_post.user_likes.remove(user_liking)
    return redirect('/profile')

def unlike_post(request, id):
    liked_post = Post.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_post.user_likes.remove(user_liking)
    return redirect(f'/view_post/{id}')

def post(request,id):
    request.session['auth'] = 0
    context ={
        'post': Post.objects.get(id=id)
    }
    return render(request, 'post.html', context)

def comment_process(request):
    if 'user' not in request.session:
        return redirect('/')
    postNum = request.POST['post_num']
    errors = Comment.objects.comment_validator(request.POST)
    
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/view_post/{postNum}')

    Comment.objects.create(
        comment = request.POST['comment'],
        poster = User.objects.get(id=request.session['id']),
        post_comment = Post.objects.get(id=postNum)
    )

    return redirect(f'/view_post/{postNum}')

def profile(request):
    request.session['auth'] = 0
    user = User.objects.get(id=request.session['id'])
    context ={
        'user': User.objects.get(id=request.session['id']),
        'user_posts': user.posts_posted.all().order_by('-created_at')
    }

    return render(request, 'profile.html', context)

def favorite_post(request, id):
    favorited_post = Post.objects.get(id=id)
    user_favoriting = User.objects.get(id=request.session['id'])
    favorited_post.user_favorites.add(user_favoriting)
    return redirect(f'/view_post/{id}')

def confirm_edit(request):
    return render(request, 'confirm_edit.html')

def edit_auth(request):
    logged_username = User.objects.get(id=request.session['id'] )
    errors = {}
    if bcrypt.checkpw(request.POST['password'].encode(), logged_username.password.encode()):
        request.session['auth'] = 1
        return redirect('/edit_profile')
    else:
        errors['wrong_pass'] = "Incorrect password."
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/confirm_edit')

def edit_profile(request):
    if request.session['auth'] != 1:
        return redirect('/dashboard')

    context ={
        'user': User.objects.get(id = request.session['id'])
    }

    return render(request, 'edit.html', context)

def edit_process(request):
    user = User.objects.get(id = request.session['id'])

    errors = {}

    if user.email != request.POST['email']:
        emailCheck = User.objects.filter(email=request.POST['email'])
        if len(emailCheck) > 0:
            errors['email_in_use'] = 'Email is already in use'
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit_profile')

    errors = User.objects.edit_validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit_profile')

    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user.email = request.POST['email']
    user.password = pw_hash
    user.save()
    request.session['auth'] = 0

    return redirect ('/profile')

def profile_ml(request):
    request.session['auth'] = 0
    user = User.objects.get(id=request.session['id'])
    context ={
        'user': User.objects.get(id=request.session['id']),
        'user_posts': user.posts_posted.all().order_by('-user_likes')
    }

    return render(request, 'profile.html', context)

def profile_faves(request):
    request.session['auth'] = 0
    user = User.objects.get(id=request.session['id'])
    context ={
        'user': User.objects.get(id=request.session['id']),
        'user_posts': user.favorite_posts.all()
    }

    return render(request, 'profile.html', context)

def confirm_delete(request, id):
    context ={
        'post': Post.objects.get(id=id)
    }

    return render(request, 'confirm_delete.html', context)

def confirm_delete_prof(request, id):
    context ={
        'post': Post.objects.get(id=id)
    }

    return render(request, 'confirm_delete_prof.html', context)


def delete(request, id):
    request.session['auth'] = 0
    post = Post.objects.get(id=id)
    post.delete()

    return redirect('/dashboard')

def delete_prof(request, id):
    request.session['auth'] = 0
    post = Post.objects.get(id=id)
    post.delete()

    return redirect('/profile')

