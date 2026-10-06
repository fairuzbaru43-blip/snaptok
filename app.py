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

    if not url:
        return jsonify({
            "success": False,
            "message": "Link tidak boleh kosong!"
        }), 400

    try:
        temp_folder = tempfile.mkdtemp(prefix="firuztok-")

        ydl_opts = {
            "outtmpl": os.path.join(temp_folder, "%(title)s.%(ext)s"),
            "format": "best",
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return send_file(
            filename,
            as_attachment=True,
            download_name=os.path.basename(filename)
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)
