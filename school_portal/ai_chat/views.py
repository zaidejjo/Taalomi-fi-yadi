from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FAQ
import os, json, cohere
from dotenv import load_dotenv

load_dotenv()


def chat_home(request):
    """
    عرض صفحة المحادثة مع قائمة الأسئلة المتكررة
    """
    faqs = FAQ.objects.all()
    return render(request, 'ai_chat/chat.html', {'faqs': faqs})


@csrf_exempt
def chat_ai(request):
    """
    التعامل مع الرسائل من المستخدم باستخدام Cohere AI
    مع الردود الذكية والروابط القابلة للنقر
    """
    if request.method != "POST":
        return JsonResponse({"reply": "⚠️ طريقة الطلب غير مدعومة."}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
    except json.JSONDecodeError:
        return JsonResponse({"reply": "⚠️ تنسيق البيانات غير صحيح."}, status=400)

    if not user_message:
        return JsonResponse({"reply": "✏️ اكتب شيئًا من فضلك."}, status=400)

    # الردود الخاصة HTML
    special_replies = {
        "من أنشأ الموقع": (
            "الموقع تم إنشاؤه وتطويره بواسطة <strong>زيد علي يوسف عجو</strong>، "
            "طالب في مدرسة الشجرة الثانوية للبنين ومتخصص في تطوير المواقع."
        ),
        "من هو زيد": (
            "زيد علي يوسف عجو هو مطور هذا الموقع، مهتم بتقنيات تطوير المواقع "
            "وتعلم الذكاء الاصطناعي.<br>"
            "تواصل معه عبر:<br>"
            "<a href='mailto:zaidejjo@gmail.com'>zaidejjo@gmail.com</a><br>"
            "<a href='https://www.instagram.com/zaidejjo' target='_blank'>Instagram</a><br>"
            "<a href='https://x.com/zaid_ejjo' target='_blank'>X</a><br>"
            "<a href='https://www.facebook.com/zaidejjo' target='_blank'>Facebook</a>"
        ),
        "تواصل": (
            "للتواصل مع المنصة مباشرة:<br>"
            "📧 <a href='mailto:taalomifiyadi@gmail.com'>taalomifiyadi@gmail.com</a>"
        ),
    }

    # الردود الخاصة أولًا
    user_lower = user_message.lower()
    for key, reply_text in special_replies.items():
        if key.lower() in user_lower:
            return JsonResponse({"reply": reply_text}, json_dumps_params={"ensure_ascii": False})

    # التحقق من مفتاح API
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    if not COHERE_API_KEY:
        return JsonResponse({"reply": "⚠️ مفتاح Cohere API غير موجود."}, status=500)

    try:
        client = cohere.ClientV2(api_key=COHERE_API_KEY)

        system_message = {
            "role": "system",
            "content": (
                "أنت مساعد ذكي لمنصة تعليمية اسمها 'تعلمي في يدي'. "
                "أجب فقط على السؤال المطروح بدقة وبشكل مختصر. "
                "لا تضف معلومات إضافية غير مطلوبة. "
                "إذا سأل المستخدم عن المطور، أشر فقط إلى زيد علي يوسف عجو، "
                "طالب في مدرسة الشجرة الثانوية للبنين، مطور ويب."
            )
        }

        response = client.chat(
            model="command-xlarge-nightly",
            messages=[system_message, {"role": "user", "content": user_message}],
            max_output_tokens=150,
            temperature=0.4
        )

        reply = response.message.content[0].text

    except Exception as e:
        reply = f"⚠️ حدث خطأ في التواصل مع API: {str(e)}"

    return JsonResponse({"reply": reply}, json_dumps_params={"ensure_ascii": False})
