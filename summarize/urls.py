from django.contrib import admin
from django.urls import path
from . import views 
from news.views import video_summarize
urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.api, name='api'),
    path('trigger-news-app/', video_summarize, name='trigger_news_app'),
]

