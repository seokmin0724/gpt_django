from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm

# 게시글 목록 (최신순)
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})

# 게시글 상세 및 댓글/대댓글 작성 처리
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 부모 댓글(최상위 댓글) 최신순 정렬
    parent_comments = post.comments.filter(parent__isnull=True).order_by('-created_at')

    # 각 부모 댓글에 대한 대댓글도 최신순 정렬해서 딕셔너리 리스트로 저장
    comments_with_replies = []
    for parent in parent_comments:
        replies = parent.replies.all().order_by('-created_at')
        comments_with_replies.append({'comment': parent, 'replies': replies})

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post

            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment

            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        comment_form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments_with_replies': comments_with_replies,
        'comment_form': comment_form
    })

# 게시글 작성
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid(): # 유효성 검사
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

# 게시글 수정
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'post': post})

# 게시글 삭제
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

