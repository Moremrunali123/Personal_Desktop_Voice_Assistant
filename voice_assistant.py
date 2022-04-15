#import json
import random
import datetime
#from urllib.request import urlopen

import pyttsx3
import os
#import time
import subprocess

import requests
import wolframalpha
import speech_recognition as sr
import pywhatkit
import wikipedia
import re
import webbrowser
from requests import get
#from selenium import webdriver
import winshell
import pyjokes
#import feedparser
import smtplib
import ctypes
import time
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
#from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from PyQt5.QtGui import *
#from PyQt5.uic import loadUiType
from assistantUi import Ui_assistantUi
#from ecapture import ecapture as ec
import sys

#engine = pyttsx3.init()
#engine.setProperty('rate', 130)  # to setting up new voice rate
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[1].id)
#engine.setProperty('voice', voices[len(voices)-1].id)
engine.setProperty('rate', 150)  # to setting up new voice rate



def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def greet():
    # greets the user with a random phrase from A
    A = ["Hi,nice to meet you", "Nice to meet you", "hey,nice to meet you", "good to meet you!"]
    b = random.choice(A)
    speak(b)


def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")
    if hour == 0 and hour <= 12:
        speak(f"Good morning, its {tt}")

    elif hour >= 12 and hour <= 18:
        speak(f"Good afternoon , its {tt}")

    else:
        speak(f"Good evening , its {tt}")
    speak("I am Alexa sir. What can i do for you?")

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('mahirat71845@gmail.com','Mahirat@71845')
    server.sendmail('moremrunali209official@gmail.com',to,content)
    server.close()

def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=b08df5c868cd487ba40231e8d912ba84'
    main_page = requests.get(main_url).json()
    #print(main_page)
    articles = main_page["articles"]
    #print("articles")
    head = []
    #day = ["first","second","third","fourth","fifth","sixth","seventh","eight","ninth","tenth"]
    day = ["first","second","third","fourth","fifth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)) :
        speak(f"today's {day[i]} news is {head[i]}")



class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def takeCommand(self):

        r = sr.Recognizer()

        with sr.Microphone() as source:
            # speak("Listening.............")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source,timeout=15,phrase_time_limit=15)

        try:
            print("Recognizing..........")
            query = r.recognize_google(audio, language="en-IN")
        # print(f"User said: {query}\n")

        except Exception as e:
            print(e)
            speak("Say that again please.....")
            return "None"
        query = query.lower()
        return query

    def TaskExecution(self):
        """textspeak = '''Hello, I am Alexa. Your personal Assistant.
                        I am here to make your life easier. You can command me to perform
                        various tasks such as calculating sums or opening applications etcetra'''
        speak(textspeak)
        speak("What's your name, Human?")
        name = self.takeCommand()
        speak("Hello, " + name + '.')"""
        wish()


        # greet()
        #speak("I am Alexa sir. What can i do for you?")
        while True:

            self.query = self.takeCommand().lower()
            # logic for executing task based on query

            if "calculate" in self.query:
                app_id ="J2PUL5-6KAK9PVQH7"
                client = wolframalpha.Client(app_id)
                indx = self.query.lower().split().index('calculate')
                query = self.query.split()[indx + 1:]
                res = client.query(' '.join(query))
                answer = next(res.results).text
                print(f"The answer is {answer}")
                speak(f"The answer is {answer}")

            elif "open notepad" in self.query:
                speak("Opening notepad")
                npath = "C:\\Windows\\system32\\notepad.exe"
                os.startfile(npath)

            elif "close notepad" in self.query:
                speak("Okay sir, closing notepad")
                os.system("taskkill /f /im notepad.exe")

            elif "open command prompt" in self.query:
                speak("Opening command prompt")
                os.system("start cmd")

            elif "close command prompt" in self.query:
                speak("Okay sir, closing command prompt")
                os.system("taskkill /f /im cmd.exe")

            elif 'open visual studio code' in self.query:
                path = "C:\\Users\\space\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(path)


   #         elif "camera" in query or "take a photo" in query:
    #            ec.capture(0, "Jarvis Camera ", "img.jpg")

            elif 'play music' in self.query:
                music_dir = "C:\\songs"
                songs = os.listdir(music_dir)
                # rd = randome.choice(songs)
                for song in songs:
                    if song.endswith('.mp3'):
                        os.startfile(os.path.join(music_dir, song))

            elif 'ip address' in self.query:
                ip = get("https://api.ipify.org").text
                speak(f"Your IP address is {ip}")

            elif 'how are you' in self.query:
                speak("I am fine, what about you?")

            elif 'fine' in self.query or 'also fine' in self.query:
                speak("It's greate, glad to meet you")

            elif 'where i am' in self.query or 'where we are' in self.query:
                speak("wait sir, let me check")
                try:
                    ipAdd = requests.get("https://api.ipify.org").text
                    print(ipAdd)
                    url = "https://get.geojs.io/v1/ip/geo/"+ipAdd+'.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    city = geo_data['city']
                    state = geo_data['state']
                    country = geo_data['country']
                    speak(f"sir i am not sure, but i think we are in {city}city of {state} state of {country} country")
                except Exception as e:
                    speak("sorry sir, Due to network issue i am not able to find where we are.")
                    pass

            if 'wikipedia' in self.query:
                speak("Searching wikipedia...........")
                query = self.query.replace("Wikipedia", "")  # if give command to Shivaji Maharaj wikipedia then
                                                                    # it search query='Shivaji Maharaj'
                results = wikipedia.summary(query, sentences=3)
                speak("According to wikipedia")
                print(results)
                speak(results)

            elif 'open youtube' in self.query:
                webbrowser.open("www.youtube.com")

            elif 'open google' in self.query:
                speak("sir, What should i search on google")
                cm = self.takeCommand().lower()
                webbrowser.open(f"{cm}")

            elif "play youtube video" in self.query or "play video" in self.query:
                speak("opening youtube please wait")
                query = self.query.replace("play youtube video", "")
                try:

                    # it plays a random YouTube
                    # video of GeeksforGeeks
                    pywhatkit.playonyt(self.query)
                    speak("Playing...")
                except:
                    # printing the error message
                    speak("Network Error Occured")

            elif 'send whatsapp message' in self.query:
                try:
                    speak("sending a whatsapp message please wait")
                    # sending message to reciever
                    # using pywhatkit
                    pywhatkit.sendwhatmsg("+91XXXXXXXXXX",
                                          "Hello from Alexa",
                                          2, 50)
                    speak("Successfully Sent!")

                except:

                    # handling exception
                    # and printing error message
                    print("An Unexpected Error!")

            elif 'open website' in self.query:
                reg_ex = re.search('open website (.+)', self.query)
                if reg_ex:
                    domain = reg_ex.group(1)
                    print(domain)
                    url = 'https://www.' + domain
                    webbrowser.open(url)
                    speak('The website you have requested has been opened for you')
                else:
                    pass



            elif 'search' in self.query:
                try:
                    speak("searching in google please wait")
                    query = self.query.replace("search", "")
                    # it will perform the Google search
                    pywhatkit.search(query)
                except:

                    # Printing Error Message
                    speak("An unknown error occured")

            elif 'email to' in self.query:
                try:
                    speak("What should I say")
                    content = self.takeCommand().lower()
                    to = "mahirat71845@gmail.com"
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    print("Sorry. I am not able to send this Email")

            elif "question" in self.query:
                speak("Sure sir, you can ask questions to me")
                # Taking input from user
                question = self.takeCommand().lower()

                # App id obtained by the above steps
                app_id = 'J2PUL5-6KAK9PVQH7'

                # Instance of wolf ram alpha
                # client class
                client = wolframalpha.Client(app_id)

                # Stores the response from
                # wolf ram alpha
                res = client.query(question)

                # Includes only text from the response
                answer = next(res.results).text
                speak(answer)
                print(answer)



            elif 'the time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is :{strTime}")

            elif 'weather' in self.query:

                api_key = "0fd494513a9a547ebc2ead5090f170b4"
                base_url = "https://home.openweathermap.org/api_key"
                speak("City Name")
                print("City name:")
                city_name = self.takeCommand()
                complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                response = requests.get(complete_url)
                x = response.json()

                if x["cod"] != "404":
                    y = x["main"]
                    current_temperature = y["temp"]
                    current_pressure = y["pressure"]
                    current_humidiy = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    print("temperature (in kelvin unit)=" + str(current_temperature)+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description))

                else:
                    speak("City not found")


            elif "who made you" in self.query or "created you" in self.query:
                text = "I have been created by Human."
                speak(text)

            elif 'joke' in self.query:
                speak(pyjokes.get_joke())

            elif "don't listen" in self.query or "stop listening" in self.query:
                speak("for how much time you want to stop alexa from listening commands")
                a = int(self.takeCommand())
                time.sleep(a)

            elif "where is" in self.query:
                query = self.query.replace("where is", "")
                location = query
                speak("User asked to Locate")
                speak(location)
                webbrowser.open("https://www.google.nl / maps / place/" + location + "")

            elif 'lock window' in self.query:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()

            elif 'shutdown system' in self.query:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                #subprocess.call('shutdown / p /f')
                os.system("shutdown /s /t 5")

            elif "restart" in self.query:
                subprocess.call(["shutdown", "/r"])
                # os.system("shutdown /r /t 5")

            elif "sleep the system" in self.query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif "hibernate" in self.query:
                speak("Hibernating")
                subprocess.call("shutdown / h")

            elif 'empty recycle bin' in self.query:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
                speak("Recycle Bin Recycled")



            elif "log off" in self.query or "sign out" in self.query:
                speak("Make sure all the application are closed before sign-out")
                time.sleep(5)
                subprocess.call(["shutdown", "/l"])

            elif "write a note" in self.query:
                speak("What should i write, sir")
                note = self.takeCommand()
                file = open('alexa.txt', 'w')
                speak("Sir, Should i include date and time")
                snfm = self.takeCommand()
                if 'yes' in snfm or 'sure' in snfm:
                    strTime = datetime.datetime.now().strftime("% H:% M:% S")
                    file.write(strTime)
                    file.write(" :- ")
                    file.write(note)
                else:
                    file.write(note)

            elif "show note" in self.query:
                speak("Showing Notes")
                file = open("alexa.txt", "r")
                print(file.read())
                speak(file.read(6))

            elif 'news' in self.query:

                try:
                    speak("please wait sir, fetching the latest news")
                    speak('here are some top news from the times of india')
                    news()
                except Exception as e:
                    print(str(e))

            elif 'you can sleep' in self.query or 'bye' in self.query:
                speak("thanks for using me, have a good day")
                # sys.exit()
                break
            speak("sir, do you have any other work")


startExecution = MainThread()
#m = MainThread()
#m.TaskExecution()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_assistantUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("7LP8.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("T8bahf.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        speak("Hello")
        speak("initiating system wait")
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
