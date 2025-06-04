from django.db import models  # 장고에서 데이터 저장할 때 사용하는 도구를 불러와요

# =================================
# ✍️ 글(Post) 모델 - 글의 정보 저장
# =================================
class Post(models.Model):
    title = models.CharField(max_length=200)
    # 글 제목을 저장해요 (최대 글자 수는 200자)

    content = models.TextField()
    # 글 내용을 저장해요 (길이에 제한 없이 쓸 수 있어요)

    created_at = models.DateTimeField(auto_now_add=True)
    # 글이 처음 만들어진 시간을 자동으로 저장해요


# =================================
# 💬 댓글(Comment) 모델 - 댓글 정보 저장
# =================================
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # 어떤 글(Post)에 달린 댓글인지 연결해줘요
    # 만약 글이 삭제되면 댓글도 같이 지워져요 (CASCADE)
    # post.comments로 댓글을 쉽게 불러올 수 있게 related_name을 붙였어요

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    # 이게 없으면 '일반 댓글'
    # 이게 있으면 '다른 댓글에 대한 답글(대댓글)'이 돼요
    # parent는 자기 자신(Comment)과 연결돼요 ('self')
    # 답글이 없을 수도 있어서 null=True, blank=True를 사용했어요
    # comment.replies로 대댓글들을 쉽게 가져올 수 있어요

    content = models.TextField()
    # 댓글 내용을 저장해요

    created_at = models.DateTimeField(auto_now_add=True)
    # 댓글이 처음 작성된 시간을 자동으로 저장해요
