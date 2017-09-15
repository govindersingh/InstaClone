from django import forms
from .models import signupuser,PostModel,LikeModel,CommentModel

class signupform(forms.ModelForm):
    class Meta:
        model=signupuser
        fields=['email','username','name','password']

class loginform(forms.ModelForm):
    class Meta:
        model=signupuser
        fields=['username','password']

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ["image" , "caption"]

class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeModel
        fields=['post']

class CommentForm(forms.ModelForm):
  class Meta:
    model = CommentModel
    fields = ['comment_text', 'post']