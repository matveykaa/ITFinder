from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

def paginateProjects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects

def searchProjects(request):
    search_guery = ''
    if request.GET.get('search_guery'):
        search_guery = request.GET.get('search_guery')

    tags = Tag.objects.filter(name__icontains=search_guery)
    projects = Project.objects.distinct().filter(
        Q(title__icontaints=search_guery) |
        Q(description__icontaints=search_guery) |
        Q(owner__name__iconatints=search_guery) |
        Q(tags__in=tags)
    )
    return projects, search_guery
