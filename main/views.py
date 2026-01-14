from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import EmailMessage

import json
import requests

from .models import Lead


def home(request):
    return redirect("/")

@csrf_exempt
@require_POST
def lead_capture(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            name = data.get("name")
            customer_type = data.get("customer_type")
            email = data.get("order")
            order = data.get("order")
            order_type = data.get("order_type")
            governorate = data.get("governorate")
            # 1. Save to DB
            Lead.objects.create(
                name=name,
                customer_type=customer_type,
                email=email,
                order=order,
                order_type=order_type,
                governorate=governorate,
                created_at=timezone.now(),
                state="Lead"
            )
    
            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=405)


@login_required
def show_leads(request):
    leads = Lead.objects.all()
    
    context = {
        "leads": leads
    }

    return render(request, "leads.html", context)

@login_required
def delete_lead(request, id):
    lead = Lead.objects.get(id=id)
    lead.delete()
    return redirect("/")

@login_required
def update_state(request, id, status):
    lead = Lead.objects.get(id=id)
    lead.state = status
    lead.save()
    return redirect("/")

def reset(request):
    if request.GET.get("token") == "secret123":
        return JsonResponse({"status": "success", "message": "Absences reset"})
    return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)
