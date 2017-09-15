from django.conf.urls import url
from .views import *

urlpatterns=[
    url(r'signup',signupview),
    url(r'login',loginview),
    url(r'feed',feedview),
    url(r'post',postview),
    url(r'like/', like_view),
    url(r'comment/', comment_view),
]

