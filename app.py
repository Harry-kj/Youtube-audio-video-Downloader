


from flask import Flask, render_template, request, jsonify, send_from_directory
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"




# Check if running on Render (or any production environment)
if os.environ.get('RENDER'):
    FFMPEG_PATH = "ffmpeg"  # Render (or Linux server) uses global ffmpeg
else:
    FFMPEG_PATH = "C:/ffmpeg/bin/ffmpeg.exe"  # Your 


os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/debug-cookies')
def debug_cookies():
    try:
        with open('cookies/cookies.txt', 'r') as f:
            lines = f.readlines()
        return f"✅ cookies.txt found. Lines: {len(lines)}"
    except FileNotFoundError:
        return "❌ cookies.txt not found."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    url = request.form['url']
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'forcejson': True,
            'simulate': True,
            'ffmpeg_location': FFMPEG_PATH,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return jsonify({
            'title': info['title'],
            'duration': info['duration_string'] if 'duration_string' in info else f"{info['duration']//60}:{info['duration']%60:02d}",
            'thumbnail': info['thumbnail']
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_type = request.form['format']
    quality = request.form['quality']
    ffmpeg_path = FFMPEG_PATH

    try:
        if format_type == 'audio':
            ydl_opts = {
                'format': 'bestaudio/best',
                'ffmpeg_location': ffmpeg_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality,
                }],
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'merge_output_format': 'mp3',
                'cookiefile': os.path.join('cookies', 'cookies.txt'),
                # 'cookiefile': 'cookies/cookies.txt',
                'http_headers': {'User-Agent': 'Mozilla/5.0'}
            }
        else:
            ydl_opts = {
                'format': f"bestvideo[height={quality}][ext=mp4]+bestaudio[ext=m4a]/mp4",
                'ffmpeg_location': ffmpeg_path,
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'merge_output_format': 'mp4',
                'cookiefile': os.path.join('cookies', 'cookies.txt'),
                # 'cookiefile': 'cookies/cookies.txt',
                'http_headers': {'User-Agent': 'Mozilla/5.0'}
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # filename = ydl.prepare_filename(info)
            # filename = os.path.splitext(filename)[0] + ('.mp3' if format_type == 'audio' else '.mp4')
            base_title = info.get('title', 'downloaded')
            if format_type == 'audio':
                filename = f"{base_title} - audio {quality}kbps.mp3"
            else:
                filename = f"{base_title} - video {quality}p.mp4"
            filename_path = os.path.join(DOWNLOAD_FOLDER, filename)
            os.rename(ydl.prepare_filename(info), filename_path)


        return send_from_directory(DOWNLOAD_FOLDER, os.path.basename(filename), as_attachment=True)

    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

