from flask import Flask, render_template, request, send_file, after_this_request
from pytube import YouTube
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    try:
        yt = YouTube(video_url)
        video = yt.streams.get_highest_resolution()

        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        filename = f"{yt.title.replace(' ', '_')}.mp4"
        file_path = os.path.join(temp_dir, filename)

        # Download the video
        video.download(output_path=temp_dir, filename=filename)

        # Schedule cleanup after response
        @after_this_request
        def remove_file(response):
            try:
                os.remove(file_path)
                os.rmdir(temp_dir)
            except Exception as cleanup_error:
                print(f"Cleanup failed: {cleanup_error}")
            return response

        # Send the file to the client
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
