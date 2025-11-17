from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FAQ
import os, json, cohere
from dotenv import load_dotenv

load_dotenv()

def chat_home(request):
    faqs = FAQ.objects.all()
    return render(request, 'ai_chat/chat.html', {'faqs': faqs})

@csrf_exempt
def chat_ai(request):
    if request.method != "POST":
        return JsonResponse({"reply": "طريقة الطلب غير مدعومة."}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
    except json.JSONDecodeError:
        return JsonResponse({"reply": "تنسيق البيانات غير صحيح."}, status=400)

    if not user_message:
        return JsonResponse({"reply": "اكتب شيئًا من فضلك."}, status=400)

    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    if not COHERE_API_KEY:
        return JsonResponse({"reply": "مفتاح Cohere API غير موجود."}, status=500)

    try:
        client = cohere.Client(api_key=COHERE_API_KEY)
        response = client.chat(
            model="command-xlarge-nightly",
            message=user_message
        )
        reply = getattr(response, "output_text", getattr(response, "text", "⚠️ لم يتمكن الذكاء الاصطناعي من الرد."))
    except Exception as e:
        reply = f"⚠️ حدث خطأ في التواصل مع API: {str(e)}"

    return JsonResponse({"reply": reply}, json_dumps_params={"ensure_ascii": False})
