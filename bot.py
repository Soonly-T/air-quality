import os
import telebot
import datetime
import time
import requests as req
import json




weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday"]
weekends = ["Friday", "Saturday", "Sunday"]



class Message:
    def __init__(self):
        self.change=""

        self.verdict = {
        "good": {
            "en": "good",
            "kh": "ល្អ",
            "jp": "良い (Good)",
            "de": "Gut (Good)"
        },
        "moderate": {
            "en": "moderate",
            "kh": "មធ្យម",
            "jp": "普通 (Moderate)",
            "de": "Mäßig (Moderate)"
        },
        "unhealthy for sensitive groups": {
            "en": "unhealthy for sensitive groups",
            "kh": "មិនល្អសម្រាប់ក្រុមអ្នកងាយនឹងទទួលផលប៉ះពាល់",
            "jp": "敏感な人にとっては不健康 (Unhealthy for Sensitive Groups)",
            "de": "Ungesund für empfindliche Gruppen (Unhealthy for Sensitive Groups)"
        },
        "unhealthy": {
            "en": "unhealthy",
            "kh": "មិនល្អ",
            "jp": "不健康 (Unhealthy)",
            "de": "Ungesund (Unhealthy)"
        },
        "very_unhealthy": {
            "en": "very unhealthy",
            "kh": "អាក្រក់ខ្លាំង",
            "jp": "非常に不健康 (Very Unhealthy)",
            "de": "Sehr ungesund (Very Unhealthy)"
        },
        "hazardous": {
            "en": "hazardous",
            "kh": "គ្រាអាសន្ន",
            "jp": "危険 (Hazardous)",
            "de": "Gefährlich (Hazardous)"
        },
        "invalid": {
            "en": "invalid AQI value",
            "kh": "តម្លៃ AQI មិនត្រឹមត្រូវ",
            "jp": "無効なAQI値",
            "de": "Ungültiger AQI-Wert"
        }
    }
        self.advice = {
            "good": {
                "en": "🌞 Go outside, breathe some of that fresh air and enjoy this wonderful day.",
                "kh": "🌞 ចេញក្រៅដោយមិនមានការព្រួយបារម្ភ រីករាយជាមួយខ្យល់បរិសុទ្ធ ហើយរីករាយជាមួយថ្ងៃដ៏អស្ចារ្យនេះ។",
                "jp": "🌞 外に出て、新鮮な空気を吸い、この素晴らしい日を楽しみましょう！",
                "de": "🌞 Gehen Sie nach draußen, atmen Sie die frische Luft ein und genießen Sie diesen wunderbaren Tag!"
            },
            "moderate": {
                "en": "😷 It's fine to go outside but make sure to keep updated with us for the latest air quality news. Also, while not necessary, wear or bring a mask just in case.",
                "kh": "😷 អាចចេញក្រៅបាន ប៉ុន្តែសូមតាមដានព័ត៌មានថ្មីៗអំពីគុណភាពខ្យល់ពីយើង។ អ្នកក៏អាចពាក់ ឬយកម៉ាស់តាមផង ដើម្បីការពារសុខភាព។",
                "jp": "😷 外に出ても大丈夫ですが、最新の空気質情報をチェックするようにしてください。必要ではありませんが、念のためにマスクを持参または着用してください。",
                "de": "😷 Es ist in Ordnung, nach draußen zu gehen, aber halten Sie sich über die neuesten Nachrichten zur Luftqualität auf dem Laufenden. Auch wenn es nicht unbedingt erforderlich ist, nehmen oder tragen Sie sicherheitshalber eine Maske."
            },
            "unhealthy for sensitive groups": {
                "en": "⚠️ If you're part of a sensitive group, such as children, the elderly, or those with respiratory issues, minimize prolonged outdoor activities and consider wearing a mask if necessary.",
                "kh": "⚠️ ប្រសិនបើអ្នកជាក្រុមអ្នកងាយនឹងទទួលផលប៉ះពាល់ ដូចជា កុមារ អ្នកចាស់ ឬអ្នកមានបញ្ហាសុខភាពផ្នែកផ្លូវដង្ហើម សូមកំុការចេញក្រៅច្រើន។ គិតពី​ការពាក់ម៉ាស់ផងប្រសិនបើចាំបាច់។",
                "jp": "⚠️ 子供、高齢者、または呼吸器系の問題を抱える敏感なグループに属している場合は、長時間の屋外活動を控え、必要に応じてマスクを着用してください。",
                "de": "⚠️ Wenn Sie zu einer empfindlichen Gruppe gehören, wie z. B. Kinder, ältere Menschen oder Personen mit Atemwegsproblemen, sollten Sie längere Aufenthalte im Freien vermeiden und bei Bedarf eine Maske tragen."
            },
            "unhealthy": {
                "en": "🚫 Limit outdoor activities to a minimum. Stay indoors as much as possible, and use air purifiers if available. Everyone, not just sensitive groups, should take precautions.",
                "kh": "🚫 កាត់បន្ថយសកម្មភាពខាងក្រៅ​ គួរប្រើប្រាស់ម៉ាសុីនខ្យល់បរិសុទ្ធ មនុស្សគ្រប់ក្រុមគួរមានការប្រុងប្រយ័ត្ន។",
                "jp": "🚫 屋外活動を最小限に抑え、可能であれば室内にいるようにしてください。また、空気清浄機を使用すると良いでしょう。全員が予防措置を講じる必要があります。",
                "de": "🚫 Reduzieren Sie Aktivitäten im Freien auf ein Minimum. Bleiben Sie möglichst in Innenräumen und verwenden Sie, wenn verfügbar, Luftreiniger. Nicht nur empfindliche Gruppen sollten Vorsichtsmaßnahmen treffen, sondern alle."
            },
            "very unhealthy": {
                "en": "❗ The air quality poses a serious health risk to everyone. Avoid going outdoors unless absolutely necessary, and wear a high-quality mask if you need to step outside. Follow health advisories closely.",
                "kh": "❗ គុណភាពខ្យល់ផ្តល់នូវហានិភ័យដល់សុខភាពសម្រាប់អ្នកគ្រប់គ្នា កុំចេញក្រៅលើកលែងតែមានភាពចាំបាច់ ហើយគួរពាក់ម៉ាស់ដែលមានគុណភាពខ្ពស់។",
                "jp": "❗ 空気質が健康に深刻なリスクをもたらします。絶対に必要でない限り外に出ないようにし、外出する場合は高性能のマスクを着用してください。公的な健康指導に従ってください。",
                "de": "❗ Die Luftqualität stellt ein ernstes Gesundheitsrisiko für alle dar. Vermeiden Sie den Aufenthalt im Freien, es sei denn, es ist absolut notwendig. Tragen Sie eine hochwertige Maske, wenn Sie nach draußen gehen müssen. Folgen Sie den Gesundheitsempfehlungen."
            },
            "hazardous": {
                "en": "🚨 Emergency conditions! Stay indoors with windows and doors shut. Avoid physical exertion, and follow any official instructions. If available, use air purifiers to improve indoor air quality.",
                "kh": "🚨 ស្ថានភាពអាសន្ន! សូមនៅក្នុងផ្ទះ បិទបង្អួចនិងទ្វារឲ្យជិត​ និង សូមប្រើប្រាស់ម៉ាសុីនខ្យល់បរិសុទ្ធ។",
                "jp": "🚨 非常事態です！屋内に留まり、窓とドアをしっかりと閉めてください。身体を動かさないようにし、公式の指示に従ってください。空気清浄機があれば使用してください。",
                "de": "🚨 Notfallbedingungen! Bleiben Sie in Innenräumen und schließen Sie Fenster und Türen. Vermeiden Sie körperliche Anstrengung und folgen Sie offiziellen Anweisungen. Verwenden Sie, wenn möglich, Luftreiniger."
            },
            "invalid": {
                "en": "❓ Please provide a valid AQI value to receive air quality advice.",
                "kh": "❓ សូមផ្តល់ជូនតម្លៃ AQI ដែលត្រឹមត្រូវ ដើម្បីទទួលបានដំបូន្មានគុណភាពខ្យល់។",
                "jp": "❓ 有効なAQI値を入力してください。",
                "de": "❓ Bitte geben Sie einen gültigen AQI-Wert ein."
            }
        }
    
    def get_aqi_category(self,aqius):
    # Define AQI category ranges
        if 0 <= aqius <= 50:
            #print(f"AQI category determined: good, AQI value: {aqius}")
            return "good"
        elif 51 <= aqius <= 100:
            #print(f"AQI category determined: moderate, AQI value: {aqius}")
            return "moderate"
        elif 101 <= aqius <= 150:
            #print(f"AQI category determined: unhealthy for sensitive groups, AQI value: {aqius}")
            return "unhealthy for sensitive groups"
        elif 151 <= aqius <= 200:
            #print(f"AQI category determined: unhealthy, AQI value: {aqius}")
            return "unhealthy"
        elif 201 <= aqius <= 300:
            #print(f"AQI category determined: very unhealthy, AQI value: {aqius}")
            return "very unhealthy"
        elif aqius > 300:
            #print(f"AQI category determined: hazardous, AQI value: {aqius}")
            return "hazardous"
        else:
            #print(f"AQI category determined: invalid, AQI value: {aqius}")
            return "invalid"

    
    morning_message= lambda self,aqius,: ({
        "en":f'''
🌅 Good morning, ladies and gentlemen. I hope you have had a restful sleep and are eager to begin the new day. The air today is at a **{aqius}**, which means it's **{self.verdict[self.get_aqi_category(aqius)]["en"]}**. {self.advice[self.get_aqi_category(aqius)]["en"]}
''',
        "kh":f'''
🌅 អរុណសួស្តី លោកនិងលោកស្រី ខ្ញុំសូមសង្ឃឹមថាអ្នកមានការគេងសំរានជ្រាលជ្រៅ ហើយត្រៀមខ្លួនដើម្បីចាប់ផ្តើមថ្ងៃថ្មី។ ខ្យល់សព្វថ្ងៃនេះមានពិន្ទុ **{aqius}** ដែលមានន័យថា **{self.verdict[self.get_aqi_category(aqius)]["kh"]}**។ **{self.advice[self.get_aqi_category(aqius)]["kh"]}**
''',
"jp":        f'''
🌅 おはようございます、みなさん！昨晩はぐっすり眠れましたか？今日の空気の指数 (AQI) は **{aqius}** で、**「{self.verdict[self.get_aqi_category(aqius)]["jp"]}」**の状態です。**{self.advice[self.get_aqi_category(aqius)]["jp"]}**
    ''',
    "de":        f'''
🌅 Guten Morgen, meine Damen und Herren. Ich hoffe, Sie hatten einen erholsamen Schlaf und sind bereit, den neuen Tag zu beginnen. Die Luft heute hat einen AQI von {aqius}, was bedeutet, dass sie **{self.verdict[self.get_aqi_category(aqius)]["de"]}** ist. **{self.advice[self.get_aqi_category(aqius)]["de"]}**
'''
    })


    signoff= lambda self :(
        {
    "en": "🌙 It's currently 21:00 and it's time for me to sign off. 💤 I will see you again tomorrow at 6 onwards to give you more updates on the air quality. 🌍 This has been intell1slt_bot at your service. 🌟 Good night! 🌌",
    "kh": "🌙 បច្ចុប្បន្ននេះម៉ោង 21:00 ហើយបានដល់ពេលដែលខ្ញុំត្រូវបញ្ចប់សេវាកម្មថ្ងៃនេះ។ 💤 ខ្ញុំនឹងជួបអ្នកវិញនៅថ្ងៃស្អែកចាប់ពីម៉ោង 6 ដើម្បីផ្តល់ព័ត៌មានថ្មីៗអំពីគុណភាពខ្យល់។ 🌍 នេះគឺជា​ intell1slt_bot ដែលបានបម្រើសេវាកម្មសម្រាប់លោកអ្នក។ 🌟 សុបិន្តល្អ! 🌌",
    "jp": "🌙 こんばんは、みなさん！今は21:00になりましたので、今日はこれでおやすみします。 💤 明日の朝6時から、また空気の質に関する情報をお届けします。 🌍 これまでお付き合いいただきありがとうございました。intell1slt_botより、良い夜をお過ごしください。 🌟 おやすみなさい！ 🌌",
    "de": "🌙 Es ist jetzt 21:00 Uhr und Zeit für mich, mich für heute zu verabschieden. 💤 Ich bin morgen ab 6 Uhr wieder da, um Ihnen weitere Updates zur Luftqualität zu geben. 🌍 Dies war intell1slt_bot, zu Ihren Diensten. 🌟 Gute Nacht! 🌌"
    }
    )

    def update(self, aqius, mainus, aqius_prior, mainus_prior, hour, minute, change):
        category=self.get_aqi_category(aqius)
        delta={
            "improving": {
                "en": "improved",
                "kh": "ជាប្រសើរឡើង",
                "jp": "向上",
                "de": "besser"
            },
            "deteriorating": {
                "en": "deteriorated",
                "kh": "ជាការធ្លាក់ចុះ",
                "jp": "悪化",
                "de": "schlechter"
            },
            "stagnant": {
                "en": "stagnant",
                "kh": "មិនមានការផ្លាស់ប្តូរ",
                "jp": "停滞",
                "de": "stagnierend"
            }

        }

        mutate_state = "change" if change[0] != 'stagnant' and change[1] != "samecat" else "change_samecat" if change[0] != 'stagnant' else "samecat"
        minute= f"{int(minute):02}"  # Ensure minute is always 2 digits
        messages = {
            "samecat": {
            "en": f'''
        Currently, it is {hour}:{minute} with an update to the air quality. The air quality is still **{self.verdict[category]["en"]}** with an AQI score of **{aqius}**. {self.advice[category]["en"]}
            ''',
            "kh": f'''
        បច្ចុប្បន្ន ម៉ោង {hour}:{minute} មានការអាប់ដេតអំពីគុណភាពខ្យល់។ គុណភាពខ្យល់នៅតែជា **{self.verdict[category]["kh"]}** ដោយមានតម្លៃ AQI **{aqius}**។ {self.advice[category]["kh"]}
            ''',
            "jp": f'''
        今の時間は{hour}時{minute}分だよ！空気の状態は変わらず**「{self.verdict[category]["jp"]}」**のままだね。AQIスコアは**{aqius}**だよ。{self.advice[category]["jp"]}
            ''',
            "de": f'''
        Es ist gerade {hour}:{minute} Uhr! Die Luftqualität ist unverändert und bleibt **„{self.verdict[category]["de"]}“**. Der AQI-Wert liegt bei **{aqius}**. {self.advice[category]["de"]}
            '''
            },
            "change_samecat": {
            "en": f'''

                    Currently, it is {hour}:{minute} with an update to the air quality. The air quality has **{delta[change[0]]["en"]}** from **{aqius_prior}** to **{aqius}**, which is still **{self.verdict[category]["en"]}**. {self.advice[category]["en"]}
            ''',
            "kh": f'''
        បច្ចុប្បន្ន ម៉ោង {hour}:{minute} មានការអាប់ដេតអំពីគុណភាពខ្យល់។ គុណភាពខ្យល់មានការផ្លាស់ប្តូរ **{delta[change[0]]["kh"]}** ពី **{aqius_prior}** ទៅ **{aqius}** ដែលនៅតែជា **{self.verdict[category]["kh"]}**។ {self.advice[category]["kh"]}
            ''',
            "jp": f'''
        今の時間は{hour}時{minute}分だよ！空気の状態が**{delta[change[0]]["jp"]}**で、**{aqius_prior}**から**{aqius}**に変わったけど、まだ**「{self.verdict[category]["jp"]}」**だね。{self.advice[category]["jp"]}
            ''',
            "de": f'''
        Es ist gerade {hour}:{minute} Uhr! Die Luftqualität hat sich **{delta[change[0]]["de"]}** von **{aqius_prior}** auf **{aqius}** verändert, bleibt aber **„{self.verdict[category]["de"]}“**. {self.advice[category]["de"]}
            '''
            },
            "change": {
            "en": f'''
        Currently, it is {hour}:{minute} with an update to the air quality. The air quality has **{delta[change[0]]["en"]}** from **{aqius_prior} ({self.get_aqi_category(aqius_prior)["en"]})** to **{aqius} ({self.get_aqi_category(aqius)["en"]})**. {self.advice[category]["en"]}
            ''',
            "kh": f'''
        បច្ចុប្បន្ន ម៉ោង {hour}:{minute} មានការអាប់ដេតអំពីគុណភាពខ្យល់។ គុណភាពខ្យល់មានការផ្លាស់ប្តូរ **{delta[change[0]]["kh"]}** ពី **{aqius_prior} ({self.get_aqi_category(aqius_prior)["kh"]})** ទៅ **{aqius} ({self.get_aqi_category(aqius)["kh"]})**។ {self.advice[category]["kh"]}
            ''',
            "jp": f'''
        今の時間は{hour}時{minute}分だよ！空気の状態が変わったよ。**{delta[change[0]]["jp"]}**で、**{aqius_prior}（{self.get_aqi_category(aqius_prior)["jp"]}）**から**{aqius}（{self.get_aqi_category(aqius)["jp"]}）**に変わったんだ。{self.advice[category]["jp"]}
            ''',
            "de": f'''
        Es ist gerade {hour}:{minute} Uhr! Die Luftqualität hat sich geändert. Sie ist **{delta[change[0]]["de"]}** von **{aqius_prior} ({self.get_aqi_category(aqius_prior)["de"]})** zu **{aqius} ({self.get_aqi_category(aqius)["de"]})** geworden. {self.advice[category]["de"]}
            '''
            }
        }

        update={
            "en":messages[mutate_state]["en"],
            "kh":messages[mutate_state]["kh"],
            "jp":messages[mutate_state]["jp"],
            "de":messages[mutate_state]["de"]
        }
        return update
    

class Main:

    def __init__(self):
        with open("./keys.json","r") as file:
            keys=json.load(file)

        self.API_KEY=keys["iqair_api"]
        self.BOT_TOKEN = keys["bot_token"]
        self.CHAT_ID = keys["chat_id"]
        self.message = ""
        self.aqius=0
        self.mainus=""
        self.aqius_prior=0
        self.mainus_prior=""
        self.intell1slt_bot=self.initializeBot()
        self.msg=Message()
        self.change = None
        self.category=""
        # self.intell1slt_bot.send_message(chat_id=self.CHAT_ID, text="This is a test message from intell1slt bot!")

        
    def initializeBot(self):
        intell1slt_bot = telebot.TeleBot(self.BOT_TOKEN)
        try:
            # Send a startup message
            # intell1slt_bot.send_message(chat_id=self.CHAT_ID, text="intell1slt_bot is now online.")
            intell1slt_bot.send_message(chat_id=712191968, text="intell1slt_bot is now online.")
            print("Test message sent!")
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Failed to send a message: {e}")
        return intell1slt_bot
    
    def get_phnom_penh_aq(self):
        for attempt in range(5):  # Retry up to 5 times
            try:
                phnom_penh_aq = req.get(f"http://api.airvisual.com/v2/city?city=Phnom Penh&state=Phnom Penh&country=Cambodia&key={self.API_KEY}").json()
                aqius = phnom_penh_aq["data"]["current"]["pollution"]["aqius"]
                mainus = phnom_penh_aq["data"]["current"]["pollution"]["mainus"]
                return aqius, mainus
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2)  # Wait before retrying
        return "Error", "Error"  # Return "Error" if all attempts fail
    
    def get_aqi_category(self,aqius):
        return self.msg.get_aqi_category(aqius)
    
    def get_image(self,aqius):
        image_file_name=self.get_aqi_category(aqius).replace(' ','_')+".png"
        return image_file_name
    
    def send_message(self,image_file_name,message):
        try:
            for attempt in range(4):  # Retry up to 4 times
                try:
                    with open(f"./labels/{image_file_name}", 'rb') as image_file:
                        self.intell1slt_bot.send_photo(
                            chat_id=self.CHAT_ID,
                            photo=image_file,  
                            caption=None      
                        )
                    print("Image sent")
                    time.sleep(1)

                    self.intell1slt_bot.send_message(
                        chat_id=self.CHAT_ID,
                        text=message,           
                        parse_mode="Markdown"  
                    )
                    print("Text sent")
                    break  
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == 3:  # If it's the last attempt, raise the exception
                        raise
                    time.sleep(2)  # Wait before retrying
            time.sleep(65)
        except Exception as e:
            print(f"An error occurred: {e}")

    def send_only_message(self,message):
        try:
            for attempt in range(4):  # Retry up to 4 times
                try:
                    self.intell1slt_bot.send_message(
                        chat_id=self.CHAT_ID,
                        text=message,           
                        parse_mode="Markdown"  
                    )
                    print("Text sent")
                    break  
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == 3:  # If it's the last attempt, raise the exception
                        raise
                    time.sleep(2)  # Wait before retrying
            time.sleep(65)
        except Exception as e:
            print(f"An error occurred: {e}")

    def update(self,date,month,year,hour,minute):

        print("update() called")
        if abs(self.aqius - self.aqius_prior) <= 2 and self.get_aqi_category(self.aqius) == self.get_aqi_category(self.aqius_prior):
            self.change = ["stagnant", "samecat", "samecat"]
        elif self.aqius > self.aqius_prior + 2 and self.get_aqi_category(self.aqius) == self.get_aqi_category(self.aqius_prior):
            self.change = ["deteriorating", "samecat", "samecat"]
        elif self.aqius < self.aqius_prior - 2 and self.get_aqi_category(self.aqius) == self.get_aqi_category(self.aqius_prior):
            self.change = ["improving", "samecat", "samecat"]
        elif self.get_aqi_category(self.aqius) != self.get_aqi_category(self.aqius_prior):
            previous_category = self.get_aqi_category(self.aqius_prior)
            current_category = self.get_aqi_category(self.aqius)
            if self.aqius > self.aqius_prior:
                self.change = ["deteriorating", previous_category, current_category]
            elif self.aqius < self.aqius_prior:
                self.change = ["improving", previous_category, current_category]

        message = f'''
        {date}/{month}/{year} {hour}:{minute:02}\n
            =====ភាសាខ្មែរ=====\n
            {self.msg.update(self.aqius, self.mainus, self.aqius_prior, self.mainus_prior, hour, f"{minute:02}", self.change)["kh"]}\n
            =====English=====\n
            {self.msg.update(self.aqius, self.mainus, self.aqius_prior, self.mainus_prior, hour, f"{minute:02}", self.change)["en"]}\n
            =====Deutsch=====\n
            {self.msg.update(self.aqius, self.mainus, self.aqius_prior, self.mainus_prior, hour, f"{minute:02}", self.change)["de"]}\n
            =====日本語=====\n
            {self.msg.update(self.aqius, self.mainus, self.aqius_prior, self.mainus_prior, hour, f"{minute:02}", self.change)["jp"]}

        '''
        self.aqius_prior = self.aqius
        self.mainus_prior = self.mainus
        return message
    def main(self):
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

            if (minute ==00) and (seconds == 0) and (hour == 6):

                print("Condition A is triggering the API call")
                print(f"API Called at {hour:02}:{minute:02}:{seconds:02} on {day}")
                self.aqius, self.mainus = self.get_phnom_penh_aq()
                image_file_name = self.get_image(self.aqius)
                self.category=self.get_aqi_category(self.aqius)
                morning_message=self.msg.morning_message(self.aqius)
                message = f'''
                            {date}/{month}/{year} {hour}:{minute:02}\n
                            =====ភាសាខ្មែរ=====\n
                            {morning_message["kh"]}\n
                            =====English=====\n
                            {morning_message["en"]}\n
                            =====Deutsch=====\n
                            {morning_message["de"]}\n
                            =====日本語=====\n
                            {morning_message["jp"]}
                        '''
                self.send_message(image_file_name,message)
            elif (minute % 5 == 0 and seconds == 0 and 6 <= hour < 21) or (hour == 21 and minute == 0 and seconds == 0):
                
                print("Condition B is triggering the API call")
                print(f"API Called at {hour:02}:{minute:02}:{seconds:02} on {day}")
                self.aqius, self.mainus = self.get_phnom_penh_aq()
                self.category=self.get_aqi_category(self.aqius)
                image_file_name = self.get_image(self.aqius)
                self.change=None
                print(f"Current AQI: {self.aqius}, Prior AQI: {self.aqius_prior}, Category:{self.category} ")
                
                if self.aqius_prior==0:
                    self.aqius_prior = self.aqius
                    self.mainus_prior = self.mainus

                message=""

                if self.category == "good":
                    if (minute % 60 == 0) and (seconds == 0) and (hour%2==0):
                        message= self.update(date,month,year,hour,minute)
                        self.send_message(image_file_name,message)
                elif self.category == "moderate":
                    if (minute % 60 == 0) and (seconds == 0):
                        message= self.update(date,month,year,hour,minute)
                        self.send_message(image_file_name,message)

                elif self.category == "unhealthy for sensitive groups":
                    if (minute % 30 == 0) and (seconds == 0):
                        message= self.update(date,month,year,hour,minute)
                        self.send_message(image_file_name,message)

                elif self.category == "unhealthy":
                    if (minute % 15 == 0) and (seconds == 0):
                        message= self.update(date,month,year,hour,minute)
                        self.send_message(image_file_name,message)

                elif self.category == "very unhealthy":
                    if (minute % 10 == 0) and (seconds == 0):
                        message= self.update(date,month,year,hour,minute)
                        self.send_message(image_file_name,message)

                elif self.category == "hazardous":
                    if (minute % 5 == 0) and (seconds == 0):
                        message= self.update(date,month,year,hour,minute)
                        self.send_message(image_file_name,message)

                if (minute == 00) and (seconds == 00) and (hour == 21):
                    time.sleep(5)
                    print("Condition C is triggering the goodbye call")
                    print(f"API Called at {hour:02}:{minute:02}:{seconds:02} on {day}")
                    signoff = self.msg.signoff()
                    print(signoff)
                    message = f'''
                    {date}/{month}/{year} {hour}:{minute:02}\n
                            =====ភាសាខ្មែរ=====\n
{signoff["kh"]}\n
                            =====English=====\n
{signoff["en"]}\n
                            =====Deutsch=====\n
{signoff["de"]}\n
                            =====日本語=====\n
{signoff["jp"]}
                    '''
                    self.send_only_message(message)
                time.sleep(65)
            
    
            time.sleep(0.1)


if __name__ == "__main__":

    air_quality_bot = Main()

    air_quality_bot.main()
