from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm

# 글 목록 보기 (최신 글이 위에 오도록 정렬)
def post_list(request):
    # 글(Post)들을 모두 가져오고, 작성된 시간을 기준으로 가장 최근 글이 먼저 나오게 정렬
    posts = Post.objects.all().order_by('-created_at')
    # 'post_list.html'이라는 화면(페이지)에 글 목록을 보여주기
    return render(request, 'post_list.html', {'posts': posts})

# 글 자세히 보기 + 댓글과 대댓글(답글) 달기
def post_detail(request, pk):
    # 글 번호(pk)를 보고 글이 있는지 찾고, 없으면 에러 보여주기
    post = get_object_or_404(Post, pk=pk)

    # 부모 댓글(처음 달린 댓글)만 가져오고, 최신순으로 정렬
    parent_comments = post.comments.filter(parent__isnull=True).order_by('-created_at')

    # 부모 댓글마다 답글(대댓글)도 가져와서 함께 저장하기
    comments_with_replies = []
    for parent in parent_comments:
        # 대댓글도 최신순으로 정렬해서
        replies = parent.replies.all().order_by('-created_at')
        # 딕셔너리에 넣어서 리스트에 추가하기
        comments_with_replies.append({'comment': parent, 'replies': replies})

    # 댓글을 새로 쓰는 경우 (POST 방식으로 보내졌을 때)
    if request.method == 'POST':
        # 댓글 폼에 적힌 내용을 가져옴
        comment_form = CommentForm(request.POST)
        # 폼이 제대로 작성되었는지 확인
        if comment_form.is_valid():
            # 저장은 잠깐 미루고 comment 변수에 담기
            comment = comment_form.save(commit=False)
            # 이 댓글이 어떤 글에 달린 건지 연결하기
            comment.post = post

            # 부모 댓글 ID가 있는지 확인 (대댓글인지 확인)
            parent_id = request.POST.get('parent_id')
            if parent_id:
                # 부모 댓글을 찾아서 연결하기 (대댓글로 설정)
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment

            # 댓글 저장하기
            comment.save()
            # 다시 글 자세히 보기 페이지로 이동
            return redirect('post_detail', pk=pk)
    else:
        # GET 방식이면 빈 댓글 폼을 보여줌
        comment_form = CommentForm()

    # 글, 댓글, 댓글 폼을 함께 화면에 보여주기
    return render(request, 'post_detail.html', {
        'post': post,
        'comments_with_replies': comments_with_replies,
        'comment_form': comment_form
    })

# 새 글 쓰기
def post_create(request):
    if request.method == 'POST':
        # 사용자가 보낸 글 폼을 받음
        form = PostForm(request.POST)
        # 글 내용이 잘 작성되었는지 확인
        if form.is_valid():
            # 글 저장하기
            form.save()
            # 글 목록 페이지로 이동
            return redirect('post_list')
    else:
        # 글을 처음 쓸 때는 빈 폼을 보여줌
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

# 글 수정하기
def post_edit(request, pk):
    # 글 번호(pk)로 글을 찾아옴
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # 사용자가 수정한 내용을 받아서 저장
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            # 글 상세 페이지로 이동
            return redirect('post_detail', pk=post.pk)
    else:
        # 수정하기 전에는 원래 글 내용을 보여줌
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'post': post})

# 글 삭제하기
def post_delete(request, pk):
    # 글 번호로 글을 찾아옴
    post = get_object_or_404(Post, pk=pk)
    # 글을 삭제함
    post.delete()
    # 글 목록 페이지로 이동
    return redirect('post_list')

