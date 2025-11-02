# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FAQ
import os
import json
import cohere
from dotenv import load_dotenv

load_dotenv()

def chat_home(request):
    """
    صفحة المحادثة الرئيسية
    """
    faqs = FAQ.objects.all()
    return render(request, 'ai_chat/chat.html', {'faqs': faqs})


@csrf_exempt
def chat_ai(request):
    """
    API endpoint للمحادثة مع AI
    """
    if request.method != "POST":
        return JsonResponse({"reply": "طريقة الطلب غير مدعومة."}, status=405)

    # قراءة البيانات المرسلة
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
    except json.JSONDecodeError:
        return JsonResponse({"reply": "تنسيق البيانات غير صحيح."}, status=400)

    if not user_message:
        return JsonResponse({"reply": "اكتب شيئًا من فضلك."}, status=400)

    # التحقق من مفتاح API
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    if not COHERE_API_KEY:
        return JsonResponse({"reply": "مفتاح Cohere API غير موجود."}, status=500)

    # محاولة الاتصال بـ Cohere
    try:
        client = cohere.Client(api_key=COHERE_API_KEY)

        # تمرير نص واحد فقط وليس مصفوفة
        response = client.chat(
            model="command-xlarge-nightly",  # النموذج الحديث
            message=user_message               # رسالة نصية واحدة
        )

        # استخراج الرد بطريقة آمنة
        if hasattr(response, "output_text"):
            reply = response.output_text
        elif hasattr(response, "text"):
            reply = response.text
        else:
            reply = "⚠️ لم يتمكن الذكاء الاصطناعي من إنشاء رد."

    except cohere.CohereAPIError as api_err:
        # الأخطاء الخاصة بـ API
        reply = f"⚠️ خطأ في API: {api_err.message}"
    except Exception as e:
        # أي خطأ عام
        reply = f"⚠️ حدث خطأ غير متوقع: {str(e)}"

    return JsonResponse({"reply": reply}, json_dumps_params={"ensure_ascii": False})
