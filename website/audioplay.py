from flask import Flask, Blueprint, render_template, request, send_file, url_for
import os

app = Flask(__name__)

# Blueprint dari kode kedua
audioplay = Blueprint('audioplay', __name__)

# Halaman untuk memilih durasi meditasi
@audioplay.route('/meditation')
def meditation():
    return render_template('meditation_duration.html')

# Endpoint untuk menampilkan halaman pemutar audio berdasarkan durasi yang dipilih
@audioplay.route('/audio-play')
def audio_play():
    # Ambil parameter durasi dari URL
    duration = request.args.get('duration', 'short')

    # Tentukan file audio berdasarkan durasi yang dipilih
    if duration == 'short':
        audio_file_path = url_for('static', filename='audio/meditation_short.mp3')
        meditation_time = 5  # Durasi 5 menit
    elif duration == 'medium':
        audio_file_path = url_for('static', filename='audio/meditation_medium.mp3')
        meditation_time = 10  # Durasi 10 menit
    else:
        audio_file_path = url_for('static', filename='audio/meditation_long.mp3')
        meditation_time = 15  # Durasi 20 menit

    remaining_time = request.args.get('remaining_time', meditation_time * 60)
    remaining_time = int(remaining_time)

    audio_file_url = url_for('audioplay.stream_audio', filename=audio_file_path)
    # Jika waktu habis, tampilkan pesan selesai
    if remaining_time <= 0:
        return render_template('complete.html')

    # Render halaman audio_player dengan durasi dan audio file yang tepat
    return render_template('audio_player.html', audio_file=audio_file_path, remaining_time=remaining_time, duration=meditation_time)

# Jalur khusus untuk streaming audio
@audioplay.route('/stream_audio/<filename>')
def stream_audio(filename):
    audio_file_path = os.path.join('static', 'audio', filename)

    # Mengirimkan file sebagai respons streaming
    return send_file(audio_file_path, mimetype='audio/mpeg')

# Register blueprint
app.register_blueprint(audioplay, url_prefix="/")

if __name__ == '__main__':
    app.run(debug=True)
