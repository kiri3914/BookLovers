from django.shortcuts import render
from .models import Activity


def activity_feed(request):
    # Получите список активностей, например, последние 10 активностей
    activity_list = Activity.objects.all().order_by('-id')[:10]
    return render(request, 'activity_feed.html', {'activity_list': activity_list})
