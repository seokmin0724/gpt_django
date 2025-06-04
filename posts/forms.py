from django import forms  # 장고에서 폼을 만들기 위한 도구를 불러와요
from .models import Post, Comment  # 우리가 만든 글(Post), 댓글(Comment) 모델을 가져와요
from django import forms  # (중복으로 적었는데 한 줄만 있어도 돼요! 아래에서 지울 거예요)

# ================================
# ✍️ 글쓰기 폼 만들기
# ================================
class PostForm(forms.ModelForm):  # 글을 쓸 수 있는 폼을 만들어요
    class Meta:
        model = Post  # 이 폼은 Post 모델(글 데이터)과 연결돼 있어요
        fields = ['title', 'content']  # 사용자가 제목이랑 내용을 입력할 수 있어요

# ================================
# 💬 댓글 쓰기 폼 (기본 버전)
# ================================
class CommentForm(forms.ModelForm):  # 댓글을 입력할 수 있는 폼이에요
    class Meta:
        model = Comment  # 이 폼은 Comment 모델(댓글 데이터)과 연결돼 있어요
        fields = ['content']  # 사용자가 댓글 내용을 입력할 수 있어요

# ⚠️ 위에 CommentForm이 있는데, 아래에 같은 이름으로 또 만들어졌어요.
# 아래 폼이 마지막에 덮어쓰기 때문에 실제로는 이 폼만 사용돼요.
# 이 폼은 댓글 입력칸을 더 보기 좋게 꾸며줘요.

# ================================
# 💬 댓글 쓰기 폼 (예쁘게 꾸민 버전 - 실제로 사용하는 폼!)
# ================================
class CommentForm(forms.ModelForm):  # 댓글을 입력할 수 있는 폼이에요
    class Meta:
        model = Comment  # 이 폼도 Comment 모델과 연결돼 있어요
        fields = ['content']  # 댓글 내용만 입력 가능해요
        widgets = {
            'content': forms.Textarea(attrs={  # 입력 칸을 'Textarea'(여러 줄 입력창)로 설정해요
                'rows': 3,  # 댓글 칸의 줄 수는 3줄로 보여요
                'placeholder': '댓글을 입력하세요. 😊',  # 입력하기 전에 흐리게 보이는 안내 문구예요
                'class': 'form-control',  # 예쁘게 보이도록 스타일을 입혀줘요 (bootstrap용)
            })
        }
