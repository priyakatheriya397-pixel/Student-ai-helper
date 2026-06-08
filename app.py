import os
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# सिंगल-फाइल HTML फ्रंटएंड (ताकि फोल्डर मिसिंग होने का एरर न आए)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>मेरा असली AI चैटबॉट</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .chat-container { width: 100%; max-width: 500px; background: white; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column; height: 80vh; }
        .header { background: #007bff; color: white; padding: 15px; text-align: center; font-size: 1.2rem; font-weight: bold; }
        .chat-box { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .message { padding: 10px 15px; border-radius: 15px; max-width: 75%; word-wrap: break-word; }
        .user { background: #007bff; color: white; align-self: flex-end; }
        .bot { background: #e9ecef; color: #333; align-self: flex-start; }
        .input-area { display: flex; border-top: 1px solid #ddd; padding: 10px; background: #fff; }
        input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; outline: none; font-size: 1rem; }
        button { background: #007bff; color: white; border: none; padding: 10px 15px; margin-left: 5px; border-radius: 4px; cursor: pointer; font-size: 1rem; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">मेरा असली AI चैटबॉट</div>
        <div class="chat-box" id="chatBox">
            <div class="message bot">नमस्ते! मैं आपका असली AI असिस्टेंट हूँ। आप मुझसे कोई भी सवाल पूछ सकते हैं।</div>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="यहाँ अपना कोई भी सवाल लिखें..." onkeypress="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">भेजें</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const text = input.value.trim();
            if (!text) return;

            // यूजर का मैसेज दिखाएं
            chatBox.innerHTML += `<div class="message user">${text}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                // बैकएंड पर रिक्वेस्ट भेजें
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                
                // बोट का जवाब दिखाएं
                chatBox.innerHTML += `<div class="message bot">${data.reply}</div>`;
            } catch (error) {
                chatBox.innerHTML += `<div class="message bot" style="color:red;">त्रुटि: कनेक्ट करने में विफल।</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    # बिना किसी एक्स्ट्रा HTML फाइल के सीधे फ्रंटएंड लोड करेगा
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"reply": "कोई सवाल नहीं मिला।"}), 400

        user_message = data['message']
        
        # बिना किसी API Key के चलने वाला 100% मुफ्त AI इंजन
        api_url = f"https://pollinations.ai{user_message}"
        response = requests.get(api_url, timeout=30)

        if response.status_code == 200 and response.text:
            return jsonify({"reply": response.text.strip()})
        else:
            return jsonify({"reply": "माफ़ कीजिये, मैं अभी जवाब नहीं दे पा रहा हूँ।"})

    except Exception as e:
        return jsonify({"reply": "सर्वर अभी व्यस्त है, कृपया दोबारा प्रयास करें।"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
