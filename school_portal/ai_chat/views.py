from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FAQ
import requests, json, os
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# ===================================
# عرض صفحة الشات مع قائمة FAQ
# ===================================
def chat_home(request):
    faqs = FAQ.objects.all()
    return render(request, 'ai_chat/chat.html', {'faqs': faqs})

# ===================================
# API endpoint للشات الذكي عبر OpenRouter
# ===================================
@csrf_exempt
def chat_ai(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
        if not user_message:
            return JsonResponse({"reply": "اكتب شيئًا من فضلك"})

        # المفتاح من OpenRouter
        OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        if not OPENROUTER_API_KEY:
            return JsonResponse({"reply": "مفتاح OpenRouter API غير موجود!"}, status=500)

        API_URL = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://your-site.com",  # اختياري
            "X-Title": "School Portal Chat"           # اختياري
        }
        payload = {
            "model": "openai/gpt-4o",  # يمكنك تغييره لأي نموذج مدعوم
            "messages": [{"role": "user", "content": user_message}]
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as http_err:
            reply = f"خطأ HTTP: {response.status_code} - {response.text}"
        except Exception as e:
            reply = f"حدث خطأ غير متوقع: {str(e)}"

        return JsonResponse({"reply": reply})

    return JsonResponse({"reply": "طريقة الطلب غير مدعومة"}, status=400)
