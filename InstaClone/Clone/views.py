# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.hashers import make_password,check_password
from imgurpython import ImgurClient
from InstaClone.settings import BASE_DIR
from uuid import uuid4

from .forms import signupform,loginform,PostForm,LikeForm,CommentForm
from .models import signupuser,SessionToken,PostModel,LikeModel,CommentModel


# Create your views here.

def signupview(request):
    today = datetime.now()
    if request.method=="GET":
        form=signupform()
    if request.method=="POST":
        form=signupform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            hashed_password=make_password(password)
            user=signupuser(username=username,name=name,email=email,password=password)
            user.save()
            response=redirect("/login")
            return response
    return render(request,"signup.html",{
        "today":today,
        "form":form
    })

def loginview(request):
    if request.method=="GET":
        form=loginform()
        return render(request, "login.html", {
            "form": form
        })
    if request.method=="POST":
        form=loginform(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=signupuser.objects.filter(username=username,password=password).first()

            if user:
                # check_password(password,user.password)
                session=SessionToken(user=user)
                session.create_token()
                session.save()
                response=redirect("/feed")
                response.set_cookie(key="session_token",value=session.session_token)
                return response
                print "User is valid"
            else:
                print "User is not valid"


def check_validation(request):
    if request.COOKIES.get('session_token'):
        session=SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
             return session.user
    else:
        return None

def postview(request):
    user = check_validation(request)
    if user:
        print 'Authentic user'
    else:
        return redirect('/login/')

    if request.method == "GET":
        form = PostForm()
        return render(request , "post.html" , {
            "form" : form
        })
    elif request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')
            post = PostModel(user = user , image = image , caption = caption)
            post.save()
            path = str(BASE_DIR + "\\" + post.image.url)
            client = ImgurClient("d91e315eb201bda", "3abed8ee4f7f5abefb205e7a5e15850a9cc8493c")
            post.image_url = client.upload_from_path(path, anon=True)['link']
            post.save()
            return redirect("/feed")


def feedview(request):
    user=check_validation(request)
    if user:
        posts=PostModel.objects.all().order_by("created_on")
        return render(request, "feeds.html",{
            "posts" : posts
        })
    else:
        return redirect('/login/')
    # return render(request, "feeds.html")

def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id

            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()

            return redirect('/feed/')
    else:
     return redirect('/login/')

def comment_view(request):
  user = check_validation(request)
  if user and request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      post_id = form.cleaned_data.get('post').id
      comment_text = form.cleaned_data.get('comment_text')
      comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
      comment.save()
      return redirect('/feed/')
    else:
        return redirect('/feed/')
  else:
    return redirect('/login')