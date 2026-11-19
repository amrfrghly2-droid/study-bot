import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from threading import Thread, Lock
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

TOKEN = os.getenv("BOT_TOKEN", "8601463498:AAHIBbSsiU_HoSH7ecY1bYUV47kxL3CDyOw")
CHAT_ID = int(os.getenv("CHAT_ID", "-1003936235079"))
CAIRO_TZ = ZoneInfo("Africa/Cairo")

sent_lock = Lock()
sent_slots = set()  # يمنع إرسال نفس الميعاد أكثر من مرة في نفس اليوم


# خادم ويب خفيف لإبقاء الخدمة حية على منصات الكلاود
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK - 24h Study Camp Bot is running on Cairo time.")

    def log_message(self, format, *args):
        return  # تقليل ضوضاء السجلات من طلبات الفحص الصحية


def run_web_server():
    port = int(os.getenv("PORT", "10000"))
    server_address = ("", port)
    httpd = HTTPServer(server_address, SimpleHandler)
    httpd.serve_forever()


Thread(target=run_web_server, daemon=True).start()


def send_telegram_message(text: str, chat_id: int = CHAT_ID) -> bool:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    now_str = datetime.now(CAIRO_TZ).strftime("%Y-%m-%d %H:%M:%S")
    try:
        resp = requests.post(url, json=payload, timeout=15)
        data = resp.json()
        if resp.status_code == 200 and data.get("ok"):
            print(f"[{now_str} Cairo] تم الإرسال بنجاح - message_id: {data['result']['message_id']}")
            return True
        else:
            print(f"[{now_str} Cairo] فشل الإرسال من تليجرام: {data}")
            return False
    except Exception as e:
        print(f"[{now_str} Cairo] خطأ شبكة أثناء الإرسال: {e}")
        return False


# الجدول الرسمي (HH:MM بتوقيت مصر Africa/Cairo)
SCHEDULE_ITEMS = [
    ("08:00", "🚨 <b>بدء المعسكر (1) - 3 ساعات مكثفة!</b> 📚🔥\n⏰ <b>الوقت:</b> من 08:00 صباحاً إلى 11:00 صباحاً.\n⚠️ الموبايل بعيد تماماً.. انطلقوا نحو حلم الطب! 🎯🩺"),
    ("11:00", "☕ <b>بريك (1) - 20 دقيقة!</b> 🌿✨\n⏰ من 11:00 إلى 11:20 صباحاً.\nقومي اشربي مية وريحي عيونك.. ربع ساعة ونرجع أقوى! ⏳💪"),
    ("11:20", "🚨 <b>بدء المعسكر (2) - 3 ساعات مكثفة!</b> 📚🔥\n⏰ <b>الوقت:</b> من 11:20 صباحاً إلى 02:20 ظهراً.\n⚠️ تركيز تام وممنوع أي مشتتات. استعينوا بالله! 🎯🩺"),
    ("14:20", "☕ <b>بريك (2) - 20 دقيقة!</b> 🌿✨\n⏰ من 02:20 إلى 02:40 ظهراً.\nاستراحة قصيرة ومفيدة لتجديد الطاقة. ⏳💪"),
    ("14:40", "🚨 <b>بدء المعسكر (3) - فترة العصر (3 ساعات)!</b> 📚🔥\n⏰ <b>الوقت:</b> من 02:40 ظهراً إلى 05:40 مسائاً.\n⚠️ وعزيمة العصر تهد الجبال.. شدوا حيلكم! 🎯🩺"),
    ("17:40", "☕ <b>بريك (3) - 20 دقيقة!</b> 🌿✨\n⏰ من 05:40 إلى 06:00 مسائاً.\nافصلي شوية وجهزي نفسك للمغرب. ⏳💪"),
    ("18:00", "🚨 <b>بدء المعسكر (4) - فترة المغرب (3 ساعات)!</b> 📚🔥\n⏰ <b>الوقت:</b> من 06:00 مسائاً إلى 09:00 مسائاً.\n⚠️ الساعات دي بتبارك اليوم كله.. استمروا! 🎯🩺"),
    ("21:00", "☕ <b>بريك (4) - 20 دقيقة!</b> 🌿✨\n⏰ من 09:00 إلى 09:20 مسائاً.\nريحوا عيونكم استعداداً لسهرة العشاء. ⏳💪"),
    ("21:20", "🚨 <b>بدء المعسكر (5) - فترة العشاء (3 ساعات)!</b> 📚🔥\n⏰ <b>الوقت:</b> من 09:20 مسائاً إلى 12:20 منتصف الليل.\n⚠️ الهمة العالية تصنع الأوائل.. انطلقوا! 🎯🩺"),
    ("00:20", "☕ <b>بريك (5) - 20 دقيقة!</b> 🌿✨\n⏰ من 12:20 إلى 12:40 صباحاً.\nاستراحة خفيفة لدخول الليل والهدوء. ⏳💪"),
    ("00:40", "🚨 <b>بدء المعسكر (6) - السهرة الليلية الأولى (3 ساعات)!</b> 🌙📚🔥\n⏰ <b>الوقت:</b> من 12:40 صباحاً إلى 03:40 فجراً.\n⚠️ سهر الليل وبطولات الصامتة.. هدوء تام وتركيز خارقة! 🎯🩺"),
    ("03:40", "☕ <b>بريك (6) - 20 دقيقة!</b> 🌿✨\n⏰ من 03:40 إلى 04:00 فجراً.\nقربنا على الفجر.. اشربي مشروب دافئ وركزي. ⏳💪"),
    ("04:00", "🚨 <b>بدء المعسكر (7) - سهرة الفجر العظيمة (3 ساعات)!</b> 🌅📚🔥\n⏰ <b>الوقت:</b> من 04:00 فجراً إلى 07:00 صباحاً.\n⚠️ بركة وقت الفجر لا تعوض.. اضربوا بقوة نحو القمة! 🎯🩺"),
    ("07:00", "☕ <b>البريك الختامي لليوم - 20 دقيقة!</b> 🌿✨\n⏰ من 07:00 إلى 07:20 صباحاً.\nعاش يا أبطال ويا عظيمات على ملحمة الـ 24 ساعة كاملة! بكرة يبدأ يوم جديد بإنجاز أكبر. تصبحون على ألف خير وثبات! ⏳💪"),
]


def scheduler_loop():
    now_cairo = datetime.now(CAIRO_TZ)
    print(f"🚀 البوت يعمل الآن بتوقيت القاهرة: {now_cairo.strftime('%Y-%m-%d %H:%M:%S')}")

    while True:
        now = datetime.now(CAIRO_TZ)
        current_hm = now.strftime("%H:%M")
        date_key = now.strftime("%Y-%m-%d")

        # تنظيف مفاتيح الأيام السابقة حتى لا تكبر الذاكرة
        stale_keys = [k for k in sent_slots if not k.startswith(date_key)]
        for k in stale_keys:
            sent_slots.discard(k)

        for target_hm, message_text in SCHEDULE_ITEMS:
            slot_key = f"{date_key}_{target_hm}"
            if current_hm == target_hm and slot_key not in sent_slots:
                with sent_lock:
                    if slot_key not in sent_slots:
                        sent_slots.add(slot_key)
                        send_telegram_message(message_text)

        time.sleep(1)


if __name__ == "__main__":
    scheduler_loop()
