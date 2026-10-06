from flask import Flask, render_template, request, jsonify, send_file
import os
import yt_dlp
import tempfile

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    url = (request.form.get("url") or "").strip()
    output_format = (request.form.get("format") or "video").lower()

    if not url:
        return jsonify({
            "success": False,
            "message": "Link tidak boleh kosong!"
        }), 400

    if output_format not in {"video", "mp3"}:
        return jsonify({
            "success": False,
            "message": "Format unduhan tidak valid."
        }), 400

    try:
        temp_folder = tempfile.mkdtemp(prefix="firuztok-")

        ydl_opts = {
            "outtmpl": os.path.join(temp_folder, "%(title)s.%(ext)s"),
            "format": "bestaudio/best" if output_format == "mp3" else "best",
            "noplaylist": True
        }

        if output_format == "mp3":
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            if output_format == "mp3":
                filename = next(
                    (
                        entry.path
                        for entry in os.scandir(temp_folder)
                        if entry.is_file() and entry.name.lower().endswith(".mp3")
                    ),
                    None
                )
                if filename is None:
                    raise FileNotFoundError("File MP3 hasil konversi tidak ditemukan.")
            else:
                filename = ydl.prepare_filename(info)

        return send_file(
            filename,
            as_attachment=True,
            download_name=os.path.basename(filename),
            mimetype="audio/mpeg" if output_format == "mp3" else None
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)