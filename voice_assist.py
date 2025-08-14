import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except Exception:
        print("Sorry, I did not catch that.")
        speak("Sorry, I did not catch that. Please say that again.")
        return ""

def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

def tell_date():
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today is {today}")

def assistant():
    speak("Hello! How can I help you?")
    while True:
        command = listen_command()

        if 'hello' in command or 'hi' in command:
            speak("Hello! How are you?")
        elif 'time' in command:
            tell_time()
        elif 'date' in command:
            tell_date()
        elif 'search' in command:
            # Extract search query after the word 'search'
            search_term = command.split('search', 1)[1].strip()
            speak(f"Searching for {search_term}")
            url = f"https://google.com/search?q={search_term}"
            webbrowser.open(url)
        elif 'exit' in command or 'quit' in command:
            speak("Goodbye!")
            break
        elif command:
            speak("Sorry, I am not programmed to do that yet.")

if __name__ == "__main__":
    assistant()
