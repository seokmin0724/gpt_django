# posts/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm

# 게시글 목록
def post_list(request):
    posts = Post.objects.all().order_by('-created_at') # 모든 post객체를 (creat-at)기준으로 내림차순 정렬하여 가져옴
    return render(request, 'post_list.html', {'posts': posts})  # 'post_list.html' 템플릿에 posts 데이터를 넘겨 렌더링

# 게시글 상세 + 댓글 작성
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) # pk에 해당하는 Post 객체를 가져오고, 없으면 404 오류 반환
    comments = post.comments.all()  # 해당 Post의 모든 댓글 가져오기 (related_name='comments'인 경우)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)  # 댓글 작성 폼에서 전송된 데이터 처리
        if comment_form.is_valid():  # 폼 데이터를 기반으로 Comment 객체 생성 (저장 X)
            comment = comment_form.save(commit=False)   # 현재 Post와 댓글 연결
            comment.post = post
            comment.save() # 댓글 저장
            return redirect('post_detail', pk=pk) # 댓글 작성 후, 같은 게시글 상세 페이지로 리다이렉트
    else:
        comment_form = CommentForm()   # GET 요청일 경우, 비어 있는 댓글 작성 폼 생성

    # 'post_detail.html' 템플릿에 post, comments, comment_form 데이터 넘겨 렌더링
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

# 게시글 작성
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():   # 유효성 검사 통과 시, Post 객체 생성 및 저장
            post = form.save()
            return redirect('post_detail', pk=post.pk) # 작성한 게시글 상세 페이지로 이동
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})  # 'post_form.html' 템플릿에 form 데이터 넘겨 렌더링

# 게시글 수정
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)  # pk에 해당하는 Post 객체를 가져오고, 없으면 404 오류 반환
    if request.method == 'POST': # POST 요청일 때, 기존 post 데이터를 PostForm에 넣어 수정
        form = PostForm(request.POST, instance=post)
        if form.is_valid():  # 유효성 검사 통과 시, 수정 내용 저장
            form.save()
            return redirect('post_detail', pk=post.pk) # 수정한 게시글 상세 페이지로 이동
    else:
        # GET 요청일 때, 기존 post 데이터를 포함한 PostForm 생성
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})

# 게시글 삭제
def post_delete(request, pk): # 삭제할 Post 객체 가져오기, 없으면 404 오류 반환
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':  # POST 요청일 때, post 삭제
        post.delete()  # 삭제 후 게시글 목록 페이지로 이동
        return redirect('post_list')
    # GET 요청일 때, 삭제 확인 페이지 렌더링
    return render(request, 'post_confirm_delete.html', {'post': post})