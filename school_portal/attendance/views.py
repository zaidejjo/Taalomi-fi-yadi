from django.shortcuts import render
from django.http import HttpResponse
from .models import Absence

def absence_list(request):
    absences = Absence.objects.all()
    return render(request, 'attendance/absence_list.html', {'absences': absences})

def add_absence(request):
    return HttpResponse("صفحة إضافة غياب")
