from django.shortcuts import render, get_object_or_404
from .models import Competition

def competition_list(request):
    competitions = Competition.objects.all()
    return render(request, 'competitions/competition_list.html', {'competitions': competitions})

def competition_detail(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    return render(request, 'competitions/competition_detail.html', {'competition': competition})
