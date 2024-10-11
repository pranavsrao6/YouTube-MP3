from flask import Flask, request, jsonify, send_file
from pytube import YouTube
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_video_to_mp3():
    data = request.get_json()
    youtube_url = data.get('url')

    if not youtube_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Download and convert the YouTube video to MP3
        mp3_file = download_youtube_video_as_mp3(youtube_url)
        return send_file(mp3_file, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def download_youtube_video_as_mp3(youtube_url, output_path='output'):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    yt = YouTube(youtube_url)
    video = yt.streams.filter(only_audio=True).first()
    
    # Download video as mp4
    downloaded_file = video.download(output_path=output_path)
    base_filename = os.path.splitext(downloaded_file)[0]
    mp3_filename = f"{base_filename}.mp3"

    # Convert to MP3 using pydub and ffmpeg
    audio = AudioSegment.from_file(downloaded_file)
    audio.export(mp3_filename, format="mp3")

    # Remove the original downloaded file (mp4)
    os.remove(downloaded_file)
    
    return mp3_filename

if __name__ == '__main__':
    app.run(debug=True)
