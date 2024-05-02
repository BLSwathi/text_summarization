import requests
from flask import Flask, render_template, request

app = Flask(_name_)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form["data"]
        maxL = int(request.form["maxL"])
        minL = maxL // 4

        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        API_TOKEN = "Bearer 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" 
        headers = {"Authorization": "Bearer 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"}

        response = query_api(API_URL, headers, data, minL, maxL)

        if response is not None:
            if "error" in response:
                return render_template("index.html", error=response["error"])
            else:
                return render_template("index.html", result=response[0]["summary_text"])
        else:
            return render_template("index.html", error="Failed to connect to API")
    else:
        return render_template("index.html")

def query_api(url, headers, data, min_length, max_length):
    payload = {
        "inputs": data,
        "parameters": {"min_length": min_length, "max_length": max_length}
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print("Exception:", e)
        return None

if _name_ == "main":
    app.run(debug=True)