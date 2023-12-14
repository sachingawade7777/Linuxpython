from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        video_url = request.form['url']
        try:
            yt = YouTube(video_url)
            video = yt.streams.get_highest_resolution()
            download_path = os.path.join(os.getcwd(), 'downloads')
            
            # Replace spaces in the title with underscores
            filename = f"{yt.title.replace(' ', '_')}.mp4"
            
            video_path = os.path.join(download_path, filename)
            video.download(download_path)
            return send_file(video_path, as_attachment=True)
        except Exception as e:
            return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
