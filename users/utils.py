from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles

def searchProfiles(request):
    search_guery = ''
    if request.GET.get('search_guery'):
        search_guery = request.GET.get('search_guery')

    skills = Skill.objects.filter(name__icontains=search_guery)
    profiles = Profile.objects.distinct().filter(
        Q(user__icontaints=search_guery) |
        Q(name__icontaints=search_guery) |
        Q(email__iconatints=search_guery) |
        Q(username=search_guery) |
        Q(skills__in=skills)
    )
    return profiles, search_guery
