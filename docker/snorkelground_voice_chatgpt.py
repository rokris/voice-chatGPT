"""
A chatbot that uses speech recognition and OpenAI's GPT-3 to generate responses.
The chatbot prompts the user for input, generates a response using the user's input
and conversation history, prints and speaks the response.
"""

import os
import sys
from contextlib import contextmanager

import api_secret
import openai
import pyttsx3
import speech_recognition as sr

"""
An api_secret.py must be create.
The secret API key variabel must be collected from OpenAI and entered into the file.
"""
openai.api_key = api_secret.API_KEY

engine = None
recognizer = None


def initialize():
    """Initializes the pyttsx3 engine and speech_recognition recognizer global variables.
    These variables are only initialized if they have not been initialized before."""
    global engine, recognizer
    if engine is None and recognizer is None:
        engine = pyttsx3.init()
        recognizer = sr.Recognizer()


@contextmanager
def suppress_stdout():
    """A context manager that temporarily suppresses stdout."""
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def get_audio_input():
    """Prompts the user to speak into the microphone and records their input.
    Prints "Mikrofonen er aktiv... (si ordet 'avbryt' for å avslutte programmet)"
    while it is listening, and "Mikrofonen er slått av igjen..." when it is finished.
    Returns the recorded audio."""
    print("Mikrofonen er aktiv... (si ordet 'avbryt' for å avslutte programmet)")
    with suppress_stdout():
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)
    print("Mikrofonen er slått av igjen...")
    return audio


def recognize_speech(audio):
    """Takes in recorded audio and attempts to recognize it using Google's speech recognition API.
    Returns the recognized text if successful, or an error message if unsuccessful."""
    with open(os.devnull, "w") as devnull:
        user_input = None
        old_stdout = sys.stdout
        try:
            sys.stdout = devnull
            user_input = recognizer.recognize_google(
                audio, language="no-NO", show_all=False
            )
        except sr.UnknownValueError:
            return "Sorry, I could not recognize your voice!"
        except sr.RequestError:
            return "Error processing request!"
        finally:
            sys.stdout = old_stdout
            return user_input


def generate_response(prompt):
    """Takes in a prompt string and uses OpenAI's GPT-3 model to generate a response.
    Returns the generated response as a string."""
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, max_tokens=1000
    )
    response_text = response["choices"][0]["text"].replace("\n", "")
    response_text = response_text.split("Snorkeladmin:", 1)[0]
    return response_text


def main():
    """Main function for the chatbot.
    Initializes the chatbot, prompts the user for input, generates a response,
    prints and speaks the response, and appends the response to the conversation history.
    Repeats this process in an infinite loop unitll the word "avbryt" is spoken."""
    initialize()
    conversation = ""
    user_name = "Roger"
    while True:
        audio = get_audio_input()
        user_input = recognize_speech(audio)
        if user_input is None:
            continue
        elif user_input == "avbryt":
            print("Stopper Snorkelground chatGPT, velkommen tilbake.")
            raise SystemExit
        prompt = f"{user_name}: {user_input}\nSnorkeladmin:"
        conversation += prompt
        while True:
            response_text = generate_response(conversation)
            if response_text:
                break
            print("Beklager, jeg kunne ikke gi deg et svar. Prøv igjen.")
        conversation += f" {response_text}\n"
        print(conversation)

        engine.say(response_text)
        engine.runAndWait()


if __name__ == "__main__":
    main()
