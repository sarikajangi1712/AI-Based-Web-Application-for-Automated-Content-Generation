import openai
import os
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# HTML template as a string (Frontend UI)
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Content Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            padding: 40px;
            display: flex;
            justify-content: center;
        }
        .container {
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            width: 600px;
            text-align: center;
        }
        input, button {
            width: 80%;
            padding: 12px;
            margin: 10px 0;
            font-size: 16px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
        }
        #result {
            margin-top: 20px;
            text-align: left;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>AI Content Generator</h2>
        <input type="text" id="topic" placeholder="Enter a topic..." />
        <button onclick="generateContent()">Generate</button>
        <div id="result"></div>
    </div>
    <script>
        async function generateContent() {
            const topic = document.getElementById('topic').value;
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = "Generating... Please wait.";

            const response = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic: topic })
            });

            const data = await response.json();
            if (data.content) {
                resultDiv.innerText = data.content;
            } else {
                resultDiv.innerHTML = "<span style='color:red;'>Error: " + data.error + "</span>";
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        topic = data.get("topic", "")

        if not topic:
            return jsonify({"error": "Topic is required"}), 400

        # Generate content with OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert content writer."},
                {"role": "user", "content": f"Write a detailed, high-quality article on: {topic}"}
            ],
            temperature=0.7,
            max_tokens=600
        )

        content = response.choices[0].message.content.strip()
        return jsonify({"content": content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
