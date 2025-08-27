import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from fastapi import HTTPException
from prompt_template import generate_prompt
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key! Please set it in the environment variable")

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    try:
        patient_data = request.get_json()

        if not patient_data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        prompt = generate_prompt(patient_data)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly, patient-focused medical assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        patient_message = response.choices[0].message.content
        
        return jsonify({"message": patient_message}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)