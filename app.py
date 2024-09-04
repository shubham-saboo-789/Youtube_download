import os
import yt_dlp
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h1>Download YouTube Audio</h1>
    <form action="/download" method="POST">
        <label for="youtube_url">YouTube Video URL:</label>
        <input type="text" id="youtube_url" name="youtube_url" required>
        <button type="submit">Download Audio</button>
    </form>
    '''

@app.route('/download', methods=['POST'])
def download_audio():
    youtube_url = request.form['youtube_url']
    try:
        # Get the user's Downloads directory
        user_profile = os.environ.get('USERPROFILE')
        downloads_dir = os.path.join(user_profile, 'Downloads')

        # Path to the ffmpeg executable (can be used when ffmpeg is in the same directory as app.py)
        # ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg', 'bin')

        # Set the output template for saving the file
        output_path = os.path.join(downloads_dir, '%(title)s.%(ext)s')  # Save with video title as filename in the 'Downloads' folder

        ydl_opts = {
            'format': 'bestaudio/best',
            # 'outtmpl': output_path,  # Use the video title for filename in the specified folder
            'outtmpl': 'C:\ffmpeg\bin',  # Use the video title for filename in the specified folder
            'ffmpeg_location': ffmpeg_path,  # Relative path to ffmpeg
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Extract audio using FFmpeg
                'preferredcodec': 'mp3',     # Save the file as .mp3
                'preferredquality': '192',    # Audio quality
            }],
            'noplaylist': True,  # Ensure only the single video is downloaded, not playlists
            'quiet': True,  # Suppress output from yt-dlp
            'progress_hooks': [lambda d: None],  # Suppress progress messages
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = os.path.join(downloads_dir, f"{info['title']}.mp3")

        # Check if the file exists and send it for download
        if os.path.exists(filename):
            return send_file(filename, as_attachment=True, download_name=f"{info['title']}.mp3")

        return "Error: Audio file not found."

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
