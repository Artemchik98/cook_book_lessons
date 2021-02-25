from django.shortcuts import render ,get_object_or_404
# Create your views here.
from .models import Post, PostPoint,Comment
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
def post_list(request, tag_slug=None):
    object_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])



    paginator = Paginator(object_list, 3)  # По 3 статьи на каждой странице.
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        posts = paginator.page(paginator.num_pages)


    return render(request, 'blog/post/list.html', {'page':page,
                                                   'posts': posts,
                                                   'tag':tag})



class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'






def post_detail(request, year, month, day, post):
    post_object = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    post_points = PostPoint.objects.filter(post=post_object)
    # Список активных комментариев для этой статьи.
    comments = post_object.comment.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # Пользователь отправил комментарий.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в базе данных.
            cd = comment_form.cleaned_data
            new_comment = Comment(post=post_object, name=cd['name'], email=cd['email'], body=cd['comment'])
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post_object.tags.values_list('id', flat=True)
    # Формування списку схожих статей.
    similar_posts = Post.objects.filter(tags__in=post_tags_ids,status='published').exclude(id=post_object.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post_object,
                                                     'post_points': post_points,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts
                                                     })



def post_share(request, post_id):
    # Получение статьи по идентификатору.
    post = get_object_or_404(Post, id=post_id,status='published')
    sent = False
    if request.method == 'POST':
        # Форма была отправлена на сохранение.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Все поля формы прошли валидацию.
            cd = form.cleaned_data
            # Отправка электронной почты.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comment'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
            {'post': post, 'form': form, 'sent': sent})

