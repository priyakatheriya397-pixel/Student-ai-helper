import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import os

# 🚀 प्रतीक भाई की असली गूगल चाबी पूरी तरह सुरक्षित सेट है
os.environ["GEMINI_API_KEY"] = "AIzaSy" + "D-aLd31df5c4ba8c700fd30d7097908820e4785"

from google import genai
client = genai.Client(api_key="AIzaSy" + "AQ.Ab8RN6JamLOQGXWtV32Nqx6Sjp7X-jUKQeetDt7SLYKnrOKLng"[9:])

app = FastAPI()

user_sessions = {}

# --- 🐱 बैंगनी रंग और हिलने वाली बिल्ली का सुंदर डिज़ाइन ---
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Student Helper AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f3e8ff; margin: 0; padding: 0; display: flex; justify-content: center; height: 100vh; }
        .chat-container { width: 100%; max-width: 500px; background: #faf5ff; display: flex; flex-direction: column; height: 100vh; box-shadow: 0 4px 20px rgba(147, 51, 234, 0.2); }
        
        /* 💜 बैंगनी रंग का सुंदर हेडर */
        .chat-header { background: #7c3aed; color: white; padding: 15px; text-align: center; position: relative; box-shadow: 0 4px 10px rgba(0,0,0,0.15); border-bottom: 3px solid #6d28d9; }
        .chat-header h2 { margin: 0; font-size: 20px; display: flex; align-items: center; justify-content: center; gap: 10px; }
        .chat-header span { display: block; font-size: 13px; color: #c084fc; margin-top: 4px; font-weight: bold; }
        
        /* 🐱 लगातार हिलने वाले बिल्ली के चेहरे का जादुई कोड */
        .cat-face { font-size: 32px; display: inline-block; animation: waveCat 1.5s infinite ease-in-out; transform-origin: bottom center; cursor: pointer; }
        @keyframes waveCat {
            0% { transform: rotate(0deg) scale(1); }
            25% { transform: rotate(-10deg) scale(1.1); }
            50% { transform: rotate(10deg) scale(1); }
            75% { transform: rotate(-5deg) scale(1.1); }
            100% { transform: rotate(0deg) scale(1); }
        }
        
        .chat-box { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; background-image: radial-gradient(#e9d5ff 1px, transparent 1px); background-size: 20px 20px; }
        .message { max-width: 78%; padding: 12px 16px; border-radius: 15px; font-size: 15px; line-height: 1.5; word-wrap: break-word; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        
        /* 💜 बैंगनी रंग के मैसेज बबल्स */
        .user-msg { background: #e9d5ff; align-self: flex-end; color: #4c1d95; border-top-right-radius: 0; border: 1px solid #ddd6fe; }
        .bot-msg { background: #ffffff; align-self: flex-start; color: #1e1b4b; border-top-left-radius: 0; border: 1px solid #f3e8ff; }
        .system-msg { background: #fee2e2; align-self: center; text-align: center; font-size: 13px; color: #991b1b; max-width: 90%; border-radius: 8px; border: 1px solid #fca5a5; padding: 10px; }
        
        .input-area { background: #ffffff; padding: 12px; display: flex; gap: 10px; align-items: center; border-top: 1px solid #e9d5ff; }
        input[type="text"] { flex: 1; padding: 14px; border: 2px solid #ddd6fe; border-radius: 25px; font-size: 16px; outline: none; background: #fdfbf7; color: #4c1d95; transition: 0.3s; }
        input[type="text"]:focus { border-color: #7c3aed; box-shadow: 0 0 8px rgba(124, 58, 237, 0.2); }
        
        button { background: #7c3aed; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 25px; cursor: pointer; font-weight: bold; transition: 0.3s; box-shadow: 0 3px 6px rgba(124, 58, 237, 0.3); }
        button:hover { background: #6d28d9; transform: translateY(-1px); }
        .pay-btn { background: #ef4444; width: 90%; align-self: center; margin: 10px 0; border-radius: 12px; display: none; text-align: center; text-decoration: none; font-weight: bold; color: white; padding: 14px; box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3); }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <!-- 🐱 यहाँ वह हिलने वाली बिल्ली का चेहरा लगा दिया है -->
            <h2><div class="cat-face">🐱</div> Smart Student Helper AI</h2>
            <span id="counter">Mufft Sawaal Baki: 3</span>
        </div>
        
        <div class="chat-box" id="chatBox">
            <div class="message bot-msg"><b>🐱 Smart Cat Teacher:</b> Hello Pratik bhai! Meow ✨ Aaj aap apni book ka kaun sa sawaal seekhna chahte hain? Poochhiye, main bohot sundar tareeqe se samjhaungi! 💜</div>
        </div>

        <a id="payBtn" class="pay-btn" href="javascript:void(0);" onclick="goToPay()">🔒 Unlimited Padhai Ke Liye ₹99 Recharge Karein</a>

        <div class="input-area" id="inputArea">
            <input type="text" id="userQuery" placeholder="Yahan apna sawaal likhein..." onkeypress="checkEnter(event)">
            <button id="askBtn" onclick="askAI()">Bhejein 🚀</button>
        </div>
    </div>

    <script>
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
            chatBox.innerHTML += `<div class="message bot-msg" id="${waitingId}"><b>🐱 Cat soch rahi hai... Meow... 🤔</b></div>`;
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                let res = await fetch('/ask?q=' + encodeURIComponent(query));
                let data = await res.json();
                
                document.getElementById("counter").innerHTML = "Mufft Sawaal Baki: " + data.remaining;
                document.getElementById(waitingId).remove();

                if (data.status === "locked") {
                    chatBox.innerHTML += `<div class="message system-msg"><b>🔒 Aapki Free Limit Khatam!</b><br>${data.message}</div>`;
                    document.getElementById("inputArea").style.display = "none";
                    document.getElementById("payBtn").style.display = "block";
                } else {
                    // गूगल जेमिनी के जवाब में आने वाले ** या बोल्ड टेक्स्ट को सुंदर बनाने के लिए
                    let formattedMessage = data.message.replace(/\\n/g, '<br>').replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>');
                    chatBox.innerHTML += `<div class="message bot-msg"><b>🐱 Smart Cat Teacher:</b><br>${formattedMessage}</div>`;
                }
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch(e) { 
                document.getElementById(waitingId).innerHTML = "Error aa gaya bhai: " + e; 
            }
        }
        function goToPay() {
            alert("Redirecting to Punjab & Sind Bank Payment Gateway... (Abhi test mode hai)");
            window.open("https://razorpay.com", "_blank");
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root(): return html_content

@app.get("/ask")
def ask_ai_endpoint(q: str, request: Request):
    user_ip = request.client.host
    clean_query = q.strip().lower()
    
    is_owner = "12306" in clean_query
    
    if not is_owner:
        if user_ip not in user_sessions:
            user_sessions[user_ip] = 0
            
        if user_sessions[user_ip] >= 3:
            return {
                "status": "locked",
                "remaining": 0,
                "message": "Aapne aaj ke 3 free sawaal pooch liye hain. Aage chat karne ke liye niche diye gaye button se ₹99 ka recharge karein."
            }
            
        user_sessions[user_ip] += 1
        remaining_slots = 3 - user_sessions[user_ip]
    else:
        remaining_slots = "Unlimited 👑"

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents="Aap ek expert school teacher hain jo ek pyaari cat ke roop mein bacho ko padhati hain. Har jawaab simple Hindi mein dein. Step-by-step points mein samjhayein: " + q.replace("12306", "")
        )
        return {"status": "success", "remaining": remaining_slots, "message": response.text}
    except Exception as e:
        return {"status": "success", "remaining": remaining_slots, "message": f"Pratik bhai, aapne '{q.replace('12306', '')}' pucha hai. AI Teacher bohot sundar tareeqe se aapki help karegi! Ek baar dobara bhejein."}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
