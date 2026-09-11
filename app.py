from flask import Flask, render_template, request, jsonify
import os
import yt_dlp

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")

    if not url:
        return jsonify({
            "success": False,
            "message": "Link tidak boleh kosong!"
        })

    try:
        ydl_opts = {
            "outtmpl": os.path.join(
                DOWNLOAD_FOLDER,
                "%(title)s.%(ext)s"
            ),
            "format": "best",
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return jsonify({
            "success": True,
            "message": "Video berhasil diunduh!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)