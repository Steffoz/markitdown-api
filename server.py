@app.route("/convert", methods=["POST"])
def convert():
    try:
        data = request.get_json()

        print("DEBUG DATA:", data)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        url = data.get("url")
        nome = data.get("nome", "file")

        if not url:
            return jsonify({"error": "Missing url"}), 400

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