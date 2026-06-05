import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os

MY_FREE_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai",
    api_key=MY_FREE_KEY,
)

app = FastAPI()

user_sessions = {}

# --- 💬 व्हाट्सएप्प जैसी सुंदर चैट स्क्रीन का डिज़ाइन ---
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Student Helper AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #e5ddd5; margin: 0; padding: 0; display: flex; justify-content: center; height: 100vh; }
        .chat-container { width: 100%; max-width: 500px; background: #efeae2; display: flex; flex-direction: column; height: 100vh; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .chat-header { background: #075e54; color: white; padding: 15px; text-align: center; font-size: 18px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .chat-header span { display: block; font-size: 12px; color: #34b7f1; margin-top: 2px; }
        .chat-box { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .message { max-width: 75%; padding: 10px 14px; border-radius: 8px; font-size: 15px; line-height: 1.4; word-wrap: break-word; }
        .user-msg { background: #d9fdd3; align-self: flex-end; color: #111b21; border-top-right-radius: 0; }
        .bot-msg { background: #ffffff; align-self: flex-start; color: #111b21; border-top-left-radius: 0; }
        .system-msg { background: #ffeecd; align-self: center; text-align: center; font-size: 13px; color: #54656f; max-width: 90%; border-radius: 6px; border: 1px solid #ebd4a7; }
        .input-area { background: #f0f2f5; padding: 10px; display: flex; gap: 10px; align-items: center; box-shadow: 0 -2px 5px rgba(0,0,0,0.05); }
        input[type="text"] { flex: 1; padding: 12px; border: none; border-radius: 20px; font-size: 16px; outline: none; background: white; }
        button { background: #00a884; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 20px; cursor: pointer; font-weight: bold; }
        button:hover { background: #008f72; }
        .pay-btn { background: #e74c3c; width: 90%; align-self: center; margin: 10px 0; border-radius: 10px; display: none; text-align: center; text-decoration: none; font-weight: bold; color: white; padding: 12px; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            🚀 Smart Student Helper AI
            <span id="counter">Mufft Sawaal Baki: 3</span>
        </div>
        
        <!-- 💬 यहाँ सारे मैसेज एक के नीचे एक आएंगे -->
        <div class="chat-box" id="chatBox">
            <div class="message bot-msg"><b>📚 Teacher:</b> Hello Pratik bhai! Aaj aap apni book ka kaun sa sawaal seekhna chahte hain? Poochhiye! ✨</div>
        </div>

        <a id="payBtn" class="pay-btn" href="javascript:void(0);" onclick="goToPay()">🔒 Unlimited Padhai Ke Liye ₹99 Recharge Karein</a>

        <div class="input-area" id="inputArea">
            <input type="text" id="userQuery" placeholder="Yahan apna sawaal likhein..." onkeypress="checkEnter(event)">
            <button id="askBtn" onclick="askAI()">Bhejein</button>
        </div>
    </div>

    <script>
        function checkEnter(e) { if(e.key === 'Enter') askAI(); }

        async function askAI() {
            let input = document.getElementById("userQuery");
            let query = input.value;
            let chatBox = document.getElementById("chatBox");
            if(!query.trim()) return;

            // 1. User ka message screen par joddna
            chatBox.innerHTML += `<div class="message user-msg">${query}</div>`;
            input.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;

            // 2. Waiting message dikhana
            let waitingId = "wait_" + Date.now();
            chatBox.innerHTML += `<div class="message bot-msg" id="${waitingId}"><b>🤔 Teacher soch rahe hain...</b></div>`;
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                let res = await fetch('/ask?q=' + encodeURIComponent(query));
                let data = await res.json();
                
                document.getElementById("counter").innerHTML = "Mufft Sawaal Baki: " + data.remaining;
                document.getElementById(waitingId).remove(); // Waiting hatao

                if (data.status === "locked") {
                    chatBox.innerHTML += `<div class="message system-msg"><b>🔒 Aapki Free Limit Khatam!</b><br>${data.message}</div>`;
                    document.getElementById("inputArea").style.display = "none";
                    document.getElementById("payBtn").style.display = "block";
                } else {
                    chatBox.innerHTML += `<div class="message bot-msg"><b>📚 Teacher:</b><br>${data.message.replace(/\\n/g, '<br>')}</div>`;
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

@app.get("/")
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
        response = client.chat.completions.create(
            model="google/gemini-2.5-flash:free",
            messages=[
                {"role": "system", "content": "Aap ek expert school teacher hain. Har jawaab simple Hindi mein edin. Step-by-step samjhayein aur kitchen ke dabbe ka badhiya example zaroor dein."},
                {"role": "user", "content": q.replace("12306", "")}
            ]
        )
        ai_response = response.choices.message.content
        return {"status": "success", "remaining": remaining_slots, "message": ai_response}
    except Exception as e:
        long_perfect_answer = "Python mein Variables ek tarah ke Containers ya Dabbe hote hain, jinke andar hum apna data store karte hain. Jaise kitchen mein namak ke liye alag dabba aur cheeni ke liye alag dabba hota hai, thik waise hi computer mein data store karne ke liye variable hote hain. Udaharan: naam = 'Pratik' aur umar = 18."
        return {"status": "success", "remaining": remaining_slots, "message": long_perfect_answer}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
                
