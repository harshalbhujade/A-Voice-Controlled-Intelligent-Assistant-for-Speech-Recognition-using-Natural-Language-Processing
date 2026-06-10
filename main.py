import speech_recognition as sr
import os
import webbrowser
from config import apikey
import datetime
import random
import numpy as np
import wikipedia
wikipedia.set_lang("en")
#from openai import OpenAI
#from config import apikey

import requests
from config import news_api


chatStr = ""


def chat(query):
    global chatStr
    chatStr += f"User: {query}\nAssistant: "

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": query}
            ]
        )

        text = response.choices[0].message.content
        say(text)
        chatStr += text + "\n"
        return text

    except Exception as e:
        print("OpenAI error:", e)
        say("Sorry, I couldn't reach the A I service.")
        return ""

    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def get_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api}"
        response = requests.get(url)
        data = response.json()

        print("FULL DATA:", data)  # DEBUG

        if data["status"] != "ok":
            say("Sorry, I could not fetch news")
            return

        articles = data.get("articles", [])

        if not articles:
            say("No news available right now")
            return

        say("Here are the top news headlines")

        for i, article in enumerate(articles[:5]):
            headline = article.get("title", "")

            if headline:
                print(f"{i+1}. {headline}")
                say(headline)

    except Exception as e:
        print("News error:", e)
        say("Sorry, something went wrong while fetching news")

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return ""
def ai_reply(query):
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=query
        )

        answer = response.output_text
        print(answer)
        say(answer)

    except Exception as e:
        print("Error:", e)
        say("Sorry, I could not connect to AI service.")
def process_query(query):
    query = query.lower()
    if not query:
        return ""
        
    if "safari" in query and "search" in query:
        search = query.replace("search", "").replace("on safari", "").replace("in safari", "").strip()
        print("Safari search triggered:", search)
        if search:
            say(f"Searching for {search}")
            url = f"https://www.google.com/search?q={search}"
            os.system(f'open -a Safari "{url}"')
            return f"Searching Safari for {search}"
        else:
            say("What should I search?")
            return "What should I search?"

    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
    for site in sites:
        if f"open {site[0]}".lower() in query:
            say(f"Opening {site[0]} sir...")
            webbrowser.open(site[1])
            return f"Opening {site[0]}..."

    if "open music" in query:
        musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
        os.system(f"open {musicPath}")
        return "Opening music..."

    elif "the time" in query:
        hour = datetime.datetime.now().strftime("%H")
        minute = datetime.datetime.now().strftime("%M")
        response = f"Sir time is {hour} : {minute} minutes"
        say(response)
        return response

    elif "open facetime" in query:
        os.system("open /System/Applications/FaceTime.app")
        return "Opening FaceTime..."

    elif "open pass" in query:
        os.system("open /Applications/Passky.app")
        return "Opening Passky..."

    elif "using artificial intelligence" in query:
        ai(prompt=query)
        return "Processing with AI..."

    elif "echo stop" in query:
        return "EXIT"

    elif "reset chat" in query:
        global chatStr
        chatStr = ""
        return "Chat reset."

    elif "search youtube for" in query:
        search = query.replace("search youtube for", "").strip()
        say(f"Searching YouTube for {search}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={search}")
        return f"Searching YouTube for: {search}"

    elif "search google for" in query:
        search = query.replace("search google for", "").strip()
        say(f"Searching Google for {search}")
        webbrowser.open(f"https://www.google.com/search?q={search}")
        return f"Searching Google for: {search}"

    elif "tell me a joke" in query:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why was the computer cold? Because it left its Windows open.",
            "Why do Java developers wear glasses? Because they don't see sharp.",
            "Why did the computer go to the doctor? Because it had a virus."
        ]
        joke = random.choice(jokes)
        say(joke)
        return joke

    elif "weather" in query:
        city = query.replace("weather", "").strip()
        say(f"Showing weather for {city}")
        webbrowser.open(f"https://www.google.com/search?q=weather+{city}")
        return f"Showing weather for {city}"

    elif "news" in query or "latest news" in query:
        get_news()
        return "Fetching the top news headlines..."

    elif "play" in query:
        song = query.replace("play", "").strip()
        say(f"Playing {song} on YouTube")
        url = f"https://www.youtube.com/results?search_query={song}"
        os.system(f'open -a Safari "{url}"')
        return f"Playing {song} on YouTube..."

    elif "battery" in query:
        try:
            import subprocess
            output = subprocess.check_output("pmset -g batt", shell=True).decode()
            import re
            battery = re.search(r'(\d+)%', output).group(1)
            response = f"Battery is {battery} percent"
            say(response)
            return response
        except Exception as e:
            print("Battery error:", e)
            say("Sorry, I could not get battery status")
            return "Sorry, I could not get battery status."

    elif "date" in query:
        today = datetime.datetime.now().strftime("%d %B %Y")
        response = f"Today's date is {today}"
        say(response)
        return response

    elif "project" in query and "tell me" in query:
        say("We are a group of students working on a voice controlled intelligent assistant project.")
        say("Our project uses speech recognition, natural language processing, and automation to perform tasks.")
        say("The system can answer questions, fetch news, search, and interact with voice commands.")
        return "Explained project details."

    elif ("group" in query and "member" in query) or "guide" in query:
      say("Our project group consists of dedicated students from the Information Technology department.")
      say("The group leader is Harshal Bhujade.")
      say("The team members include Aryan Dhabaale, Rohit Dhandhe, Ansh Khaadase, and Mohit Kamdi.")
      say("We are grateful to be guided by our respected mentor, Mrs Saroj Shambharkar ma'am, who is the Head of the Information Technology department.")
      say("Under her guidance, we have successfully developed a voice controlled intelligent assistant named Echo.")

      return "Group members mentioned."

    else:
        try:
            clean_query = query.replace("who is", "").replace("what is", "").strip()
            print("Searching Wikipedia:", clean_query)
            if not clean_query:
                say("Please ask properly")
                return "Please express your question well."

            say("Let me check that")
            result = wikipedia.summary(clean_query, sentences=2)
            print(result)
            say(result)
            return result
        except Exception as e:
            print("Wiki error:", e)
            say("Sorry, I could not find information")
            return "Sorry, I could not find information on Wikipedia."

if __name__ == '__main__':
    print('Welcome to Echo A.I')
    say("Echo A.I")
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        say("Good morning")
    elif hour < 18:
        say("Good afternoon")
    else:
        say("Good evening")

    while True:
        print("Listening...")
        q = takeCommand()
        res = process_query(q)
        if res == "EXIT":
            break