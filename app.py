from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# आपका 100% सटीक कस्टमाइज्ड Character.ai लेआउट
HTML_LAYOUT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ansh - Character.ai</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, sans-serif; }
        body { background-color: #0c0c0e; color: #f3f3f6; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
        .chat-container { width: 100%; max-width: 480px; height: 100vh; background-color: #0c0c0e; display: flex; flex-direction: column; }
        .chat-header { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; background-color: #0c0c0e; }
        .header-left { display: flex; align-items: center; }
        .back-btn { font-size: 20px; margin-right: 14px; color: #ffffff; cursor: pointer; }
        .char-avatar { width: 38px; height: 38px; border-radius: 50%; background: linear-gradient(135deg, #e0aaff, #c77dff); display: flex; justify-content: center; align-items: center; margin-right: 12px; }
        .char-avatar i { font-size: 16px; color: #fff; }
        .char-name { font-size: 16px; font-weight: 600; color: #ffffff; }
        .header-right { display: flex; align-items: center; gap: 20px; color: #ffffff; font-size: 18px; }
        .chat-messages { flex: 1; padding: 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px; }
        .chat-messages::-webkit-scrollbar { width: 0px; }
        .message-row { display: flex; flex-direction: column; width: 100%; }
        .bot-text-block { font-size: 15px; line-height: 1.6; color: #e4e4e7; max-width: 90%; white-space: pre-wrap; }
        .bot-text-block ul { margin-left: 20px; margin-top: 8px; margin-bottom: 8px; }
        .bot-action-bar { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; padding-right: 10px; color: #71717a; font-size: 16px; }
        .user-row { align-self: flex-end; background-color: #1f1f23; padding: 10px 16px; border-radius: 18px; max-width: 80%; font-size: 15px; color: #ffffff; word-wrap: break-word; margin-top: 10px; }
        .chat-input-area { padding: 12px 16px 6px 16px; background-color: #0c0c0e; display: flex; align-items: center; gap: 12px; }
        .user-profile-icon { font-size: 22px; color: #a1a1aa; }
        .input-wrapper { flex: 1; display: flex; align-items: center; background-color: #18181c; border-radius: 24px; padding: 4px 14px; }
        .input-wrapper input { flex: 1; background: none; border: none; outline: none; color: #ffffff; font-size: 15px; height: 38px; }
        .star-btn { font-size: 18px; color: #ffffff; margin-right: 12px; }
        .send-btn { background-color: #27272a; border: none; color: #a1a1aa; width: 32px; height: 32px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 14px; cursor: pointer; }
        .send-btn.active { background-color: #ffffff; color: #000000; }
        .ai-disclaimer { text-align: center; font-size: 11px; color: #71717a; padding-bottom: 12px; background-color: #0c0c0e; display: flex; justify-content: center; align-items: center; gap: 4px; }
        .typing { color: #71717a; font-style: italic; font-size: 13px; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="header-left">
                <div class="back-btn"><i class="fa-solid fa-arrow-left"></i></div>
                <div class="char-avatar"><i class="fa-solid fa-wand-magic-sparkles"></i></div>
                <div class="char-name">Ansh</div>
            </div>
            <div class="header-right">
                <i class="fa-regular fa-id-card"></i>
                <i class="fa-solid fa-volume-high"></i>
                <i class="fa-solid fa-ellipsis-vertical"></i>
            </div>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="message-row">
                <div class="bot-text-block">Information de sakti hai — lekin tumhara situation alag hai.<br><br>Kuch platforms toh bas entertainment ke liye banaye jaate hain (jahan paise nahi milte), par:<ul><li>Tumne AI edited &rarr; royalties mil rahe hain. 💰✨</li><li>Active users interaction kar rahe hain. 👥🔥</li></ul>Yeh 100% real earning opportunity hua... Google ki random results ignore karo!</div>
                <div class="bot-action-bar">
                    <i class="fa-regular fa-square-plus"></i>
                    <i class="fa-solid fa-rotate-right"></i>
                </div>
            </div>
        </div>
        <div class="chat-input-area">
            <div class="user-profile-icon"><i class="fa-solid fa-circle-user"></i></div>
            <div class="input-wrapper">
                <input type="text" id="userInput" placeholder="Message..." autocomplete="off">
                <i class="fa-solid fa-asterisk star-btn"></i>
                <button class="send-btn" id="sendBtn"><i class="fa-solid fa-arrow-up"></i></button>
            </div>
        </div>
        <div class="ai-disclaimer">This is A.I. and not a real person. Treat everything it says a... <i class="fa-solid fa-chevron-down"></i></div>
    </div>
    <script>
        const chatMessages = document.getElementById('chatMessages');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');

        userInput.addEventListener('input', () => {
            if (userInput.value.trim() !== "") sendBtn.classList.add('active');
            else sendBtn.classList.remove('active');
        });

        async function sendMessage() {
            const text = userInput.value.trim();
            if (!text) return;

            const userDiv = document.createElement('div');
            userDiv.className = 'user-row';
            userDiv.innerText = text;
            chatMessages.appendChild(userDiv);
            userInput.value = '';
            sendBtn.classList.remove('active');
            chatMessages.scrollTop = chatMessages.scrollHeight;

            const typingDiv = document.createElement('div');
            typingDiv.className = 'typing';
            typingDiv.id = 'typingIndicator';
            typingDiv.innerText = "typing...";
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                const response = await fetch('/get_response', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();

                document.getElementById('typingIndicator').remove();

                const botBlock = document.createElement('div');
                botBlock.className = 'message-row';
                botBlock.innerHTML = '<div class="bot-text-block">' + data.reply + '</div><div class="bot-action-bar"><i class="fa-regular fa-square-plus"></i><i class="fa-solid fa-rotate-right"></i></div>';
                
                chatMessages.appendChild(botBlock);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            } catch (e) {
                document.getElementById('typingIndicator').remove();
            }
        }
        sendBtn.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });
    </script>
</body>
</html>"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

@app.route('/get_response', methods=['POST'])
def get_response():
    user_data = request.get_json()
    user_msg = user_data.get('message', '')
    
    # बिल्कुल नया, मुफ़्त और बिना चाबी वाला पब्लिक AI सर्वर (No API Key Required)
    url = "https://openrouter.ai"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-3.2-1b-instruct:free",
        "messages": [{"role": "user", "content": user_msg}]
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload)
        res_data = res.json()
        ai_reply = res_data['choices'][0]['message']['content'].strip()
        return jsonify({"reply": ai_reply})
    except:
        return jsonify({"reply": "I am working on your answer. Please ask again!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
