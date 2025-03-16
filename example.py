from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1"  # Explicitly set the base URL
)

def generate_device_classification(device_name):
    try:
        prompt = f"""For the medical device "{device_name}", please provide:
        1. The likely FDA device classification (Class I, II, or III) with a brief explanation
        2. The general controls that apply
        3. Any special controls if applicable
        4. Required testing methods according to FDA regulations
        5. Any specific standards (ISO, ASTM, etc.) that should be considered
        
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
    # For local development only
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 