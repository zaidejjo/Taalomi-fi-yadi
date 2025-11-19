from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FAQ
import os, json, cohere
from dotenv import load_dotenv

load_dotenv()


def chat_home(request):
    """عرض صفحة المحادثة مع قائمة الأسئلة المتكررة"""
    faqs = FAQ.objects.all()
    return render(request, 'ai_chat/chat.html', {'faqs': faqs})


@csrf_exempt
def chat_ai(request):
    """التعامل مع الرسائل من المستخدم باستخدام Cohere AI"""
    if request.method != "POST":
        return JsonResponse({"reply": "⚠️ طريقة الطلب غير مدعومة."}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
    except json.JSONDecodeError:
        return JsonResponse({"reply": "⚠️ تنسيق البيانات غير صحيح."}, status=400)

    if not user_message:
        return JsonResponse({"reply": "✏️ اكتب شيئًا من فضلك."}, status=400)

    # الردود الخاصة
    special_replies = {
        "من أنشأ الموقع": (
            "الموقع تم إنشاؤه وتطويره بواسطة **زيد علي يوسف عجو**، طالب في مدرسة الشجرة الثانوية للبنين، "
            "متخصص في تطوير مواقع الويب، ويحرص دائمًا على تقديم محتوى تعليمي مفيد وعملي للمستخدمين."
        ),
        "من هو زيد": (
            "زيد علي يوسف عجو هو مطور هذا الموقع، طالب في مدرسة الشجرة الثانوية للبنين، "
            "مهتم بتقنيات تطوير المواقع وتعلم الذكاء الاصطناعي. يمكنك التواصل معه عبر:\n"
            "Email: zaidejjo@gmail.com\n"
            "Instagram: https://www.instagram.com/zaidejjo\n"
            "X: https://x.com/zaid_ejjo\n"
            "Facebook: https://www.facebook.com/zaidejjo"
        ),
        "تواصل": (
            "للتواصل مع المنصة مباشرة، يمكنك إرسال بريد إلكتروني إلى:\n"
            "Email: taalomifiyadi@gmail.com\n"
            "وسيتم الرد بأسرع وقت ممكن."
        ),
    }

    user_lower = user_message.lower()
    for key, reply_text in special_replies.items():
        if key.lower() in user_lower:
            return JsonResponse({"reply": reply_text}, json_dumps_params={"ensure_ascii": False})

    # التحقق من وجود مفتاح API
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    if not COHERE_API_KEY:
        return JsonResponse({"reply": "⚠️ مفتاح Cohere API غير موجود."}, status=500)

    try:
        client = cohere.ClientV2(api_key=COHERE_API_KEY)
        response = client.chat(
            model="command-xlarge-nightly",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "أنت مساعد ذكي لمنصة تعليمية اسمها تعلمي في يدي. يجب أن تكون ودودًا، "
                        "تعليميًا، وتجيب بطريقة واضحة ومفيدة. "
                        "حاول تضمين معلومات عملية أو نصائح تعليمية عند الحاجة. "
                        "إذا سأل المستخدم عن المطور، أشر إلى أنه زيد علي يوسف عجو، "
                        "طالب في مدرسة الشجرة الثانوية للبنين، مطور مواقع ويب، "
                        "ويحب التعلم والمشاريع العملية."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )
        # استخراج الرد من API
        reply = response.message.content[0].text
    except Exception as e:
        reply = f"⚠️ حدث خطأ في التواصل مع API: {str(e)}"

    return JsonResponse({"reply": reply}, json_dumps_params={"ensure_ascii": False})
