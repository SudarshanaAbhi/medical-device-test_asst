from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_device_classification(device_name):
    try:
        prompt = f"""For the medical device "{device_name}", please provide:
        1. The likely FDA device classification (Class I, II, or III) with a brief explanation
        2. The types of metrics that should be collected and the type of equipment that should be used to collect them
        3. The general controls that apply
        4. Any special controls if applicable
        5. Required testing methods according to FDA regulations
        6. Any specific standards (ISO, ASTM, etc.) that should be considered
        
        Format the response in clear sections with headers. Base your response on FDA regulations and guidelines."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in medical device regulations and FDA requirements. Provide accurate classification and testing information based on FDA guidelines. If there's any uncertainty, err on the side of higher classification and more stringent testing requirements."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    device_name = request.form.get('device_name', '')
    
    if not device_name:
        return jsonify({'error': 'Please provide a medical device name'}), 400
    
    classification_info = generate_device_classification(device_name)
    return jsonify({'classification_info': classification_info})

if __name__ == "__main__":
    app.run(debug=True) 