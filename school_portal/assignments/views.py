from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Assignment, Submission, Quiz, QuizQuestion

def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignments/assignment_list.html', {'assignments': assignments})

def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    return render(request, 'assignments/assignment_detail.html', {'assignment': assignment})

def quiz_view(request, lesson_id):
    # مؤقتًا نعرض رسالة فقط
    return HttpResponse(f"صفحة الكويز للدرس رقم {lesson_id}")
