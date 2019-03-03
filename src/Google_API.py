import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types as image_types
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import texttospeech

# Instantiates a client
speech_client = speech.SpeechClient()


def annotate_image(image_file_name):
    # Instantiates a client
    vision_client = vision.ImageAnnotatorClient()
    # Loads the image into memory
    with io.open(image_file_name, 'rb') as image_file:
        content = image_file.read()

    image = image_types.Image(content=content)

    # Performs label detection on the image file
    response = vision_client.label_detection(image=image)
    labels = response.label_annotations
    result = {"labels": labels}
    return result


def text_speech(text_dict):
    client = texttospeech.TextToSpeechClient()
    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    for key, value in text_dict.items():
        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        synthesis_input = texttospeech.types.SynthesisInput(text=value)
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        # The response's audio_content is binary.
        with open(os.path.join('resources/audio', str(key)+'.mp3'), 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)


def speech_text(speech_content):
    audio = types.RecognitionAudio(content=speech_content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='en-US')

    # Detects speech in the audio file
    response = speech_client.recognize(config, audio)
    api_results = []
    for result in response.results:
        [api_results.append(alt.transcript) for alt in result.alternatives]
    return api_results
