import pyaudio
import keyboard
import tempfile
import wave
from openai import OpenAI
from dotenv import load_dotenv
import os

# Parameters for recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
HOTKEY_START = "ctrl+alt+l"
HOTKEY_STOP = "ctrl+alt+s" 
load_dotenv()
client = OpenAI()

def start_recording():
    audio = pyaudio.PyAudio()
    
    recorded_data = None  # This will store the audio data
    
    while True:
        if keyboard.is_pressed(HOTKEY_START):
            print("Recording started...")
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                                rate=RATE, input=True,
                                frames_per_buffer=CHUNK)
            frames = []

            # Keep recording until 's' is pressed
            while not keyboard.is_pressed(HOTKEY_STOP):
                data = stream.read(CHUNK)
                frames.append(data)

            print("Recording stopped.")
            
            # Stop and close the stream 
            stream.stop_stream()
            stream.close()
            # Terminate the PortAudio interface
            audio.terminate()
            
            # Store the audio data in the recorded_data variable
            recorded_data = b''.join(frames)
            break

    # Generate a unique filename for the temporary WAV file
    temp_filename = tempfile.mktemp(suffix=".wav")

    # Save the audio data to the temporary WAV file
    with wave.open(temp_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recorded_data)

    # Re-open the temporary file in binary read mode for transcription
    with open(temp_filename, 'rb') as f:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format='json'
        )

    # Clean up by removing the temporary file
    os.remove(temp_filename)

    return response.text

