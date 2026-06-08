import os
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS एरर को रोकने के लिए

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"reply": "कोई सवाल नहीं मिला।"}), 400

        user_message = data['message']

        # बिना API Key के काम करने वाला मुफ्त पब्लिक API (DuckDuckGo AI Proxy)
        # यह Llama 3 मॉडल का उपयोग करता है जो बिल्कुल फ्री है
        url = "https://fakeopen.com" # या कोई भी ओपन पब्लिक एंडपॉइंट
        
        # वैकल्पिक सुरक्षित तरीका: Hugging Face के पब्लिक मॉडल का उपयोग बिना टोकन के
        # हम यहाँ एक ओपन-सोर्स API एंडपॉइंट का उपयोग कर रहे हैं
        api_url = "https://pollinations.ai" # यह बिना किसी चाबी के चलने वाला मुफ्त AI है
        
        # Pollinations AI पर सीधे रिक्वेस्ट भेज रहे हैं जो बिना की (Key) के तुरंत जवाब देता है
        response = requests.get(f"{api_url}{user_message}", timeout=30)

        if response.status_code == 200 and response.text:
            return jsonify({"reply": response.text.strip()})
        else:
            return jsonify({"reply": "माफ़ कीजिये, मैं अभी जवाब नहीं दे पा रहा हूँ। कृपया दोबारा कोशिश करें।"})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"reply": "सर्वर अभी व्यस्त है, कृपया एक बार फिर प्रयास करें।"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
