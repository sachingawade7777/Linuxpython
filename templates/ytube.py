from flask import Flask, render_template, request
from pytube import YouTube

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
            video.download('./downloads')  # Download the video to the 'downloads' folder
            return f"Video downloaded successfully: {yt.title}"
        except Exception as e:
            return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
