# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from uuid import uuid4
# Create your models here.

class signupuser(models.Model):
    username = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "<signupuser:%s-%s>" %(self.username,self.id)

class SessionToken(models.Model):
    user = models.ForeignKey(signupuser)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token=str(uuid4())

class PostModel(models.Model):
    user = models.ForeignKey(signupuser)
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def like_count(self):
        return self.likemodel_set.count()

    @property
    def comments(self):
        return self.commentmodel_set.order_by("created_on").all()

    def liked_by_user(self, user):
        l = self.likemodel_set.filter(user=user)
        return len(l) > 0

class LikeModel(models.Model):
    user = models.ForeignKey(signupuser)
    post = models.ForeignKey(PostModel)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class CommentModel(models.Model):
  user = models.ForeignKey(signupuser)
  post = models.ForeignKey(PostModel)
  comment_text = models.CharField(max_length=555)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)