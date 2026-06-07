import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# फ्री AI मॉडल का API URL
HF_API_URL = "https://huggingface.co"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def bot_response():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip() if data else ""
        
        if not user_message:
            user_message = request.form.get('msg', '').strip()

        if not user_message:
            return jsonify({"response": "कृपया कुछ टाइप करें..."})

        # फ्री AI मॉडल को मैसेज भेजना
        payload = {"inputs": user_message}
        response = requests.post(HF_API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                ai_response = result[0].get('generated_text', 'मैं समझ नहीं पाया।')
            elif isinstance(result, dict):
                ai_response = result.get('generated_text', 'मैं समझ नहीं पाया।')
            else:
                ai_response = "माफ़ कीजिये, अभी जवाब नहीं मिल पाया।"
        else:
            ai_response = "सर्वर अभी व्यस्त है, कृपया कुछ देर बाद प्रयास करें।"

        return jsonify({"response": ai_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "सर्वर में कुछ समस्या आ रही है।"})

if __name__ == '__main__':
    # Render के लिए पोर्ट को सेट करना ज़रूरी है
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
