import os
from flask import Flask, render_template_string

app = Flask(__name__)

# सुंदर और रिस्पॉन्सिव चैट डिज़ाइन (इसमें AI सीधे आपके फोन से कनेक्ट होगा)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .chat-container { width: 90%; max-width: 400px; background: white; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; height: 80vh; }
        .chat-header { background: #007bff; color: white; padding: 15px; text-align: center; font-size: 18px; font-weight: bold; }
        .chat-box { padding: 15px; flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .message { padding: 10px; border-radius: 5px; max-width: 75%; word-wrap: break-word; font-size: 14px; line-height: 1.4; }
        .user-msg { background: #007bff; color: white; align-self: flex-end; }
        .bot-msg { background: #e9ecef; color: #333; align-self: flex-start; }
        .input-area { display: flex; border-top: 1px solid #ddd; }
        .input-area input { flex: 1; padding: 15px; border: none; outline: none; font-size: 14px; }
        .input-area button { padding: 15px; background: #007bff; color: white; border: none; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">मेरा असली AI चैटबॉट</div>
    <div class="chat-box" id="chatBox">
        <div class="message bot-msg">नमस्ते! मैं आपका असली AI असिस्टेंट हूँ। अब आप मुझसे दुनिया का कोई भी सवाल पूछ सकते हैं, मैं हर सवाल का तुरंत जवाब दूँगा!</div>
    </div>
    <div class="input-area">
        <input type="text" id="userInput" placeholder="यहाँ अपना कोई भी सवाल लिखें...">
        <button onclick="sendMessage()">भेजें</button>
    </div>
</div>

<script>
    function sendMessage() {
        let inputField = document.getElementById("userInput");
        let message = inputField.value.trim();
        if (!message) return;

        let chatBox = document.getElementById("chatBox");
        chatBox.innerHTML += `<div class="message user-msg">${message}</div>`;
        inputField.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;

        // सीधे आपके ब्राउज़र से फ्री AI API को कॉल करना (Render का सर्वर अब बीच में रुकावट नहीं बनेगा)
        let promptWithInstruction = encodeURIComponent(message + " (कृपया इसका उत्तर हमेशा सरल हिंदी भाषा में विस्तार से दें)");
        let apiUrl = `https://pollinations.ai{promptWithInstruction}`;

        // बोट टाइपिंग इंडिकेटर दिखाएं
        let loadingId = "loading_" + Date.now();
        chatBox.innerHTML += `<div class="message bot-msg" id="${loadingId}">सोच रहा हूँ...</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;

        fetch(apiUrl)
        .then(response => {
            if(response.ok) {
                return response.text();
            } else {
                throw new Error("API Network error");
            }
        })
        .then(text => {
            // 'सोच रहा हूँ...' को असली जवाब से बदलें
            document.getElementById(loadingId).innerText = text;
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById(loadingId).innerText = "माफ़ कीजिये, रिस्पॉन्स मिलने में समस्या हुई। कृपया दोबारा प्रयास करें।";
            chatBox.scrollTop = chatBox.scrollHeight;
        });
    }
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
