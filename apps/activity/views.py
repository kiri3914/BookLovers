from django.shortcuts import render
from .models import Activity


def activity_feed(request):
    activity_list = Activity.objects.all().order_by('-id')[:10]
    return render(request, 'activity/activity_feed.html', {'activity_list': activity_list})

