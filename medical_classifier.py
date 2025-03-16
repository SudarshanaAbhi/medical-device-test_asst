from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import numpy as np

app = Flask(__name__)

# Load BioClinicalBERT model and tokenizer
MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()

def get_embedding(text):
    """Get embeddings for input text using BioClinicalBERT"""
    # Tokenize and prepare input
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Get model output
    with torch.no_grad():
        outputs = model(**inputs)
        # Use [CLS] token embedding as text representation
        embeddings = outputs.last_hidden_state[:, 0, :]
        # Normalize embeddings
        embeddings = F.normalize(embeddings, p=2, dim=1)
    
    return embeddings

def classify_device(text):
    """Classify medical device based on text description"""
    # Get text embedding
    embedding = get_embedding(text)
    
    # Simple rule-based classification based on embedding features
    # This is a placeholder - you would typically use a trained classifier here
    embedding_np = embedding.cpu().numpy()[0]
    
    # Example classification logic (simplified)
    risk_score = np.mean(np.abs(embedding_np))
    
    if risk_score < 0.3:
        classification = "Class I"
        explanation = "Low risk device with simple, well-established functionality."
    elif risk_score < 0.6:
        classification = "Class II"
        explanation = "Moderate risk device requiring special controls."
    else:
        classification = "Class III"
        explanation = "High risk device requiring premarket approval."
    
    # Suggest relevant testing methods based on classification
    if classification == "Class I":
        testing = [
            "Basic safety testing",
            "Electrical safety testing (if applicable)",
            "Biocompatibility testing (if patient contact)",
            "Sterilization validation (if sterile)"
        ]
    elif classification == "Class II":
        testing = [
            "Comprehensive safety testing",
            "Performance testing",
            "Biocompatibility testing",
            "Sterilization validation",
            "Software validation (if applicable)",
            "Clinical data review"
        ]
    else:  # Class III
        testing = [
            "Extensive safety and performance testing",
            "Clinical trials",
            "Long-term biocompatibility studies",
            "Sterilization validation",
            "Software validation",
            "Risk analysis",
            "Post-market surveillance plan"
        ]
    
    return {
        "classification": classification,
        "explanation": explanation,
        "testing_methods": testing,
        "risk_score": float(risk_score)
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    device_description = request.form.get('device_description', '')
    if not device_description:
        return jsonify({'error': 'Please provide a device description'}), 400
    
    result = classify_device(device_description)
    return jsonify(result)

if __name__ == '__main__':
    print(f"Using device: {device}")
    app.run(debug=True) 