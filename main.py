import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import openai
import pywhatkit

from config import apikey
from BrainAi import ReplyBrain


chatStr = ""
# https://youtu.be/Z3ZAJoi4x6Q

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey

    chatStr += f"You: {query}\nFreddy: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(chatStr)
    # print(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']} \n"
    speak(response["choices"][0]["text"])

    return response["choices"][0]["text"]




# def ai(prompt):
#     openai.api_key = apikey
#     text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
#
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=prompt,
#         temperature=0.7,
#         max_tokens=256,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#     # todo: Wrap this inside of a  try catch block
#     # print(response["choices"][0]["text"])
#     text += response["choices"][0]["text"]
#     if not os.path.exists("Openai"):
#         os.mkdir("Openai")
#
#     # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
#     with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
#         f.write(text)

def speak(text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voices', voices[0].id)
    engine.setProperty('rate', 180)
    # print("")
    # # print(f"You : {text}.")
    # print("")
    engine.say(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            # print(f"You : {query.upper()}")
            return query
        except Exception as e:
            return "Some Error Occured. Please Try Again."


if __name__ == '__main__':
    speak("Hello Sir! I am Freddy your Virtual Assistant. How may I help you.")
    while 1:
        print("listening...")
        query = takecommand()
        # speak(query)

        # --------------  WEBSITES  ------------------
        sites = [["youtube", "https://www.youtube.com/"],
                 ["google", "https://www.google.co.in/"],
                 ["wikipedia", "https://www.wikipedia.org/"],
                 ["geeks for geeks", "https://www.geeksforgeeks.org/"],
                 ["w3school", "https://www.w3schools.com/"],
                 ["romantic songs on youtube", "https://www.youtube.com/watch?v=gErAmJR1UOk"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                webbrowser.open(site[1])
                speak(f"Opening {site[0]} Sir")

        # --------------  SONGS AS GENRES ON YT  ------------------
        songs = [["romantic songs on youtube", "https://www.youtube.com/watch?v=gErAmJR1UOk"],
                 ["sad songs on youtube", "https://www.youtube.com/watch?v=z-diRlyLGzo&list=PL9khxBZiiQwoKEqdTrb4ip"
                                          "-S_Tov6FkBQ"],
                 ["soothing songs on youtube", "https://www.youtube.com/watch?v=SQ1ED8-tBpE"],
                 ["punjabi songs on youtube", "https://www.youtube.com/watch?v=mZQH8CPQ-wo&list"
                                              "=RDCMUCsaXTlOmt0o9aGeC_n_r8VQ&start_radio=1"]]
        for song in songs:
            if f"Play {song[0]}".lower() in query.lower():
                webbrowser.open(song[1])
                speak(f"Playing {song[0]} Sir")

        # --------------  SONGS BY NAME ON YT ------------------

        # --------------  SONGS BY NAME IN MEMORY ------------------



        if "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir the time is {strfTime}")

        elif "on youtube".lower() in query.lower():
            speak("Ok Sir, This is what I found for your search!")
            query = query.replace("Freddy", "")
            query = query.replace("search", "")
            query = query.replace("on youtube", "india")
            query = query.replace("open", "")
            link = 'https://www.youtube.com/results?search_query=' + query
            webbrowser.open(link)
        #
        # elif " youtube search".lower() in query.lower():
        #     # query = query.replace(" on Youtube", "")
        #     query = query.replace("Freddy", "")
        #     query = query.replace("youtube search", "")
        #     query = query.replace("open", "")
        #     query = query.replace("search", "")
        #
        #     link = 'https://www.youtube.com/results?search_query=' + query
        #     webbrowser.open(link)
        #     speak("Ok Sir! This is what I found for your search.")

        elif 'on google'.lower() in query.lower():
            speak("Ok Sir! This is what I found for your search.")
            query = query.replace("Freddy","")
            query = query.replace("search","")
            query = query.replace("on google","")
            pywhatkit.search(query)

        elif "Freddy stop".lower() in query.lower():
            speak("Ok, quitting now. Goodbye!")
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        elif "play".lower() in query.lower():
            musics = [["heeriye", "Songs/Heeriye.mp3"],
                      ["ek zindagi", "Songs/Ek_zindagi.mp3"],
                      ["skechers", "Songs/Skechers.mp3"],
                      ["starboy", "Songs/Starboy.mp3"],
                      ["jannatein kahan", "Songs/Jannatein_Kahan.mp3"]
                      ]
            for music in musics:
                if f"Play {music[0]}".lower() in query.lower():
                    music_path = music[1]
                    os.system(f" start {music_path}")
                    speak(f"Playing {music[0]} Sir")
        else:
            chat(query)
