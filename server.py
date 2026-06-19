from flask import Flask, request, jsonify
from markitdown import MarkItDown
import requests
import os

app = Flask(__name__)
md = MarkItDown()

@app.route("/convert", methods=["POST"])
def convert():
    try:
        data = request.get_json()

        print("DEBUG DATA:", data)

        url = data.get("url")
        nome = data.get("nome", "file")

        if not url:
            return jsonify({"error": "missing url"}), 400

        r = requests.get(url)
        path = f"./{nome}.pdf"

        with open(path, "wb") as f:
            f.write(r.content)

        result = md.convert(path)

        os.remove(path)

        return jsonify({
            "text": result.text_content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5005, debug=True)