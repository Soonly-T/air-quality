import os
import telebot
import datetime
import time
import requests as req
import json
from textwrap import dedent

API_KEY='''88e45ac1-6083-478d-bac0-6523f4bc4c76'''
# Function to print the chat ID of the bot
aqius_prior = 0
labels_dir='./labels'
image_files = []

# Loop through the files in the folder
for file_name in os.listdir(labels_dir):
    if file_name.endswith(".png"):  # Check if it's a PNG file
        image_files.append(os.path.join(labels_dir, file_name))  # Add the full path to the list


def get_phnom_penh_aq():
    phnom_penh_aq=(req.get(f"http://api.airvisual.com/v2/city?city=Phnom Penh&state=Phnom Penh&country=Cambodia&key={API_KEY}").json())

    aqius=phnom_penh_aq["data"]["current"]["pollution"]["aqius"]
    mainus=phnom_penh_aq["data"]["current"]["pollution"]["mainus"]
    return aqius,mainus

# Bot configuration
BOT_TOKEN = "8020379908:AAE5oD5MS73BnjcMKd2wSQrj34drgbo6w4s"
CHAT_ID = "-1002684296791"

# # URL to get updates
# url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

# # Make the request to Telegram API
# response = req.get(url)

# # Parse the JSON response
# if response.status_code == 200:  # Ensure the request was successful
#     updates = response.json()
#     print("Updates:", updates)
    
#     # Extract chat IDs from the updates
#     if "result" in updates:
#         for update in updates["result"]:
#             if "message" in update:
#                 chat_id = update["message"]["chat"]["id"]
#                 chat_type = update["message"]["chat"]["type"]
#                 chat_title = update["message"]["chat"].get("title", "Private Chat")
#                 print(f"Chat ID: {chat_id}, Type: {chat_type}, Title: {chat_title}")
# else:
#     print(f"Failed to fetch updates. Error code: {response.status_code}")

# Define weekdays and weekends
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday"]
weekends = ["Friday", "Saturday", "Sunday"]

# Initialize the bot
intell1slt_bot = telebot.TeleBot(BOT_TOKEN)
intell1slt_bot.send_message(chat_id=CHAT_ID, text="intell1slt_bot is now online.")

def morning_message_en(aqius, mainus):
    verdict, advice = "", ""
    if 0 <= aqius <= 50:
        verdict = "good"
        advice = "🌞 Go outside, breathe some of that fresh air and enjoy this wonderful day."
    elif 51 <= aqius <= 100:
        verdict = "moderate"
        advice = "😷 It's fine to go outside but make sure to keep updated with us for the latest air quality news. Also, while not necessary, wear or bring a mask just in case."
    elif 101 <= aqius <= 150:
        verdict = "unhealthy for sensitive groups"
        advice = "⚠️ If you're part of a sensitive group, such as children, the elderly, or those with respiratory issues, minimize prolonged outdoor activities and consider wearing a mask if necessary."
    elif 151 <= aqius <= 200:
        verdict = "unhealthy"
        advice = "🚫 Limit outdoor activities to a minimum. Stay indoors as much as possible, and use air purifiers if available. Everyone, not just sensitive groups, should take precautions."
    elif 201 <= aqius <= 300:
        verdict = "very unhealthy"
        advice = "❗ The air quality poses a serious health risk to everyone. Avoid going outdoors unless absolutely necessary, and wear a high-quality mask if you need to step outside. Follow health advisories closely."
    elif aqius > 300:
        verdict = "hazardous"
        advice = "🚨 Emergency conditions! Stay indoors with windows and doors shut. Avoid physical exertion, and follow any official instructions. If available, use air purifiers to improve indoor air quality."
    else:
        verdict = "invalid AQI value"
        advice = "❓ Please provide a valid AQI value to receive air quality advice."
    return (
        f'''
🌅 Good morning, ladies and gentlemen. I hope you have had a restful sleep and are eager to begin the new day. The air today is at a **{aqius}**, which means it's **{verdict}**. {advice}
'''
    )

def morning_message_kh(aqius, mainus):
    verdict, advice = "", ""
    if 0 <= aqius <= 50:
        verdict = "ល្អ"
        advice = "🌞 ចេញក្រៅដោយមិនមានការព្រួយបារម្ភ រីករាយជាមួយខ្យល់បរិសុទ្ធ ហើយរីករាយជាមួយថ្ងៃដ៏អស្ចារ្យនេះ។"
    elif 51 <= aqius <= 100:
        verdict = "មធ្យម"
        advice = "😷 អាចចេញក្រៅបាន ប៉ុន្តែសូមតាមដានព័ត៌មានថ្មីៗអំពីគុណភាពខ្យល់ពីយើង។ អ្នកក៏អាចពាក់ ឬយកម៉ាស់តាមផង ដើម្បីការពារសុខភាព។"
    elif 101 <= aqius <= 150:
        verdict = "មិនល្អសម្រាប់ក្រុមអ្នកងាយនឹងទទួលផលប៉ះពាល់"
        advice = "⚠️ ប្រសិនបើអ្នកជាក្រុមអ្នកងាយនឹងទទួលផលប៉ះពាល់ ដូចជា កុមារ អ្នកចាស់ ឬអ្នកមានបញ្ហាសុខភាពផ្នែកផ្លូវដង្ហើម សូមកំុការចេញក្រៅច្រើន។ គិតពី​ការពាក់ម៉ាស់ផងប្រសិនបើចាំបាច់។"
    elif 151 <= aqius <= 200:
        verdict = "មិនល្អ"
        advice = "🚫 កាត់បន្ថយសកម្មភាពខាងក្រៅ​ គួរប្រើប្រាស់ម៉ាសុីនខ្យល់បរិសុទ្ធ មនុស្សគ្រប់ក្រុមគួរមានការប្រុងប្រយ័ត្ន។"
    elif 201 <= aqius <= 300:
        verdict = "អាក្រក់ខ្លាំង"
        advice = "❗ គុណភាពខ្យល់ផ្តល់នូវហានិភ័យដល់សុខភាពសម្រាប់អ្នកគ្រប់គ្នា កុំចេញក្រៅលើកលែងតែមានភាពចាំបាច់ ហើយគួរពាក់ម៉ាស់ដែលមានគុណភាពខ្ពស់។"
    elif aqius > 300:
        verdict = "គ្រាអាសន្ន"
        advice = "🚨 ស្ថានភាពអាសន្ន! សូមនៅក្នុងផ្ទះ បិទបង្អួចនិងទ្វារឲ្យជិត​ និង សូមប្រើប្រាស់ម៉ាសុីនខ្យល់បរិសុទ្ធ។"
    return (
        f'''
🌅 អរុណសួស្តី លោកនិងលោកស្រី ខ្ញុំសូមសង្ឃឹមថាអ្នកមានការគេងសំរានជ្រាលជ្រៅ ហើយត្រៀមខ្លួនដើម្បីចាប់ផ្តើមថ្ងៃថ្មី។ ខ្យល់សព្វថ្ងៃនេះមានពិន្ទុ **{aqius}** ដែលមានន័យថា **{verdict}**។ **{advice}**
'''
    )

def morning_message_jp(aqius, mainus):
    verdict, advice = "", ""
    if 0 <= aqius <= 50:
        verdict = "良い (Good)"
        advice = "🌞 外に出て、新鮮な空気を吸い、この素晴らしい日を楽しみましょう！"
    elif 51 <= aqius <= 100:
        verdict = "普通 (Moderate)"
        advice = "😷 外に出ても大丈夫ですが、最新の空気質情報をチェックするようにしてください。必要ではありませんが、念のためにマスクを持参または着用してください。"
    elif 101 <= aqius <= 150:
        verdict = "敏感な人にとっては不健康 (Unhealthy for Sensitive Groups)"
        advice = "⚠️ 子供、高齢者、または呼吸器系の問題を抱える敏感なグループに属している場合は、長時間の屋外活動を控え、必要に応じてマスクを着用してください。"
    elif 151 <= aqius <= 200:
        verdict = "不健康 (Unhealthy)"
        advice = "🚫 屋外活動を最小限に抑え、可能であれば室内にいるようにしてください。また、空気清浄機を使用すると良いでしょう。全員が予防措置を講じる必要があります。"
    elif 201 <= aqius <= 300:
        verdict = "非常に不健康 (Very Unhealthy)"
        advice = "❗ 空気質が健康に深刻なリスクをもたらします。絶対に必要でない限り外に出ないようにし、外出する場合は高性能のマスクを着用してください。公的な健康指導に従ってください。"
    elif aqius > 300:
        verdict = "危険 (Hazardous)"
        advice = "🚨 非常事態です！屋内に留まり、窓とドアをしっかりと閉めてください。身体を動かさないようにし、公式の指示に従ってください。空気清浄機があれば使用してください。"
    else:
        verdict = "無効なAQI値"
        advice = "❓ 有効なAQI値を入力してください。"
    return (
        f'''
🌅 おはようございます、みなさん！昨晩はぐっすり眠れましたか？今日の空気の指数 (AQI) は **{aqius}** で、**「{verdict}」**の状態です。**{advice}**
    '''
    )

def morning_message_de(aqius, mainus):
    verdict, advice = "", ""
    if 0 <= aqius <= 50:
        verdict = "Gut (Good)"
        advice = "🌞 Gehen Sie nach draußen, atmen Sie die frische Luft ein und genießen Sie diesen wunderbaren Tag!"
    elif 51 <= aqius <= 100:
        verdict = "Mäßig (Moderate)"
        advice = "😷 Es ist in Ordnung, nach draußen zu gehen, aber halten Sie sich über die neuesten Nachrichten zur Luftqualität auf dem Laufenden. Auch wenn es nicht unbedingt erforderlich ist, nehmen oder tragen Sie sicherheitshalber eine Maske."
    elif 101 <= aqius <= 150:
        verdict = "Ungesund für empfindliche Gruppen (Unhealthy for Sensitive Groups)"
        advice = "⚠️ Wenn Sie zu einer empfindlichen Gruppe gehören, wie z. B. Kinder, ältere Menschen oder Personen mit Atemwegsproblemen, sollten Sie längere Aufenthalte im Freien vermeiden und bei Bedarf eine Maske tragen."
    elif 151 <= aqius <= 200:
        verdict = "Ungesund (Unhealthy)"
        advice = "🚫 Reduzieren Sie Aktivitäten im Freien auf ein Minimum. Bleiben Sie möglichst in Innenräumen und verwenden Sie, wenn verfügbar, Luftreiniger. Nicht nur empfindliche Gruppen sollten Vorsichtsmaßnahmen treffen, sondern alle."
    elif 201 <= aqius <= 300:
        verdict = "Sehr ungesund (Very Unhealthy)"
        advice = "❗ Die Luftqualität stellt ein ernstes Gesundheitsrisiko für alle dar. Vermeiden Sie den Aufenthalt im Freien, es sei denn, es ist absolut notwendig. Tragen Sie eine hochwertige Maske, wenn Sie nach draußen gehen müssen. Folgen Sie den Gesundheitsempfehlungen."
    elif aqius > 300:
        verdict = "Gefährlich (Hazardous)"
        advice = "🚨 Notfallbedingungen! Bleiben Sie in Innenräumen und schließen Sie Fenster und Türen. Vermeiden Sie körperliche Anstrengung und folgen Sie offiziellen Anweisungen. Verwenden Sie, wenn möglich, Luftreiniger."
    else:
        verdict = "Ungültiger AQI-Wert"
        advice = "❓ Bitte geben Sie einen gültigen AQI-Wert ein."
    return (
        f'''
🌅 Guten Morgen, meine Damen und Herren. Ich hoffe, Sie hatten einen erholsamen Schlaf und sind bereit, den neuen Tag zu beginnen. Die Luft heute hat einen AQI von {aqius}, was bedeutet, dass sie **{verdict}** ist. **{advice}**
'''
    )


def signoff_en():
    return(
f''' 
🌙 It's currently 21:00 and it's time for me to sign off. 💤 I will see you again tomorrow at 6 onwards to give you more updates on the air quality. 🌍 This has been intell1slt_bot at your service. 🌟 Good night! 🌌
''')

def signoff_kh():
    return(
f''' 
🌙 បច្ចុប្បន្ននេះម៉ោង 21:00 ហើយបានដល់ពេលដែលខ្ញុំត្រូវបញ្ចប់សេវាកម្មថ្ងៃនេះ។ 💤 ខ្ញុំនឹងជួបអ្នកវិញនៅថ្ងៃស្អែកចាប់ពីម៉ោង 6 ដើម្បីផ្តល់ព័ត៌មានថ្មីៗអំពីគុណភាពខ្យល់។ 🌍 នេះគឺជា​ intell1slt_bot ដែលបានបម្រើសេវាកម្មសម្រាប់លោកអ្នក។ 🌟 សុបិន្តល្អ! 🌌
''')

def signoff_jp():
    return(
f''' 
🌙 こんばんは、みなさん！今は21:00になりましたので、今日はこれでおやすみします。 💤 明日の朝6時から、また空気の質に関する情報をお届けします。 🌍 これまでお付き合いいただきありがとうございました。intell1slt_botより、良い夜をお過ごしください。 🌟 おやすみなさい！ 🌌
''')

def signoff_de():
    return(
f''' 
🌙 Es ist jetzt 21:00 Uhr und Zeit für mich, mich für heute zu verabschieden. 💤 Ich bin morgen ab 6 Uhr wieder da, um Ihnen weitere Updates zur Luftqualität zu geben. 🌍 Dies war intell1slt_bot, zu Ihren Diensten. 🌟 Gute Nacht! 🌌
''')




def update_en(aqius, mainus, aqius_prior, mainus_prior, hour, minute, change):
    minute = f"{int(minute):02}"  # Ensure minute is always 2 digits
    verdict, advice = "", ""
    if 0 <= aqius <= 50:
        verdict = "good"
        advice = "🌞 Go outside, breathe some of that fresh air and enjoy this wonderful day."
    elif 51 <= aqius <= 100:
        verdict = "moderate"
        advice = "😷 It's fine to go outside but make sure to keep updated with us for the latest air quality news. Also, while not necessary, wear or bring a mask just in case."
    elif 101 <= aqius <= 150:
        verdict = "unhealthy for sensitive groups"
        advice = "⚠️ If you're part of a sensitive group, such as children, the elderly, or those with respiratory issues, minimize prolonged outdoor activities and consider wearing a mask if necessary."
    elif 151 <= aqius <= 200:
        verdict = "unhealthy"
        advice = "🚫 Limit outdoor activities to a minimum. Stay indoors as much as possible, and use air purifiers if available. Everyone, not just sensitive groups, should take precautions."
    elif 201 <= aqius <= 300:
        verdict = "very unhealthy"
        advice = "❗ The air quality poses a serious health risk to everyone. Avoid going outdoors unless absolutely necessary, and wear a high-quality mask if you need to step outside. Follow health advisories closely."
    elif aqius > 300:
        verdict = "hazardous"
        advice = "🚨 Emergency conditions! Stay indoors with windows and doors shut. Avoid physical exertion, and follow any official instructions. If available, use air purifiers to improve indoor air quality."
    else:
        verdict = "invalid AQI value"
        advice = "❓ Please provide a valid AQI value to receive air quality advice."
    
    if (change[0] != 'stagnant') and (change[1] != "samecat"):
        return f'''
Currently, it is {hour}:{minute} with an update to the air quality. The air quality has **{change[0]}** from **{aqius_prior} ({change[1]})** to **{aqius} ({change[2]})**. {advice}
        '''
    elif (change[0] != 'stagnant'):
        return f'''
Currently, it is {hour}:{minute} with an update to the air quality. The air quality has **{change[0]}** from **{aqius_prior}** to **{aqius}** which is **{verdict}**. {advice}
        '''
    else:
        return f'''
Currently, it is {hour}:{minute} with an update to the air quality. The air quality is still **{verdict}** with an AQI score of **{aqius}**. {advice}
        '''


def update_kh(aqius, mainus, aqius_prior, mainus_prior, hour, minute, change):
    minute = f"{int(minute):02}"  # Ensure minute is always 2 digits
    verdict, advice = "", ""
    if 0 <= aqius <= 50:
        verdict = "ល្អ"
        advice = "🌞 ចេញក្រៅដោយមិនមានការព្រួយបារម្ភ រីករាយជាមួយខ្យល់បរិសុទ្ធ ហើយរីករាយជាមួយថ្ងៃដ៏អស្ចារ្យនេះ។"
    elif 51 <= aqius <= 100:
        verdict = "មធ្យម"
        advice = "😷 អាចចេញក្រៅបាន ប៉ុន្តែសូមតាមដានព័ត៌មានថ្មីៗអំពីគុណភាពខ្យល់ពីយើង។ អ្នកក៏អាចពាក់ ឬយកម៉ាស់តាមផង ដើម្បីការពារសុខភាព។"
    elif 101 <= aqius <= 150:
        verdict = "មិនល្អសម្រាប់ក្រុមអ្នកងាយនឹងទទួលផលប៉ះពាល់"
        advice = "⚠️ ប្រសិនបើអ្នកជាក្រុមអ្នកងាយនឹងទទួលផលប៉ះពាល់ ដូចជា កុមារ អ្នកចាស់ ឬអ្នកមានបញ្ហាសុខភាពផ្នែកផ្លូវដង្ហើម សូមកំុការចេញក្រៅច្រើន។ គិតពី​ការពាក់ម៉ាស់ផងប្រសិនបើចាំបាច់។"
    elif 151 <= aqius <= 200:
        verdict = "មិនល្អ"
        advice = "🚫 កាត់បន្ថយសកម្មភាពខាងក្រៅ​ គួរប្រើប្រាស់ម៉ាសុីនខ្យល់បរិសុទ្ធ មនុស្សគ្រប់ក្រុមគួរមានការប្រុងប្រយ័ត្ន។"
    elif 201 <= aqius <= 300:
        verdict = "អាក្រក់ខ្លាំង"
        advice = "❗ គុណភាពខ្យល់ផ្តល់នូវហានិភ័យដល់សុខភាពសម្រាប់អ្នកគ្រប់គ្នា កុំចេញក្រៅលើកលែងតែមានភាពចាំបាច់ ហើយគួរពាក់ម៉ាស់ដែលមានគុណភាពខ្ពស់។"
    elif aqius > 300:
        verdict = "គ្រាអាសន្ន"
        advice = "🚨 ស្ថានភាពអាសន្ន! សូមនៅក្នុងផ្ទះ បិទបង្អួចនិងទ្វារឲ្យជិត​ និង សូមប្រើប្រាស់ម៉ាសុីនខ្យល់បរិសុទ្ធ។"
    
    if (change[0] != 'stagnant') and (change[1] != "samecat"):
        return f'''
បច្ចុប្បន្ន វាជាម៉ោង {hour}:{minute} មានការអាប់ដេតអំពីគុណភាពខ្យល់។ គុណភាពខ្យល់មានការផ្លាស់ប្តូរ **{change[0]}** ពី **{aqius_prior} ({change[1]})** ទៅ **{aqius}** ({change[2]})**។ {advice}
        '''
    elif (change[0] != 'stagnant'):
        return f'''
បច្ចុប្បន្ន ម៉ោង {hour}:{minute} មានការអាប់ដេតអំពីគុណភាពខ្យល់។ គុណភាពខ្យល់មានការផ្លាស់ប្តូរ **{change[0]}** ពី **{aqius_prior}** ទៅ **{aqius}** ដែលជា **{verdict}**។ {advice}
        '''
    else:
        return f'''
បច្ចុប្បន្ន វាជាម៉ោង {hour}:{minute} មានការអាប់ដេតអំពីគុណភាពខ្យល់។ គុណភាពខ្យល់នៅតែជា **{verdict}** ដោយមានតម្លៃ AQI **{aqius}**។ {advice}
        '''


def update_jp(aqius, mainus, aqius_prior, mainus_prior, hour, minute, change):
    minute = f"{int(minute):02}"  # Ensure minute is always 2 digits
    verdict, advice = "", ""
    if 0 <= aqius <= 50:
        verdict = "良い"
        advice = "🌞 外に出て、新鮮な空気を吸って、この素晴らしい日を楽しみましょう。"
    elif 51 <= aqius <= 100:
        verdict = "普通"
        advice = "😷 外に出ても問題ありませんが、最新の空気質情報をチェックするのを忘れないでください。必要に応じてマスクを持参してください。"
    elif 101 <= aqius <= 150:
        verdict = "敏感な人にとって不健康"
        advice = "⚠️ 子供や高齢者、または呼吸器の問題を抱えている人は、長時間の屋外活動を控え、必要であればマスクを着用してください。"
    elif 151 <= aqius <= 200:
        verdict = "不健康"
        advice = "🚫 屋外での活動を最小限に抑え、可能であれば室内にいるようにしてください。空気清浄機を利用するとよいでしょう。"
    elif 201 <= aqius <= 300:
        verdict = "非常に不健康"
        advice = "❗ 空気質は健康に深刻な影響を及ぼします。外出する際は、高品質のマスクを着用し、健康アドバイスに従ってください。"
    elif aqius > 300:
        verdict = "危険"
        advice = "🚨 緊急事態です！窓やドアを閉め切り、屋内にとどまってください。空気清浄機を使用することをお勧めします。"
    
    if (change[0] != 'stagnant') and (change[1] != "samecat"):
        return f'''
今の時間は{hour}時{minute}分だよ！空気の状態が変わったよ。**{change[0]}**で、**{aqius_prior}（{change[1]}）**から**{aqius}（{change[2]}）**に変わったんだ。{advice}
        '''
    elif (change[0] != 'stagnant'):
        return f'''
今の時間は{hour}時{minute}分だよ！空気の状態が**{change[0]}**で、**{aqius_prior}**から**{aqius}**に変わったよ。今の空気は**「{verdict}」**だね。{advice}
        '''
    else:
        return f'''
今の時間は{hour}時{minute}分だよ！空気の状態は変わらず**「{verdict}」**のままだね。AQIスコアは**{aqius}**だよ。{advice}
        '''


def update_de(aqius, mainus, aqius_prior, mainus_prior, hour, minute, change):
    minute = f"{int(minute):02}"  # Ensure minute is always 2 digits
    verdict, advice = "", ""
    if 0 <= aqius <= 50:
        verdict = "gut"
        advice = "🌞 Geh ruhig nach draußen, atme die frische Luft ein und genieße diesen wunderbaren Tag!"
    elif 51 <= aqius <= 100:
        verdict = "moderat"
        advice = "😷 Es ist okay, nach draußen zu gehen, aber halte die aktuellen Luftqualitätsupdates im Blick. Sicher ist sicher, nimm eine Maske mit!"
    elif 101 <= aqius <= 150:
        verdict = "ungesund für empfindliche Gruppen"
        advice = "⚠️ Wenn du zu einer empfindlichen Gruppe gehörst – Kinder, ältere Menschen oder Menschen mit Atemproblemen – solltest du lange Aktivitäten im Freien vermeiden. Trag eine Maske, wenn nötig."
    elif 151 <= aqius <= 200:
        verdict = "ungesund"
        advice = "🚫 Beschränke Aktivitäten im Freien auf ein Minimum. Bleib möglichst drinnen und benutze einen Luftreiniger, wenn du einen hast."
    elif 201 <= aqius <= 300:
        verdict = "sehr ungesund"
        advice = "❗ Die Luftqualität ist ein ernsthaftes Gesundheitsrisiko. Gehe nur raus, wenn es absolut notwendig ist, und trag dabei eine hochwertige Maske. Achte auf Gesundheitsanweisungen."
    elif aqius > 300:
        verdict = "gefährlich"
        advice = "🚨 Notfall! Bleib drinnen, halte Fenster und Türen geschlossen und vermeide körperliche Anstrengungen. Nutze, falls vorhanden, einen Luftreiniger."
    else:
        verdict = "ungültiger AQI-Wert"
        advice = "❓ Bitte gib einen gültigen AQI-Wert ein, um Ratschläge zur Luftqualität zu erhalten."

    if (change[0] != 'stagnant') and (change[1] != "samecat"):
        return f'''
Es ist gerade {hour}:{minute} Uhr! Die Luftqualität hat sich geändert. Sie ist **{change[0]}** von **{aqius_prior} ({change[1]})** zu **{aqius} ({change[2]})** geworden. {advice}
        '''
    elif (change[0] != 'stagnant'):
        return f'''
Es ist gerade {hour}:{minute} Uhr! Die Luftqualität hat sich **{change[0]}** von **{aqius_prior}** auf **{aqius}** verändert. Die aktuelle Luftqualität ist **„{verdict}“**. {advice}
        '''
    else:
        return f'''
Es ist gerade {hour}:{minute} Uhr! Die Luftqualität ist unverändert und bleibt **„{verdict}“**. Der AQI-Wert liegt bei **{aqius}**. {advice}
        '''





# intell1slt_bot.send_message(chat_id=CHAT_ID, text="This is a test message from intell1slt bot!")
print("Test message sent!")



message=""
time_stamp_1=None
aqius_prior=""
mainus_prior=""
# Main loop to check time and call API


def get_aqi_category(aqius):
    # Define AQI category ranges
    if 0 <= aqius <= 50:
        return "good"
    elif 51 <= aqius <= 100:
        return "moderate"
    elif 101 <= aqius <= 150:
        return "unhealthy for sensitive groups"
    elif 151 <= aqius <= 200:
        return "unhealthy"
    elif 201 <= aqius <= 300:
        return "very unhealthy"
    elif aqius > 300:
        return "hazardous"
    else:
        return "invalid"

while True:
    # Fetch the current time and extract components
    current_time = datetime.datetime.now()
    seconds = int(current_time.strftime("%S"))
    minute = int(current_time.strftime("%M"))
    hour = int(current_time.strftime("%H"))
    day = current_time.strftime("%A")
    month = current_time.strftime("%B")
    date = int(current_time.strftime("%d"))
    year = current_time.strftime("%Y")


    if (minute ==0) and (seconds == 0) and (hour == 6):
        print("Condition A is triggering the API call")
        aqius_prior = 0
        mainus_prior = ""
        print(f"API Called at {hour:02}:{minute:02}:{seconds:02} on {day}")
        time_stamp_1 = current_time.replace(second=0, microsecond=0)

        aqius, mainus = get_phnom_penh_aq()
        image_file_name=get_aqi_category(aqius=aqius).replace(' ','_')+".png"
        print(image_file_name)
        message = f'''
                    {date}/{month}/{year} {hour}:{minute:02}\n
                    =====ភាសាខ្មែរ=====\n
                    {morning_message_kh(aqius, mainus)}\n
                    =====English=====\n
                    {morning_message_en(aqius, mainus)}\n
                    =====Deutsch=====\n
                    {morning_message_de(aqius, mainus)}\n
                    =====日本語=====\n
                    {morning_message_jp(aqius, mainus)}
                '''

        # image_path =   # Path to the image file

        # Send the image with the text message
        try:
            for attempt in range(4):  # Retry up to 4 times
                try:
                    with open(f"./labels/{image_file_name}", 'rb') as image_file:
                        intell1slt_bot.send_photo(
                            chat_id=CHAT_ID,
                            photo=image_file,  # Photo binary
                            caption=None      # No caption for the photo
                        )
                    print("Image sent")
                    # Wait for 1 second to ensure the image loads first
                    time.sleep(1)

                    # Send the message after the photo
                    intell1slt_bot.send_message(
                        chat_id=CHAT_ID,
                        text=message,           # Your text message
                        parse_mode="Markdown"  # Optional: Specify Markdown or HTML if needed
                    )
                    print("Text sent")
                    break  # Exit the loop if successful
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == 3:  # If it's the last attempt, raise the exception
                        raise
                    time.sleep(2)  # Wait before retrying
            time.sleep(65)
        except Exception as e:
            print(f"An error occurred: {e}")
            # Continue execution even if an error occurs

    # Check if it's time to call the API (every 5 minutes at XX:00 seconds)
    elif (minute % 5 == 0) and (seconds == 0) and (6 <= hour <= 21):  #
        print((6 <= hour <= 21))
        print("Condition B is triggering the API call")
        change = None
        time_stamp_1 = current_time.replace(second=0, microsecond=0)
        print(f"API Called at {hour:02}:{minute:02}:{seconds:02} on {day}")
        aqius, mainus = get_phnom_penh_aq()
        image_file_name=get_aqi_category(aqius=aqius).replace(' ','_') +".png"
        print(aqius)
        if aqius_prior==0:
            aqius_prior = aqius
            mainus_prior = mainus



        def update():
            print("update() called")
            if aqius_prior == 0:
                aqius_prior = aqius
                mainus_prior = mainus

   

            if abs(aqius - aqius_prior) <= 2 and get_aqi_category(aqius) == get_aqi_category(aqius_prior):
                change = ["stagnant", "samecat", "samecat"]
            elif aqius > aqius_prior + 2 and get_aqi_category(aqius) == get_aqi_category(aqius_prior):
                change = ["deteriorating", "samecat", "samecat"]
            elif aqius < aqius_prior - 2 and get_aqi_category(aqius) == get_aqi_category(aqius_prior):
                change = ["improving", "samecat", "samecat"]
            elif get_aqi_category(aqius) != get_aqi_category(aqius_prior):
                previous_category = get_aqi_category(aqius_prior)
                current_category = get_aqi_category(aqius)
                if aqius > aqius_prior:
                    change = ["deteriorating", previous_category, current_category]
                elif aqius < aqius_prior:
                    change = ["improving", previous_category, current_category]

            message = f'''
            {date}/{month}/{year} {hour}:{minute:02}\n
                =====ភាសាខ្មែរ=====\n
                {update_kh(aqius, mainus, aqius_prior, mainus_prior, hour, f"{minute:02}", change)}\n
                =====English=====\n
                {update_en(aqius, mainus, aqius_prior, mainus_prior, hour, f"{minute:02}", change)}\n
                =====Deutsch=====\n
                {update_de(aqius, mainus, aqius_prior, mainus_prior, hour, f"{minute:02}", change)}\n
                =====日本語=====\n
                {update_jp(aqius, mainus, aqius_prior, mainus_prior, hour, f"{minute:02}", change)}

            '''
            try:
                for attempt in range(4):  # Retry up to 4 times
                    try:
                        with open(f"./labels/{image_file_name}", 'rb') as image_file:
                            intell1slt_bot.send_photo(
                                chat_id=CHAT_ID,
                                photo=image_file,  # Photo binary
                                caption=None  # No caption for the photo
                            )
                        print("Image sent")
                        # Wait for 1 second to ensure the image loads first
                        time.sleep(1)

                        # Send the message after the photo
                        intell1slt_bot.send_message(
                            chat_id=CHAT_ID,
                            text=message,           # Your text message
                            parse_mode="Markdown"  # Optional: Specify Markdown or HTML if needed
                        )
                        print("Text sent")
                        break  # Exit the loop if successful
                    except Exception as e:
                        print(f"Attempt {attempt + 1} failed: {e}")
                        if attempt == 3:  # If it's the last attempt, raise the exception
                            raise
                        time.sleep(2)  # Wait before retrying
                print("Text Sent")
                time.sleep(65)
            except FileNotFoundError as e:
                print(f"File not found: {e}")
            except telebot.apihelper.ApiException as e:
                print(f"Telegram API error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
            print(f"Current AQI: {aqius}, Prior AQI: {aqius_prior}")
            aqius_prior = aqius
            mainus_prior = mainus
            

        


        if get_aqi_category(aqius) == "good":
            pass
        elif get_aqi_category(aqius) == "moderate":
            if (minute % 60 == 0) and (seconds == 0):
                update()
                time.sleep(65)
        elif get_aqi_category(aqius) == "unhealthy for sensitive groups":
            if (minute % 30 == 0) and (seconds == 0):
                update()
                time.sleep(65)
        elif get_aqi_category(aqius) == "unhealthy":
            if (minute % 15 == 0) and (seconds == 0):
                update()
                time.sleep(65)
        elif get_aqi_category(aqius) == "very unhealthy":
            if (minute % 10 == 0) and (seconds == 0):
                update()
                time.sleep(65)
        elif get_aqi_category(aqius) == "hazardous":
            if (minute % 5 == 0) and (seconds == 0):
                update()
                time.sleep(65)
        time.sleep(65)
    if (minute == 0) and (seconds == 30) and (hour == 21):
        message = f'''
        {date}/{month}/{year} {hour}:{minute:02}\n
            =====ភាសាខ្មែរ=====\n
            {signoff_kh()}\n
            =====English=====\n
            {signoff_en()}\n
            =====Deutsch=====\n
            {signoff_de()}\n
            =====日本語=====\n
            {signoff_jp()}
        '''
        # Debugging the message

        intell1slt_bot.send_message(chat_id=CHAT_ID, text=message)
        time.sleep(65)

    time.sleep(0.25)
    continue
    # Template to send an image using the Telegram bot
    # Uncomment and modify the following lines to send an image:

    # with open("path_to_image.jpg", "rb") as image_file:
    #     intell1slt_bot.send_photo(chat_id=CHAT_ID, photo=image_file, caption="Optional caption for the image")