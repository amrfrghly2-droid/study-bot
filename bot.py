import time
from datetime import datetime
import requests
import schedule
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = "8601463498:AAHIBbSsiU_HoSH7ecY1bYUV47kxL3CDyOw"
CHAT_ID = -1003936235079  # آيدي القناة الرسمي

# خادم وهمي بسيط لتشغيل السيرفر السحابي 24/7 دون توقف
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running 24/7 for 24h study camps!")

def run_web_server():
    server_address = ('', 10000)
    httpd = HTTPServer(server_address, SimpleHandler)
    httpd.serve_forever()

# تشغيل الخادم في الخلفية
Thread(target=run_web_server, daemon=True).start()

# دالة لإرسال الرسائل للقناة
def send_message(text, target_chat_id=CHAT_ID):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": target_chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print("خطأ في إرسال الرسالة:", e)

# دوال معسكرات المذاكرة والبريكات على مدار 24 ساعة
def session_1():
    send_message("🚨 **بدء المعسكر (1) - 3 ساعات مكثفة!** 📚🔥\n⏰ **الوقت:** من 08:00 صباحاً إلى 11:00 صباحاً.\n⚠️ الموبايل بعيد تماماً.. انطلقوا نحو حلم الطب! 🎯🩺")

def break_1():
    send_message("☕ **بريك (1) - 20 دقيقة!** 🌿✨\n⏰ من 11:00 إلى 11:20 صباحاً.\nقومي اشربي مية وريحي عيونك.. ربع ساعة ونرجع أقوى! ⏳💪")

def session_2():
    send_message("🚨 **بدء المعسكر (2) - 3 ساعات مكثفة!** 📚🔥\n⏰ **الوقت:** من 11:20 صباحاً إلى 02:20 ظهراً.\n⚠️ تركيز تام وممنوع أي مشتتات. استعينوا بالله! 🎯🩺")

def break_2():
    send_message("☕ **بريك (2) - 20 دقيقة!** 🌿✨\n⏰ من 02:20 إلى 02:40 ظهراً.\nاستراحة قصيرة ومفيدة لتجديد الطاقة. ⏳💪")

def session_3():
    send_message("🚨 **بدء المعسكر (3) - فترة العصر (3 ساعات)!** 📚🔥\n⏰ **الوقت:** من 02:40 ظهراً إلى 05:40 مسائاً.\n⚠️ وعزيمة العصر تهد الجبال.. شدوا حيلكم! 🎯🩺")

def break_3():
    send_message("☕ **بريك (3) - 20 دقيقة!** 🌿✨\n⏰ من 05:40 إلى 06:00 مسائاً.\nافصلي شوية وجهزي نفسك للمغرب. ⏳💪")

def session_4():
    send_message("🚨 **بدء المعسكر (4) - فترة المغرب (3 ساعات)!** 📚🔥\n⏰ **الوقت:** من 06:00 مسائاً إلى 09:00 مسائاً.\n⚠️ الساعات دي بتبارك اليوم كله.. استمروا! 🎯🩺")

def break_4():
    send_message("☕ **بريك (4) - 20 دقيقة!** 🌿✨\n⏰ من 09:00 إلى 09:20 مسائاً.\nريحوا عيونكم استعداداً لسهرة العشاء. ⏳💪")

def session_5():
    send_message("🚨 **بدء المعسكر (5) - فترة العشاء (3 ساعات)!** 📚🔥\n⏰ **الوقت:** من 09:20 مسائاً إلى 12:20 منتصف الليل.\n⚠️ الهمة العالية تصنع الأوائل.. انطلقوا! 🎯🩺")

def break_5():
    send_message("☕ **بريك (5) - 20 دقيقة!** 🌿✨\n⏰ من 12:20 إلى 12:40 صباحاً.\nاستراحة خفيفة لدخول الليل والهدوء. ⏳💪")

def session_6():
    send_message("🚨 **بدء المعسكر (6) - السهرة الليلية الأولى (3 ساعات)!** 🌙📚🔥\n⏰ **الوقت:** من 12:40 صباحاً إلى 03:40 فجراً.\n⚠️ سهر الليل وبطولات الصامتة.. هدوء تام وتركيز خارقة! 🎯🩺")

def break_6():
    send_message("☕ **بريك (6) - 20 دقيقة!** 🌿✨\n⏰ من 03:40 إلى 04:00 فجراً.\nقربنا على الفجر.. اشربي مشروب دافئ وركزي. ⏳💪")

def session_7():
    send_message("🚨 **بدء المعسكر (7) - سهرة الفجر العظيمة (3 ساعات)!** 🌅📚🔥\n⏰ **الوقت:** من 04:00 فجراً إلى 07:00 صباحاً.\n⚠️ بركة وقت الفجر لا تعوض.. اضربوا بقوة نحو القمة! 🎯🩺")

def break_final():
    send_message("☕ **البريك الختامي لليوم - 20 دقيقة!** 🌿✨\n⏰ من 07:00 إلى 07:20 صباحاً.\nعاش يا أبطال ويا عظيمات على ملحمة الـ 24 ساعة كاملة! بكرة يبدأ يوم جديد بإنجاز أكبر. تصبحون على ألف خير وثبات! ⏳💪")

# جدول الأوقات لمدار 24 ساعة كاملة بالدقيقة
schedule.every().day.at("08:00").do(session_1)
schedule.every().day.at("11:00").do(break_1)
schedule.every().day.at("11:20").do(session_2)
schedule.every().day.at("14:20").do(break_2)
schedule.every().day.at("14:40").do(session_3)
schedule.every().day.at("17:40").do(break_3)
schedule.every().day.at("18:00").do(session_4)
schedule.every().day.at("21:00").do(break_4)
schedule.every().day.at("21:20").do(session_5)
schedule.every().day.at("00:20").do(break_5)
schedule.every().day.at("00:40").do(session_6)
schedule.every().day.at("03:40").do(break_6)
schedule.every().day.at("04:00").do(session_7)
schedule.every().day.at("07:00").do(break_final)

print("🚀 بوت معسكرات الـ 24 ساعة يعمل بكفاءة تامة على مدار الساعة... 🩺")

while True:
    schedule.run_pending()
    time.sleep(1)
