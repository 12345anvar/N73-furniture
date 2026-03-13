from django.views.generic import ListView, DetailView

from blogs.models import Blog, BlogStatus, Category, Tag


class BlogListView(ListView):
    model = Blog
    template_name = 'blogs/blogs-list.html'
    context_object_name = 'blogs'
    paginate_by = 6

    def get_queryset(self):
        blogs = Blog.objects.filter(status=BlogStatus.PUBLISHED).order_by('-id')

        categories = self.request.GET.getlist('cat')
        tags = self.request.GET.getlist('tag')

        categories_id_list = []
        tags_id_list = []

        if categories:
            categories_id_list = list(map(int, categories[0].split(',')))

        if tags:
            tags_id_list = list(map(int, tags[0].split(',')))

        if categories_id_list:
            blogs = blogs.filter(categories__id__in=categories_id_list)
        if tags_id_list:
            blogs = blogs.filter(tags__id__in=tags_id_list)
        return blogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(parent=None).order_by('-id')
        context["tags"] = Tag.objects.all().order_by('-id')
        context["recent_posts"] = Blog.objects.order_by('-created_at')[:2]
        return context

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogs/blog-detail.html'
    context_object_name = 'blog'