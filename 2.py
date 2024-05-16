import pyaudio
import base64
import requests

# Set parameters
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1  # Mono channel
RATE = 44100  # 44.1kHz sampling rate
CHUNK = 1024  # 1024 samples per frame
RECORD_SECONDS = 3  # Record for 3 seconds

# Shazam API endpoint and your API key
SHAMAZAM_API_ENDPOINT = "https://shazam.p.rapidapi.com/songs/detect"

# Initialize pyaudio
audio = pyaudio.PyAudio()

# Start Recording
stream = audio.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)
print("Recording...")

frames = []

# Record for the specified number of chunks
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# Stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

# Combine the frames and convert to raw PCM bytes
raw_pcm_data = b"".join(frames)

# Convert raw PCM data to Base64 string
base64_string = base64.b64encode(raw_pcm_data).decode("utf-8")

# Prepare the payload for Shazam API
payload = {"encoded_audio": base64_string}

# Send request to Shazam API
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "ff7711ae85msh7c32a1d09f8b33ap1c2075jsn58e69dd603d5",
    "X-RapidAPI-Host": "shazam.p.rapidapi.com",
}

response = requests.post(SHAMAZAM_API_ENDPOINT, json=payload, headers=headers)

# Check response
if response.status_code == 200:
    result = response.json()
    print("Song recognized!")
    print(result)
else:
    print(f"Failed to recognize song: {response.status_code} - {response.text}")
