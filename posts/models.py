# posts/models.py
from django.db import models

# 게시글(Post) 모델 정의
class Post(models.Model):
    # 게시글 제목: 최대 200자까지 입력 가능한 문자열 필드
    title = models.CharField(max_length=200)
    # 게시글 내용: 길이 제한 없는 텍스트 필드
    content = models.TextField()
    # 게시글 작성일: 생성 시 자동으로 현재 시간 저장
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Post 객체를 문자열로 표현할 때, 제목(title) 출력
        return self.title


# 댓글(Comment) 모델 정의
class Comment(models.Model):
    # Post 모델과 연결 (ForeignKey): 하나의 게시글(Post)에 여러 댓글(Comment) 가능
    # related_name='comments' -> post.comments를 통해 해당 게시글의 댓글 목록 접근 가능
    # on_delete=models.CASCADE -> 게시글 삭제 시, 해당 댓글들도 같이 삭제
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    # 댓글 내용: 길이 제한 없는 텍스트 필드
    content = models.TextField()
    # 댓글 작성일: 생성 시 자동으로 현재 시간 저장
    created_at = models.DateTimeField(auto_now_add=True)
    # 댓글 수정일: 저장 시마다 현재 시간으로 자동 업데이트
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Comment 객체를 문자열로 표현할 때, 어떤 게시글의 댓글인지 표시
        return f'Comment on {self.post}'