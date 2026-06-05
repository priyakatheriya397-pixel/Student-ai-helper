import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from google import genai

# 🛡️ Render के Dashboard से ही चाबी उठाएगा, कोड में कुछ भी लीक नहीं होगा
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

app = FastAPI()
user_sessions = {}

html_content = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Student Toolkit AI</title>
    <style>
        /* 🎨 गहरा पर्पल मुख्य बैकग्राउंड */
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%);
            margin: 0;
            padding: 20px;
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            box-sizing: border-box;
        }

        /* 👑 मुख्य डैशबोर्ड कंटेनर */
        .dashboard {
            width: 100%;
            max-width: 800px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            text-align: center;
            margin-top: 40px;
        }

        .dashboard h1 { margin: 0 0 10px 0; font-size: 32px; color: #f3e8ff; }
        .dashboard p { font-size: 16px; color: #ddd6fe; margin-bottom: 30px; }

        /* 🎛️ टूल्स ग्रिड और बड़े बटन्स */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .tool-card {
            background: rgba(255, 255, 255, 0.15);
            border: 2px solid #a78bfa;
            padding: 25px 20px;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            color: white;
        }

        .tool-card:hover {
            background: #7c3aed;
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(124, 58, 237, 0.4);
        }

        .tool-icon { font-size: 40px; margin-bottom: 15px; }
        .tool-card h3 { margin: 0 0 8px 0; font-size: 18px; }
        .tool-card p { margin: 0; font-size: 13px; color: #e9d5ff; }

        /* 💬 छोटा फ्लोटिंग चैट विजेट (उंगली बराबर गोल बटन) */
        .chat-widget-btn {
            position: fixed;
            bottom: 25px;
            right: 25px;
            width: 60px;
            height: 60px;
            background: #7c3aed;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            border: 2px solid #ddd6fe;
            z-index: 1000;
            transition: transform 0.2s;
        }
        .chat-widget-btn:hover { transform: scale(1.1); }

        /* 📱 छोटा चैट बॉक्स जो बटन दबाने पर खुलेगा */
        .chat-window {
            position: fixed;
            bottom: 95px;
            right: 25px;
            width: 350px;
            height: 450px;
            background: #faf5ff;
            border-radius: 15px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.3);
            display: none; /* शुरुआत में छुपा रहेगा */
            flex-direction: column;
            overflow: hidden;
            border: 2px solid #7c3aed;
            z-index: 1000;
            color: #111;
        }

        .chat-header { background: #7c3aed; color: white; padding: 12px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; }
        .close-btn { cursor: pointer; font-size: 20px; }
        .chat-box { flex: 1; padding: 12px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; background: #fdfbf7; font-size: 14px; }
        
        .message { max-width: 80%; padding: 10px 14px; border-radius: 12px; line-height: 1.4; }
        .user-msg { background: #e9d5ff; align-self: flex-end; color: #4c1d95; border-top-right-radius: 0; }
        .bot-msg { background: #ffffff; align-self: flex-start; border: 1px solid #e9d5ff; border-top-left-radius: 0; }
        
        .input-area { padding: 10px; display: flex; gap: 8px; background: white; border-top: 1px solid #e9d5ff; }
        .input-area input { flex: 1; padding: 10px; border: 1px solid #ddd6fe; border-radius: 20px; outline: none; }
        .input-area button { background: #7c3aed; color: white; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>

    <!-- 🌐 मुख्य डैशबोर्ड -->
    <div class="dashboard">
        <h1>🐱 Smart Student Toolkit</h1>
        <p>प्रतीक भाई द्वारा निर्मित शक्तिशाली एआई सिस्टम। आप नीचे दिए गए टूल्स का उपयोग करके कुछ भी बना सकते हैं!</p>
        
        <div class="tools-grid">
            <!-- टूल 1: वेब पेज बनाना -->
            <div class="tool-card" onclick="openToolChat('web_create')">
                <div class="tool-icon">🌐</div>
                <h3>Create Web Page</h3>
                <p>नया HTML/CSS वेबसाइट कोड तुरंत तैयार करें</p>
            </div>
            
            <!-- टूल 2: वेब पेज एडिट करना -->
            <div class="tool-card" onclick="openToolChat('web_edit')">
                <div class="tool-icon">✍️</div>
                <h3>Edit Web Page</h3>
                <p>अपने पुराने कोड को सुधारें या नया फीचर जोड़ें</p>
            </div>
            
            <!-- टूल 3: वीडियो एआई टूल्स -->
            <div class="tool-card" onclick="openToolChat('video_ai')">
                <div class="tool-icon">🎥</div>
                <h3>Video Tools AI</h3>
                <p>वीडियो स्क्रिप्ट, आइडिया और रील्स के प्रॉम्प्ट्स बनाएं</p>
            </div>
        </div>
    </div>

    <!-- 💬 छोटा फ्लोटिंग चैट बटन (उंगली बराबर) -->
    <div class="chat-widget-btn" onclick="toggleChat()">🐱</div>

    <!-- 📱 छोटा चैट विंडो विजेट -->
    <div class="chat-window" id="chatWindow">
        <div class="chat-header">
            <span id="chatTitle">🐱 Cat Teacher Help</span>
            <span class="close-btn" onclick="toggleChat()">✖</span>
        </div>
        <div class="chat-box" id="chatBox">
            <div class="message bot-msg"><b>🐱 Cat Teacher:</b> Meow! प्रतीक भाई, मैं आपकी क्या मदद करूँ? आप ऊपर दिए गए टूल्स भी चुन सकते हैं! ✨</div>
        </div>
        <div class="input-area">
            <input type="text" id="userQuery" placeholder="Yahan apna sawaal likhein..." onkeypress="checkEnter(event)">
            <button onclick="askAI()">Bhejein</button>
        </div>
    </div>

    <script>
        let currentMode = "general";

        function toggleChat() {
            let win = document.getElementById("chatWindow");
            win.style.display = (win.style.display === "flex") ? "none" : "flex";
        }

        function openToolChat(mode) {
            currentMode = mode;
            let title = document.getElementById("chatTitle");
            let chatBox = document.getElementById("chatBox");
            
            document.getElementById("chatWindow").style.display = "flex";
            
            if(mode === 'web_create') {
                title.innerText = "🌐 Web Creator AI";
                chatBox.innerHTML += `<div class="message bot-msg"><b>🤖 System:</b> आप नया वेब पेज बनाना चाहते हैं। मुझे बताएं कि आपको किस तरह की वेबसाइट का HTML कोड चाहिए?</div>`;
            } else if(mode === 'web_edit') {
                title.innerText = "✍️ Web Editor AI";
                chatBox.innerHTML += `<div class="message bot-msg"><b>🤖 System:</b> अपना पुराना कोड यहाँ पेस्ट करें और बताएं कि उसमें क्या बदलाव या एडिट करना है?</div>`;
            } else if(mode === 'video_ai') {
                title.innerText = "🎥 Video AI Assistant";
                chatBox.innerHTML += `<div class="message bot-msg"><b>🤖 System:</b> वीडियो टूल एक्टिवेटेड। आप किस टॉपिक पर वीडियो स्क्रिप्ट या रील्स के प्रॉम्प्ट्स बनाना चाहते हैं?</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function checkEnter(e) { if(e.key === 'Enter') askAI(); }

        async function askAI() {
            let input = document.getElementById("userQuery");
            let query = input.value;
            let chatBox = document.getElementById("chatBox");
            if(!query.trim()) return;

            chatBox.innerHTML += `<div class="message user-msg">${query}</div>`;
            input.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;

            let waitingId = "wait_" + Date.now();
            chatBox.innerHTML += `<div class="message bot-msg" id="${waitingId}"><b>🐱 Cat सोच रही है... 🤔</b></div>`;
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                // मोड को भी सर्वर पर पैरामीटर के रूप में भेज रहे हैं
                let res = await fetch(`/ask?q=${encodeURIComponent(query)}&mode=${currentMode}`);
                let data = await res.json();
                
                document.getElementById(waitingId).remove();
                let formattedMessage = data.message.replace(/\\n/g, '<br>').replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>');
                chatBox.innerHTML += `<div class="message bot-msg"><b>🐱 AI Response:</b><br>${formattedMessage}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch(e) { 
                document.getElementById(waitingId).innerHTML = "Error: " + e; 
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root(): 
    return html_content

@app.get("/ask")
