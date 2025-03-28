from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Facebook Graph API URL
GRAPH_URL = "https://graph.facebook.com/me?fields=id,name&access_token="

# Function to check a single token
def check_token(token):
    try:
        response = requests.get(GRAPH_URL + token)
        data = response.json()
        if "id" in data and "name" in data:
            return {"status": "valid", "name": data['name'], "id": data['id'], "token": token}
        else:
            return {"status": "invalid", "token": token}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Home Route
@app.route('/')
def index():
    return render_template("index.html")

# Single Token Check
@app.route('/check', methods=['POST'])
def check():
    token = request.form.get("token")
    result = check_token(token)
    return jsonify(result)

# Bulk Token Check
@app.route('/bulk_check', methods=['POST'])
def bulk_check():
    file = request.files['file']
    tokens = file.read().decode('utf-8').splitlines()
    
    valid_tokens = []
    invalid_tokens = []

    for token in tokens:
        result = check_token(token)
        if result["status"] == "valid":
            valid_tokens.append(result)
        else:
            invalid_tokens.append(result["token"])

    # Auto Remove Expired Tokens
    with open("valid_tokens.txt", "w") as f:
        for valid in valid_tokens:
            f.write(valid["token"] + "\n")

    return jsonify({"valid": valid_tokens, "invalid": invalid_tokens})

# Run the App
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5200)))
