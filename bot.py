import time
from datetime import datetime
import requests
import schedule
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = "8601463498:AAHIBbSsiU_HoSH7ecY1bYUV47kxL3CDyOw"
CHAT_ID = -1004477766854  # آيدي جروب المتابعة

# متغير لحفظ آخر رسالة تمت معالجتها عشان ما نكررش الرد
last_update_id = 0

# خادم وهمي بسيط لتشغيل السيرفر السحابي 24/7 دون توقف
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running 24/7!")

def run_web_server():
    server_address = ('', 10000)
    httpd = HTTPServer(server_address, SimpleHandler)
    httpd.serve_forever()

# تشغيل الخادم في الخلفية
Thread(target=run_web_server, daemon=True).start()

# دالة لإرسال الرسائل
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

# دالة فحص والرد الفوري على الرسائل الخاصة
def check_private_messages():
    global last_update_id
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=5"
    try:
        response = requests.get(url, timeout=10).json()
        if "result" in response and response["result"]:
            for update in response["result"]:
                last_update_id = update["update_id"]
                
                if "message" in update:
                    msg = update["message"]
                    chat_type = msg.get("chat", {}).get("type")
                    
                    if chat_type == "private":
                        chat_id = msg["chat"]["id"]
                        user_name = msg.get("from", {}).get("first_name", "يا دكتورة")
                        user_text = msg.get("text", "")
                        
                        print(f"تم استقبال رسالة خاصة من: {user_name} - النص: {user_text}")
                        
                        welcome_text = (
                            f"أهلاً بكِ يا {user_name} في بوت طريق القمة! 🩺✨\n\n"
                            "عالمك الخاص لتنظيم المذاكرة والمتابعة.\n"
                            "هذا البوت **خاص بتيم متابعة الدكتور عمر جمال** لمساعدة طلاب الثانوية العامة (دفعة 2027) على تنظيم معسكرات المذاكرة وتحقيق الحلم المنشود.\n\n"
                            "شدّي حيلك، اصبري على التعب، وكل لحظة سهر بتكتب بكرة بياض وجه في كلية الطب! 🎯💪"
                        )
                        
                        send_message(welcome_text, target_chat_id=chat_id)
                
    except Exception as e:
        print("خطأ في جلب الرسائل الخاصة:", e)

# معسكرات المذاكرة
def study_session_1():
    msg = (
        "🚨 **بدء معسكر المذاكرة الأول (3 ساعات مكثفة)!** 📚🔥\n"
        "⏰ **الوقت:** من الساعة 08:00 صباحاً وحتى 11:00 صباحاً.\n\n"
        "⚠️ **قاعدة ذهبية صارمة:**\n"
        "• اقفلي الموبايل خالص أو ارميه في أوضة تانية بعيد عن إيدك عشان أي مسكة ليه بتسحب طاقة تركيزك.\n"
        "• جهزي ميتك، كتابك، وسمّي الله.. الساعات دي بتبني مستقبلك واسمك قدام أهلك يوم النتيجة.\n\n"
        "💡 *«من سار على الدرب وصل، والتعب بيعدي وبتبقى حلاوة النجاح هي اللي بتنسي كل السهر.»*\n\n"
        "تركيز تام.. انطلقوا الآن! 🎯🩺"
    )
    send_message(msg)

def break_session_1():
    msg = (
        "☕ **وقت البريك الأول (ثلث ساعة - 20 دقيقة)!** 🌿✨\n"
        "⏰ **الوقت:** من 11:00 صباحاً إلى 11:20 صباحاً.\n\n"
        "عاش يا عظيمات، مجهود جبار في الـ 3 ساعات اللي فاتوا! قومي اشربي مية، ريحي عيونك، واتحركي شوية بعيد عن الشاشات عشان نرجع أقوى.\n"
        "قدامكم 20 دقيقة بريك وخليكم جاهزين! ⏳💪"
    )
    send_message(msg)

def study_session_2():
    msg = (
        "🚨 **بدء معسكر المذاكرة الثاني (3 ساعات مكثفة)!** 📚🔥\n"
        "⏰ **الوقت:** من الساعة 11:20 صباحاً وحتى 02:20 ظهراً.\n\n"
        "⚠️ **تنبيه عاجل:** الموبايل بعيد تماماً عن المكتب! ممنوع التمرير أو فتح السوشيال ميديا.\n"
        "استوعبوا الوجبة العلمية دي بكل تركيز، وافتكروا حلم كلية الطب اللي يستاهل كل تعب.\n"
        "💡 *«النجاح مش بيجي من تفوق مفاجئ، ده تراكم ساعات سهر وتعب مستمرة.»*\n\n"
        "استعينوا بالله وابدؤوا السيشن! 🎯🩺"
    )
    send_message(msg)

def break_session_2():
    msg = (
        "☕ **وقت البريك الثاني (ثلث ساعة - 20 دقيقة)!** 🌿✨\n"
        "⏰ **الوقت:** من 02:20 ظهراً إلى 02:40 ظهراً.\n\n"
        "استراحة قصيرة ومفيدة.. قومي غيري مكانك، افصلي شوية، وجهزي نفسك لفترة العصر.\n"
        "يلا اشربي مية وركزي في الراحة! ⏳💪"
    )
    send_message(msg)

def study_session_3():
    msg = (
        "🚨 **بدء معسكر المذاكرة الثالث - فترة العصر (3 ساعات)!** 📚🔥\n"
        "⏰ **الوقت:** من الساعة 03:00 عصراً وحتى 06:00 مسائاً.\n\n"
        "⚠️ **انتبهي:** ابعدي أي مشتتات أو رسايل تبررلك فتح الموبايل. التركيز هنا بيصنع الفارق الحقيقي في حصيلة اليوم.\n"
        "💡 *«كل خطوة تقربك للقمة هي ثمرة صبرك وإصرارك اليوم.»*\n\n"
        "انطلقوا يا بطلات! 🎯🩺"
    )
    send_message(msg)

def break_session_3():
    msg = (
        "☕ **وقت البريك الثالث (ثلث ساعة - 20 دقيقة)!** 🌿✨\n"
        "⏰ **الوقت:** من 06:00 مسائاً إلى 06:20 مسائاً.\n\n"
        "عاش يا بطلات، عديتوا نص اليوم بكل اقتدار! ريحوا عيونكم وافصلوا كويس عشان السهرة الليلية.\n"
        "قدامكم 20 دقيقة بريك! ⏳💪"
    )
    send_message(msg)

def study_session_4():
    msg = (
        "🚨 **بدء معسكر المذاكرة الرابع - السهرة الليلية (3 ساعات)!** 📚🔥\n"
        "⏰ **الوقت:** من الساعة 06:20 مسائاً وحتى 09:20 ليلاً.\n\n"
        "⚠️ **الضربة القاضية للكسل:** دي السهرة اللي تجيب الفارق.. اقفلي النت عن الموبايل واهزمي الإرهاق.\n"
        "💡 *«السهر في طلب العلم عبادة وطريق حقيقي للقمة.»*\n\n"
        "شدوا حيلكم يا دكاترة! 🎯🩺"
    )
    send_message(msg)

def break_session_4():
    msg = (
        "☕ **وقت البريك الأخير (استراحة الختام)!** 🌿✨\n"
        "⏰ **الوقت:** من 09:20 ليلاً إلى 09:40 ليلاً.\n\n"
        "عاش يا عظيمات على التزامكم اليوم كله! ريحوا وانهوا يومكم بكل راحة وطمأنينة وأنتو فخورين بانجازكم.\n"
        "تصبحوا على ألف خير وإنجاز! ⏳💪"
    )
    send_message(msg)

# جدول الأوقات
schedule.every().day.at("08:00").do(study_session_1)
schedule.every().day.at("11:00").do(break_session_1)
schedule.every().day.at("11:20").do(study_session_2)
schedule.every().day.at("14:20").do(break_session_2)
schedule.every().day.at("15:00").do(study_session_3)
schedule.every().day.at("18:00").do(break_session_3)
schedule.every().day.at("18:20").do(study_session_4)
schedule.every().day.at("21:20").do(break_session_4)

print("🚀 بوت معسكرات المذاكرة يعمل الآن 24/7 بكفاءة تامة... 🩺")

while True:
    schedule.run_pending()
    check_private_messages()
    time.sleep(1)
