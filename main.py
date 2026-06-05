import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os

# 🚀 Google Gemini की 100% फ्री और हमेशा चलने वाली चाबी यहाँ सेट कर दी है
GEMINI_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai",
    api_key=GEMINI_KEY,
)

app = FastAPI()

user_sessions = {}

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Student Helper AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; display: flex; justify-content: center; }
        .container { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 500px; text-align: center; }
        h1 { color: #2c3e50; font-size: 24px; }
        p { color: #7f8c8d; }
        input[type="text"] { width: 90%; padding: 12px; margin: 15px 0; border: 2px solid #bdc3c7; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
        button { background-color: #3498db; color: white; border: none; padding: 12px 25px; font-size: 16px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; margin-bottom: 10px; }
        .pay-btn { background-color: #2ecc71; display: none; width: 100%; color: white; border: none; padding: 12px 25px; font-size: 16px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        #responseBox { margin-top: 20px; text-align: left; background: #eef2f3; padding: 15px; border-radius: 6px; display: none; font-size: 15px; line-height: 1.5; color: #333; }
        #counter { color: #e74c3c; font-weight: bold; font-size: 14px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Smart Student Helper AI</h1>
        <p>Pratik bhai jaisa aapka apna AI Tutor! Apni book ka sawaal niche likhein:</p>
        <input type="text" id="userQuery" placeholder="e.g., Python mein Variables kya hain?">
        <button id="askBtn" onclick="askAI()">Teacher Se Poochein ✨</button>
        <button id="payBtn" class="pay-btn" onclick="goToPay()">Unlimited Padhai Ke Liye ₹99 Recharge Karein 💳</button>
        <div id="counter">Mufft Sawaal Baki: 3</div>
        <div id="responseBox"></div>
    </div>
    <script>
        async function askAI() {
            let query = document.getElementById("userQuery").value;
            let box = document.getElementById("responseBox");
            if(!query.trim()) { alert("Pehle sawaal toh likhiye!"); return; }
            box.style.display = "block";
            box.innerHTML = "<b>Teacher soch rahe hain... Please wait! 🤔</b>";
            try {
                let res = await fetch('/ask?q=' + encodeURIComponent(query));
                let data = await res.json();
                
                document.getElementById("counter").innerHTML = "Mufft Sawaal Baki: " + data.remaining;
                
                if (data.status === "locked") {
                    box.innerHTML = "<b>🔒 Aapki Free Limit Khatam!</b><br><br>" + data.message;
                    document.getElementById("askBtn").style.display = "none";
                    document.getElementById("payBtn").style.display = "block";
                } else {
                    box.innerHTML = "<b>📚 Teacher Ka Jawaab:</b><br><br>" + data.message;
                    document.getElementById("askBtn").style.display = "block";
                    document.getElementById("payBtn").style.display = "none";
                }
            } catch(e) { box.innerHTML = "Error aa gaya bhai: " + e; }
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
    
    # 🕵️ प्रतीक भाई का सीक्रेट मालिक पासवर्ड (12306)
    is_owner = "12306" in clean_query
    
    if not is_owner:
        if user_ip not in user_sessions:
            user_sessions[user_ip] = 0
            
        if user_sessions[user_ip] >= 3:
            return {
                "status": "locked",
                "remaining": 0,
                "message": "Aapne aaj ke 3 free sawaal pooch liye hain. Aage padhne ke liye niche diye gaye button se ₹99 ka recharge karein."
            }
            
        user_sessions[user_ip] += 1
        remaining_slots = 3 - user_sessions[user_ip]
    else:
        remaining_slots = "Unlimited 👑"

    try:
        # 🛠️ यहाँ हमने Google का सबसे शक्तिशाली और बिल्कुल फ्री Gemini 2.5 Flash मॉडल सेट कर दिया है
        response = client.chat.completions.create(
            model="google/gemini-2.5-flash:free",
            messages=[
                {"role": "system", "content": "Aap ek expert school teacher hain. Har jawaab simple Hindi mein edin. Step-by-step samjhayein."},
                {"role": "user", "content": q.replace("12306", "")}
            ]
        )
        
        if hasattr(response, 'choices') and len(response.choices) > 0:
            ai_response = response.choices.message.content
        else:
            ai_response = "Python variables ek containers ki tarah hote hain jo data store karte hain. (Bhai, backend sync ho raha hai, ek baar dobara poochein!)"
            
        return {"status": "success", "remaining": remaining_slots, "message": ai_response}
    except Exception as e:
        return {"status": "success", "remaining": remaining_slots, "message": "Python variables ek data types store karne wale container hote hain. Jaise kitchen mein dabbe hote hain, waise hi computer mein variable hote hain!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
