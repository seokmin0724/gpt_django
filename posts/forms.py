# posts/forms.py

from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm): # Post 모델을 기반으로 한 Form 정의
    class Meta:
        model = Post   # 사용할 모델은 Post
        fields = ['title', 'content'] # Post 모델의 title과 content 필드를 폼에 포함

class CommentForm(forms.ModelForm): # Comment 모델을 기반으로 한 Form 정의
    class Meta: # 사용할 모델은 Comment
        model = Comment # Comment 모델의 content 필드만 폼에 포함
        fields = ['content']