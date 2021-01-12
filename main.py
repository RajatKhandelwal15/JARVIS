from Jarvis import JarvisAssistant
import json, re, os, random, pprint, webbrowser, datetime, requests
import config, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request  # used to make requests
import urllib.parse  # used to parse values into the url
import pyjokes
import time
import pyautogui
from PIL import Image
import wolframalpha
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Jarvis.features.gui import Ui_MainWindow


obj = JarvisAssistant()

# ================================ MEMORY ===========================================================================================================

GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey jarvis",
             "ok jarvis", "are you there"]
GREETINGS_RES = ["always there for you sir", "i am ready sir",
                 "your wish my command", "how can i help you sir?", "i am online and ready sir"]

EMAIL_DIC = {
    'myself': 'atharvaaingle@gmail.com',
    'my official email': 'atharvaaingle@gmail.com',
    'my second email': 'atharvaaingle@gmail.com',
    'my official mail': 'atharvaaingle@gmail.com',
    'my second mail': 'atharvaaingle@gmail.com'
}

CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
# =======================================================================================================================================================
def speak(text):
    obj.tts(text)

app_id = config.wolframalpha_id
def computational_intelligence(question):
    client = wolframalpha.Client(app_id)
    answer = client.query(question)
    answer = next(answer.results).text
    print(answer)
    
    return answer

def wish():
    speak("I am Jarvis. Online and ready sir. Please tell me how may I help you")
# if __name__ == "__main__":


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()


    def TaskExecution(self):

    # wish()

        while True:
            command = obj.mic_input()

            if re.search('date', command):
                date = obj.tell_me_date()
                print(date)
                speak(date)

            elif "time" in command:
                time_c = obj.tell_time()
                print(time_c)
                speak(f"Sir the time is {time_c}")

            elif re.search('launch', command):
                dict_app = {
                    'chrome': 'C:/Program Files/Google/Chrome/Application/chrome'
                }

                app = command.split(' ', 1)[1]
                path = dict_app.get(app)

                if path is None:
                    speak('Application path not found')
                    print('Application path not found')

                else:
                    speak('Launching: ' + app + 'for you sir!')
                    obj.launch_any_app(path_of_app=path)

            elif command in GREETINGS:
                speak(random.choice(GREETINGS_RES))

            elif re.search('open', command):
                domain = command.split(' ')[-1]
                open_result = obj.website_opener(domain)
                speak(f'Alright sir !! Opening {domain}')
                print(open_result)

            elif re.search('weather', command):
                city = command.split(' ')[-1]
                weather_res = obj.weather(city=city)
                print(weather_res)
                speak(weather_res)

            elif re.search('tell me about', command):
                topic = command.split(' ')[-1]
                if topic:
                    wiki_res = obj.tell_me(topic)
                    print(wiki_res)
                    speak(wiki_res)
                else:
                    speak(
                        "Sorry sir. I couldn't load your query from my database. Please try again")

            elif "buzzing" in command or "news" in command or "headlines" in command:
                news_res = obj.news()
                speak('Source: The Times Of India')
                speak('Todays Headlines are..')
                for index, articles in enumerate(news_res):
                    pprint.pprint(articles['title'])
                    speak(articles['title'])
                    if index == len(news_res)-1:
                        break
                    # speak('Moving on the next news headline..')
                speak('These were the top headlines, Have a nice day Sir!!..')

            elif 'search google for' in command:
                obj.search_anything_google(command)
                

            # elif 'youtube' in command:
            #     speak('Ok!')
            #     reg_ex = re.search('youtube (.+)', command)
            #     if reg_ex:
            #         domain = command.split("youtube",1)[1]
            #         song = urllib.parse.urlencode({"search_query" : domain})
            #         print(song)

            #         # fetch the ?v=query_string
            #         result = urllib.request.urlopen("http://www.youtube.com/results?" + song)
            #         print(result)

            #         # make the url of the first result song
            #         search_results = re.findall(r'href=\"\/watch\?v=(.{11})', result.read().decode())
            #         print(search_results)

            #         # make the final url of song selects the very first result from youtube result
            #         url = "http://www.youtube.com/watch?v="+search_results[0]

            #         # play the song using webBrowser module which opens the browser 
            #         # webbrowser.open(url, new = 1)
            #         webbrowser.open_new(url)

            elif "email" in command or "send email" in command:
                sender_email = config.email
                sender_password = config.email_password

                try:
                    speak("Whom do you want to email sir ?")
                    recipient = obj.mic_input()
                    receiver_email = EMAIL_DIC.get(recipient)
                    if receiver_email:

                        speak("What is the subject sir ?")
                        subject = obj.mic_input()
                        speak("What should I say?")
                        message = obj.mic_input()
                        msg = 'Subject: {}\n\n{}'.format(subject, message)
                        obj.send_mail(sender_email, sender_password,
                                    receiver_email, msg)
                        speak("Email has been successfully sent")

                    else:
                        speak(
                            "I coudn't find the requested person's email in my database. Please try again with a different name")

                except:
                    speak("Sorry sir. Couldn't send your mail. Please try again")

            elif "what do i have" in command or "do i have plans" or "am i busy" in command:
                obj.google_calendar_events(command)

            if "make a note" in command or "write this down" in command or "remember this" in command:
                speak("What would you like me to write down?")
                note_text = obj.mic_input()
                obj.take_note(note_text)
                speak("I've made a note of that")
            
            elif "close the note" in command or "close notepad" in command:
                speak("Okay sir, closing notepad")
                os.system("taskkill /f /im notepad++.exe")

            
            if "joke" in command:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)
            
            elif "system" in command:
                sys_info = obj.system_info()
                print(sys_info)
                speak(sys_info)
            
            elif "where is" in command:
                place = command.split('where is ', 1)[1]
                current_loc, target_loc, distance = obj.location(place)
                city = target_loc.get('city', '')
                state = target_loc.get('state', '')
                country = target_loc.get('country', '')
                time.sleep(1)
                try:

                    if city:
                        res = f"{place} is in {state} state and country {country}. It is {distance} km away from your current location"
                        print(res)
                        speak(res)
                    
                    else:
                        res = f"{state} is a state in {country}. It is {distance} km away from your current location"
                        print(res)
                        speak(res)

                except:
                    res = "Sorry sir, I couldn't get the co-ordinates of the location you requested. Please try again"
                    speak(res)
            
            
            elif "ip address" in command:
                ip = requests.get('https://api.ipify.org').text
                print(ip)
                speak(f"Your ip address is {ip}")

            elif "switch the window" in command or "switch window" in command:
                speak("Okay sir, Switching the window")
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            
            elif "where i am" in command or "current location" in command or "where am i" in command:
                try:
                    city, state, country = obj.my_location()
                    print(city, state, country)
                    speak(f"You are currently in {city} city which is in {state} state and country {country}")
                except Exception as e:
                    speak("Sorry sir, I coundn't fetch your current location. Please try again")

            elif "take screenshot" in command or "take a screenshot" in command or "capture the screen" in command:
                speak("By what name do you want to save the screenshot?")
                name = obj.mic_input()
                speak("Alright sir, taking the screenshot")
                img = pyautogui.screenshot()
                name = f"{name}.png"
                img.save(name)
                speak("The screenshot has been succesfully captured")

            elif "show me the screenshot" in command:
                try:
                    img = Image.open('D://JARVIS//JARVIS_2.0//' + name)
                    img.show(img)
                    speak("Here it is sir")
                    time.sleep(2)
                
                except IOError:
                    speak("Sorry sir, I am unable to display the screenshot")
            

            elif "hide all files" in command or "hide this folder" in command:
                os.system("attrib +h /s /d")
                speak("Sir, all the files in this folder are now hidden")
            
            elif "visible" in command or "make files visible" in command:
                os.system("attrib -h /s /d")
                speak("Sir, all the files in this folder are now visible to everyone. I hope you are taking this decision in your own peace")

            # if "calculate" in command or "what is" in command:
            #     query = command
            #     answer = computational_intelligence(query)
            #     speak(answer)







startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)


    # def run(self):
    #     self.TaskExection
    def startTask(self):
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/live_wallpaper.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/initiating.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000) 
        startExecution.start()
    
    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())
        
