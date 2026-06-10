# ...existing code...
import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import re
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chatStr = ""
# https://youtu.be/Z3ZAJoi4x6Q
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Harry: {query}\nEcho: "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    except Exception as e:
        print("OpenAI request failed:", e)
        return "Sorry, I couldn't reach the AI service."

    text = response["choices"][0]["text"].strip()
    say(text)
    chatStr += f"{text}\n"
    return text
# ...existing code...
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    except Exception as e:
        print("OpenAI request failed:", e)
        return

    text += response["choices"][0]["text"].strip()
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # Safe filename derived from prompt; fallback to random id
    safe = re.sub(r'[^A-Za-z0-9 _-]', '', prompt).strip()
    filename = safe[:50] or str(random.randint(1, 10**9))
    with open(f"Openai/{filename}.txt", "w", encoding="utf-8") as f:
        f.write(text)
# ...existing code...
def say(text):
    # cross-platform TTS: use macOS 'say' if available, else pyttsx3 if installed, else print
    try:
        if os.name == "posix" and os.uname().sysname == "Darwin":
            os.system(f'say "{text}"')
        else:
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except Exception:
                print(text)
    except Exception:
        print(text)
# ...existing code...
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            print("Listening...")
            audio = r.listen(source, timeout=6, phrase_time_limit=8)
        except Exception as e:
            print("Listening timed out or failed:", e)
            return ""
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Speech recognition service error:", e)
        return ""
    except Exception as e:
        print("Recognition error:", e)
        return ""
# ...existing code...
if __name__ == '__main__':
    print('Welcome to Echo A.I')
    say("Echo A.I")
    while True:
        query = takeCommand()
        if not query:
            continue
        q = query.lower()
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if site[0].lower() in q and ("open " + site[0]).lower() in q:
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                break

        # todo: Add a feature to play a specific song
        elif_clause_executed = False
        if "open music" in q:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            if os.path.exists(musicPath):
                os.system(f"open {musicPath}")
            else:
                say("Music file not found.")
            elif_clause_executed = True

        if not elif_clause_executed:
            if "the time" in q:
                hour = datetime.datetime.now().strftime("%H")
                minute = datetime.datetime.now().strftime("%M")
                say(f"Sir time is {hour} bajke {minute} minutes")
            elif "open facetime" in q:
                os.system("open /System/Applications/FaceTime.app")
            elif "open pass" in q:
                os.system("open /Applications/Passky.app")
            elif "using artificial intelligence" in q or "artificial intelligence" in q:
                ai(prompt=query)
            elif "Echo quit" in q or "quit Echo" in q:
                exit()
            elif "reset chat" in q:
                chatStr = ""
            else:
                print("Chatting...")
                chat(query)
# ...existing code...