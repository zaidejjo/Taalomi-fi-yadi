from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Transfer

def transfer_list(request):
    transfers = Transfer.objects.all()
    return render(request, 'transfers/transfer_list.html', {'transfers': transfers})

def request_transfer(request):
    return HttpResponse("صفحة طلب انتقال (لاحقًا نعملها فورم)")

def approve_transfer(request, transfer_id):
    transfer = get_object_or_404(Transfer, id=transfer_id)
    transfer.status = 'approved'
    transfer.save()
    return HttpResponse(f"تمت الموافقة على انتقال الطالب {transfer.student}")
