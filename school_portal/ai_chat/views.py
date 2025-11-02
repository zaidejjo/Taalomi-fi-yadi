from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FAQ
import requests, json, os
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# ===================================
# عرض صفحة الدردشة مع الأسئلة الشائعة
# ===================================
def chat_home(request):
    faqs = FAQ.objects.all()
    return render(request, 'ai_chat/chat.html', {'faqs': faqs})


# ===================================
# API endpoint للتحدث مع الذكاء الاصطناعي عبر Hugging Face
# ===================================
@csrf_exempt
def chat_ai(request):
    if request.method == "POST":
        # قراءة الرسالة القادمة من المستخدم
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()
        except json.JSONDecodeError:
            return JsonResponse({"reply": "تنسيق البيانات غير صحيح."}, status=400)

        if not user_message:
            return JsonResponse({"reply": "اكتب شيئًا من فضلك."}, status=400)

        # جلب مفتاح Hugging Face من .env
        HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
        if not HUGGINGFACE_API_KEY:
            return JsonResponse({"reply": "مفتاح Hugging Face غير موجود في .env"}, status=500)

        # عنوان الـ API ونموذج اللغة
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral‑7B‑Instruct‑v0.2"
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {"inputs": user_message}

        # إرسال الطلب إلى API
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()

            # استخراج الرد الصحيح من النتيجة
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                reply = result[0]["generated_text"]
            elif isinstance(result, dict) and "error" in result:
                reply = f"حدث خطأ من API: {result['error']}"
            else:
                reply = "لم يتمكن النموذج من توليد رد مفهوم."
        except requests.exceptions.HTTPError:
            reply = f"خطأ HTTP: {response.status_code} - {response.text}"
        except Exception as e:
            reply = f"حدث خطأ: {str(e)}"

        # إرجاع الرد بصيغة JSON
        return JsonResponse({"reply": reply}, json_dumps_params={"ensure_ascii": False})

    # إذا لم تكن الطريقة POST
    return JsonResponse({"reply": "طريقة الطلب غير مدعومة."}, status=405)
