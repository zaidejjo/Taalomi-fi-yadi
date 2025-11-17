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

    # الردود الخاصة
    special_replies = {
        "من أنشأ الموقع": (
            "الموقع تم إنشاؤه وتطويره بواسطة زيد علي عجو، "
            "مع كل البيانات والمحتوى المقدم من فريق المشروع."
        ),
        "من هو زيد": (
            "زيد علي عجو هو مطور هذا الموقع، ويمكنك التواصل معه من خلال:\n"
            "📧 zaidejjo@gmail.com\n"
            "📸 Instagram: https://www.instagram.com/zaidejjo\n"
            "🐦 X: https://x.com/zaid_ejjo\n"
            "📘 Facebook: https://www.facebook.com/zaidejjo"
        ),
        "تواصل": (
            "للتواصل مع المنصة، يمكنك إرسال بريد إلكتروني إلى:\n"
            "📧 taalomifiyadi@gmail.com"
        ),
    }

    user_lower = user_message.lower()
    for key, reply_text in special_replies.items():
        if key.lower() in user_lower:
            return JsonResponse({"reply": reply_text}, json_dumps_params={"ensure_ascii": False})

    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    if not COHERE_API_KEY:
        return JsonResponse({"reply": "مفتاح Cohere API غير موجود."}, status=500)

    try:
        client = cohere.ClientV2(api_key=COHERE_API_KEY)
        response = client.chat(
            model="command-xlarge-nightly",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي لمنصة تعليمية."},
                {"role": "user", "content": user_message}
            ]
        )
        # استخراج الرد الصحيح
        reply = response.message.content[0].text
    except Exception as e:
        reply = f"⚠️ حدث خطأ في التواصل مع API: {str(e)}"

    return JsonResponse({"reply": reply}, json_dumps_params={"ensure_ascii": False})
