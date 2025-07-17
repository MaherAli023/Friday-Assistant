import pyttsx3
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import os
import smtplib
import pywhatkit as kt
from selenium import webdriver
import time
from tkinter import *
from tkinter import messagebox
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import sys
from dadjokes import Dadjoke



#Setting up voice from Microsoft
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
r = sr.Recognizer()

def Login_Info():
    user_name = e1.get()
    password = e2.get()
 
    # if(user_name == "" and password == "") 
 
 
    if(user_name == "Maher" and password == "1234"):
 
        messagebox.showinfo("","Login Successful!")
        root.destroy()
 
    else :
        messagebox.showinfo("","Incorrect Username and Password")

def on_close():
    response = messagebox.showwarning('Warning','Please enter correct login details')

root = Tk()
root.title("Login: Friday")
#root.iconbitmap('C:\\Users\\syedm\\OneDrive\\Desktop\\Friday-Voice-Assistant\\fridayLogo.ico') 

root.protocol('WM_DELETE_WINDOW',on_close)


root.geometry("450x250")
global e1
global e2
 
Label(root, text="User name").place(x=10, y=10)
Label(root, text="Password").place(x=10, y=40)
 
e1 = Entry(root)
e1.place(x=140, y=10)
 
e2 = Entry(root)
e2.place(x=140, y=40)
e2.config(show="*")
 
 
Button(root, text="Login", command=Login_Info ,height = 2, width = 10).place(x=10, y=100)

root.mainloop()

#After login success, voice assistant starts

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    

def greeting():

    # Function to greet user according to the time
    
    hour = int(datetime.datetime.now().hour)

    if hour <12:
        speak("Good Morning!!")
        print("Good Morning!!")
    elif hour <18:
        speak("Good afternoon!!")
        print("Good afternoon!!")
    else:
        speak("Good Evening!!")
        print("Good Evening!!")

    speak("This is Friday, how may I help you?")
    print("This is Friday, how may I help you?")

        
def takeCommand():
    # It takes microphone input from the user and returns string output
    

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=6)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"
    return query
'''
while True:
    command = takeCommand()

    if "hi friday" in command or "hey friday" in command:
        speak("Hello! How can I help you?")
'''
def prompt_openrouter(prompt):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",   # Required
            "X-Title": "Friday-Assistant"         # Optional project name
        }

        data = {
            "model": "mistralai/mixtral-8x7b-instruct",   # ✅ Valid model name
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        print("Error with OpenRouter:", e)
        return "Sorry, there was a problem in response."


speak_count = 0

if __name__ == "__main__":
    '''
    This is the main function of the program
    '''
    greeting()

    while speak_count < 10:
        user_command = takeCommand().lower()
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        # Logic for executing tasks based on query
        if 'wikipedia' in user_command:
            speak('Searching Wikipedia...')
            user_command = user_command.replace("wikipedia", "")
            results = wikipedia.summary(user_command, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'search google' in user_command:
            speak('Searching in Google...')
            user_command = user_command.replace("search google", "")
            kt.search(user_command)

        elif 'open youtube' in user_command:
            webbrowser.get(chrome_path).open("youtube.com")

        elif 'open google' in user_command:
            webbrowser.get(chrome_path).open("google.com")

        elif 'open github' in user_command:
            webbrowser.get(chrome_path).open("github.com")

        elif 'time' in user_command:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            print(f"Sir, the time is {strTime}")

        elif 'open spotify' in user_command:
            webbrowser.get(chrome_path).open("spotify.com")

        elif 'open control panel' in user_command:
            os.system("control panel")

        elif 'open calculator' in user_command:
            os.system("calc")


        elif 'in maps' in user_command:
            user_command = user_command.replace("search" and "in maps", "")
            driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get('https://www.google.com/maps/')
            searchBox = driver.find_element(By.ID, 'searchboxinput').send_keys(user_command + Keys.ENTER)
            time.sleep(30)
            driver.quit()
            
            
        elif 'cancel execution' in user_command:
            speak("Okay sir,cancelling execution.")
            exit()
   

        elif 'tell jokes' in user_command:
            dadjoke = Dadjoke()
            print(dadjoke.joke)
            speak(dadjoke.joke)

        elif 'news' in user_command:
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()

            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            for i,news in enumerate(news_list):
                print(news.title.text)
                speak(news.title.text)
                print(news.link.text)
                print(news.pubDate.text)
                speak(news.pubDate.text)
                print("-"*60)
                if i >=4:
                    break
        
        elif 'weather' in user_command:
            user_command = user_command.replace("weather", "")
            print(user_command)
            print('Displaying Weather report for: ' + user_command)
            url = 'https://wttr.in/{}'.format(user_command)
            res = requests.get(url)
            print(res.text)


        elif user_command.lower().startswith('friday'):
            try:
                prompt = user_command.lower().replace('friday', '').strip()

                if not prompt:
                    speak("I didn't catch your question. Try again.")
                    continue

                response = prompt_openrouter(prompt)
                print("OpenRouter’s response:", response)
                speak(response)

            except Exception as e:
                print("Error with OpenRouter:", e)
                speak("Sorry, I couldn't get a response.")

        
        elif 'memo' in user_command:

            def newTask():
                task = my_entry.get()
                if task != "":
                 lb.insert(END, task)
                 my_entry.delete(0, "end")
                else:
                 messagebox.showwarning("WARNING", "Please enter some task")

            def deleteTask():
                lb.delete(ANCHOR)
    
            root = Tk()
            # ws.geometry('500x450+500+200')
            root.geometry('800x650+800+400')
            root.title('To Do List: Friday')
            root.config(bg='#223441')
            root.resizable(width=False, height=False)

            frame = Frame(root)
            frame.pack(pady=10)

            lb = Listbox(
                frame,
                width=25,
                height=8,
                font=('Times', 18),
                bd=0,
                fg='#464646',
                highlightthickness=0,
                selectbackground='#a6a6a6',
                activestyle="none",
                )
            lb.pack(side=LEFT, fill=BOTH)

            task_list = []

            for item in task_list:
                lb.insert(END, item)

            sb = Scrollbar(frame)
            sb.pack(side=RIGHT, fill=BOTH)

            lb.config(yscrollcommand=sb.set)
            sb.config(command=lb.yview)

            my_entry = Entry(
                root,
                font=('times', 24)
                )

            my_entry.pack(pady=20)

            button_frame = Frame(root)
            button_frame.pack(pady=20)

            addTask_btn = Button(
                button_frame,
                text='Add Task',
                font=('times 14'),
                bg='#c5f776',
                padx=20,
                pady=10,
                command=newTask
            )
            addTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

            delTask_btn = Button(
                button_frame,
                text='Delete Task',
                font=('times 14'),
                bg='#ff8b61',
                padx=20,
                pady=10,
                command=deleteTask
            )
            delTask_btn.pack(fill=BOTH, expand=True, side=LEFT)
            root.mainloop()