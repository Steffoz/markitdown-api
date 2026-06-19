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
    nome = data.get("nome", "file.pdf")

    # scarica file
    r = requests.get(url)
    path = f"./{nome}.pdf"

    with open(path, "wb") as f:
        f.write(r.content)

    # conversione
    result = md.convert(path)

    # cleanup (IMPORTANTE)
    os.remove(path)

    return jsonify({
        "text": result.text_content
    })

if __name__ == "__main__":
    app.run(port=5005, debug=True)