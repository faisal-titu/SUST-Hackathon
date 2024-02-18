from django.urls import path
from .views import  video_summarize

urlpatterns = [
    path('news/summarize', video_summarize, name='video_summarize'),
    # path('trigger-news-app/', video_summarize, name='video_summarize'),

    # path('news/videos/', news_videos, name='news_videos'),

    
    # Add more URL patterns as needed
]
