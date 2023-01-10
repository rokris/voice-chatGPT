"""
A chatbot that uses speech recognition and OpenAI's GPT-3 to generate responses.
The chatbot prompts the user for input, generates a response using the user's input
and conversation history, prints and speaks the response.
"""

import os
import sys

import api_secret
import openai
import speech_recognition as sr
from google.cloud import texttospeech


"""
An api_secret.py must be create.
The secret API key variabel must be collected from OpenAI and entered into the file.
"""
openai.api_key = api_secret.API_KEY
GOOGLE_API_KEY = api_secret.GOOGLE_API_KEY

recognizer = None
ttsclient = None


def initialize():
    """Initializes the pyttsx3 engine and speech_recognition recognizer global variables.
    These variables are only initialized if they have not been initialized before."""
    global engine, recognizer, ttsclient
    if recognizer is None and ttsclient is None:
        recognizer = sr.Recognizer()
        ttsclient = texttospeech.TextToSpeechClient(client_options={"api_key": GOOGLE_API_KEY})


def get_audio_input():
    """Prompts the user to speak into the microphone and records their input.
    Prints "Mikrofonen er aktiv... (si ordet 'avbryt' for å avslutte programmet)"
    while it is listening, and "Mikrofonen er slått av igjen..." when it is finished.
    Returns the recorded audio."""
    with sr.Microphone() as source:
        print("Mikrofonen er aktiv... (si ordet 'avbryt' for å avslutte programmet)")
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

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=response_text)
        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = ttsclient.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        # The response's audio_content is binary.
        with open("output.mp3", "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')


if __name__ == "__main__":
    main()
