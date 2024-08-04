from flask import Flask, render_template, request, redirect, url_for,jsonify
import os
import pyaudio
import wave

app = Flask(__name__)

def record_audio_to_file(filename, duration=1, channels=1, rate=44100, frames_per_buffer=1):
    """Record user's input audio and save it to the specified file."""
    FORMAT = pyaudio.paInt16
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=FORMAT, channels=channels, rate=rate, frames_per_buffer=frames_per_buffer, input=True)
    print("Start recording...")

    frames = []
    # Record for the given duration
    for _ in range(0, int(rate / frames_per_buffer * duration)):
        data = stream.read(frames_per_buffer)
        frames.append(data)
    print("Recording stopped")
    stream.stop_stream()
    stream.close()
    p.terminate()
    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Audio recorded and saved to {filename}")
    return filename

@app.route('/')
def index():
     return render_template('index.html')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    data = request.get_json()
    username = data['username']
    directory = "C:\\Users\\user\\Desktop\\recordings"

    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Find the next available filename
    file_count = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name)) and name.startswith(username)])
    output_file = os.path.join(directory, f"{username}{file_count:02d}.wav")

    # Call the function to record audio
    record_audio_to_file(output_file)
    return jsonify({'message': 'Recording saved', 'filepath': output_file})

if __name__ == '__main__':
    app.run(debug=True)