from flask import Flask, request, jsonify
from markitdown import MarkItDown
import requests
import os

app = Flask(__name__)
md = MarkItDown()

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()

    url = data["url"]
    nome = data.get("nome", "file")

    # download file
    r = requests.get(url, timeout=60, allow_redirects=True)

    path = f"./{nome}.pdf"

    with open(path, "wb") as f:
        f.write(r.content)

    # 🔥 TRY SOLO QUI
    try:
        result = md.convert(path)

        return jsonify({
            "text": result.text_content
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(port=5005, debug=True)