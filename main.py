import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import subprocess
from urllib.parse import quote_plus


# ---------------------------------
# 1. START JARVIS
# ---------------------------------

recognizer = sr.Recognizer()
speaker = pyttsx3.init()

speaker.setProperty("rate", 175)
speaker.setProperty("volume", 1.0)


# ---------------------------------
# 2. MAKE JARVIS SPEAK
# ---------------------------------

def speak(message):
    print("JARVIS:", message)
    speaker.say(message)
    speaker.runAndWait()


# ---------------------------------
# 3. LISTEN TO YOUR VOICE
# ---------------------------------

def listen():
    with sr.Microphone() as source:
        print("\nListening... Speak now.")

        recognizer.adjust_for_ambient_noise(
            source, duration=0.5
        )

        try:
            audio = recognizer.listen(
                source, timeout=8, phrase_time_limit=8
            )

            print("Understanding your voice...")

            command = recognizer.recognize_google(audio)
            command = command.lower()

            print("You said:", command)
            return command

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

        except sr.UnknownValueError:
            speak("Sorry, I could not understand.")
            return ""

        except sr.RequestError:
            speak("Speech recognition needs an internet connection.")
            return ""

        except OSError:
            speak("I cannot access the microphone.")
            return ""


# ---------------------------------
# 4. UNDERSTAND COMMANDS
# ---------------------------------

def execute_command(command):

    if not command:
        return True

    # Tell the current time
    if "time" in command:
        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )
        speak("The time is " + current_time)

    # Tell today's date
    elif "date" in command or "today" in command:
        today = datetime.datetime.now().strftime(
            "%d %B %Y"
        )
        speak("Today's date is " + today)

    # Open YouTube
    elif "youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    # Open Google
    elif "google" in command and "search" not in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    # Search Google for a topic
    elif "search" in command:
        topic = command.replace("search", "", 1).strip()

        if topic.startswith("for "):
            topic = topic[4:].strip()

        if topic:
            speak("Searching Google for " + topic)
            url = "https://www.google.com/search?q=" + quote_plus(topic)
            webbrowser.open(url)
        else:
            speak("Please say what you want to search for.")

    # Open Notepad
    elif "notepad" in command:
        speak("Opening Notepad.")
        subprocess.Popen(["notepad.exe"])

    # Open Calculator
    elif "calculator" in command:
        speak("Opening Calculator.")
        subprocess.Popen(["calc.exe"])

    # Answer a basic identity question
    elif "your name" in command or "who are you" in command:
        speak("I am Jarvis, your personal AI assistant.")

    # Exit the assistant
    elif any(word in command for word in [
        "stop jarvis", "exit jarvis", "quit jarvis",
        "shutdown jarvis"
    ]):
        speak("Goodbye. Jarvis is shutting down.")
        return False

    # Unknown command
    else:
        speak("I do not know that command yet.")

    return True


# ---------------------------------
# 5. MAIN PROGRAM
# ---------------------------------

def main():
    speak("Hello, I am Jarvis, your personal AI assistant.")
    speak("Say Jarvis followed by a command.")

    running = True

    while running:
        command = listen()

        if not command:
            continue

        # Respond only when the wake word is spoken
        if "jarvis" in command:
            command = command.replace("jarvis", "", 1).strip()

            if not command:
                speak("Yes, how can I help you?")
                continue

            running = execute_command(command)

        else:
            print("Say Jarvis before your command.")


# ---------------------------------
# 6. RUN THE PROGRAM
# ---------------------------------

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nJARVIS stopped.")
    except Exception as error:
        print("An unexpected error occurred:", error)