from django.shortcuts import render ,get_object_or_404
# Create your views here.
from .models import Post, PostPoint
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import ListView


def post_list(request):
    object_list = Post.objects.all()
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

    return render(request, 'blog/post/list.html', {'page':page, 'posts': posts})



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
    return render(request, 'blog/post/detail.html', {'post': post_object,
                                                     'post_points': post_points})
