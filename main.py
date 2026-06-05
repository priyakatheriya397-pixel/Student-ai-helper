html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Student Helper AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* 🎨 पुराना लेआउट और साथ में नया पर्पल टच */
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f3e8ff; margin: 0; padding: 0; display: flex; justify-content: center; height: 100vh; }
        .chat-container { width: 100%; max-width: 500px; background: #faf5ff; display: flex; flex-direction: column; height: 100vh; box-shadow: 0 4px 20px rgba(147, 51, 234, 0.2); }
        .chat-header { background: #7c3aed; color: white; padding: 15px; text-align: center; position: relative; box-shadow: 0 4px 10px rgba(0,0,0,0.15); border-bottom: 3px solid #6d28d9; }
        .chat-header h2 { margin: 0; font-size: 20px; display: flex; align-items: center; justify-content: center; gap: 10px; }
        .chat-header span { display: block; font-size: 13px; color: #c084fc; margin-top: 4px; font-weight: bold; }
        .chat-box { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; background-image: radial-gradient(#e9d5ff 1px, transparent 1px); background-size: 20px 20px; }
        .message { max-width: 78%; padding: 12px 16px; border-radius: 15px; font-size: 15px; line-height: 1.5; word-wrap: break-word; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .user-msg { background: #e9d5ff; align-self: flex-end; color: #4c1d95; border-top-right-radius: 0; border: 1px solid #ddd6fe; }
        .bot-msg { background: #ffffff; align-self: flex-start; color: #111b21; border-top-left-radius: 0; border: 1px solid #f3e8ff; }
        .system-msg { background: #fee2e2; align-self: center; text-align: center; font-size: 13px; color: #991b1b; max-width: 90%; border-radius: 8px; border: 1px solid #fca5a5; padding: 10px; }
        .input-area { background: #ffffff; padding: 12px; display: flex; gap: 10px; align-items: center; border-top: 1px solid #e9d5ff; }
        input[type="text"] { flex: 1; padding: 14px; border: 2px solid #ddd6fe; border-radius: 25px; font-size: 16px; outline: none; background: #fdfbf7; color: #4c1d95; }
        button { background: #7c3aed; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 25px; cursor: pointer; font-weight: bold; box-shadow: 0 3px 6px rgba(124, 58, 237, 0.3); }
        .pay-btn { background: #ef4444; width: 90%; align-self: center; margin: 10px 0; border-radius: 12px; display: none; text-align: center; text-decoration: none; font-weight: bold; color: white; padding: 14px; }
        
        /* 🎛️ नया छोटा टूल्स कंटेनर जो चैट के नीचे दिखेगा */
        .extra-tools { display: flex; gap: 10px; justify-content: center; padding: 10px; background: #faf5ff; border-top: 1px solid #e9d5ff; }
        .mini-btn { background: #a78bfa; color: white; border: none; padding: 8px 12px; font-size: 12px; border-radius: 15px; cursor: pointer; font-weight: bold; }
        .mini-btn:hover { background: #7c3aed; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h2>🐱 Smart Student Helper AI</h2>
            <span id="counter">Mufft Sawaal Baki: 3</span>
        </div>
        <div class="chat-box" id="chatBox">
            <div class="message bot-msg"><b>🐱 Smart Cat Teacher:</b> Hello Pratik bhai! Meow ✨ Aaj aap apni book ka kaun sa sawaal seekhna chahte hain? Poochhiye! 💜</div>
        </div>
        
        <!-- 🎛️ छोटे टूल ऑप्शंस यहाँ जोड़ दिए हैं -->
        <div class="extra-tools">
            <button class="mini-btn" onclick="setMode('web_create')">🌐 Create Web</button>
            <button class="mini-btn" onclick="setMode('web_edit')">✍️ Edit Web</button>
            <button class="mini-btn" onclick="setMode('video_ai')">🎥 Video AI</button>
        </div>

        <a id="payBtn" class="pay-btn" href="javascript:void(0);" onclick="goToPay()">🔒 Unlimited Padhai Ke Liye ₹99 Recharge Karein</a>
        <div class="input-area" id="inputArea">
            <input type="text" id="userQuery" placeholder="Yahan apna sawaal likhein..." onkeypress="checkEnter(event)">
            <button id="askBtn" onclick="askAI()">Bhejein 🚀</button>
        </div>
    </div>
    <script>
        let currentMode = "general";
        function setMode(mode) {
            currentMode = mode;
            let chatBox = document.getElementById("chatBox");
            if(mode === 'web_create') chatBox.innerHTML += `<div class="message bot-msg"><b>🤖 System:</b> Web Creator Mode चालू है! अपना प्रॉम्प्ट लिखें।</div>`;
            if(mode === 'web_edit') chatBox.innerHTML += `<div class="message bot-msg"><b>🤖 System:</b> Web Editor Mode चालू है! अपना कोड पेस्ट करें।</div>`;
            if(mode === 'video_ai') chatBox.innerHTML += `<div class="message bot-msg"><b>🤖 System:</b> Video Assistant Mode चालू है! टॉपिक बताएं।</div>`;
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
            chatBox.innerHTML += `<div class="message bot-msg" id="${waitingId}"><b>🐱 Cat soch rahi hai... Meow... 🤔</b></div>`;
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                // यहाँ बैकएंड एंडपॉइंट पर क्वेरी के साथ मोड (mode) भी भेजा जा रहा है
                let res = await fetch('/ask?q=' + encodeURIComponent(query) + '&mode=' + currentMode);
                let data = await res.json();
                
                document.getElementById("counter").innerHTML = "Mufft Sawaal Baki: " + data.remaining;
                document.getElementById(waitingId).remove();

                if (data.status === "locked") {
                    chatBox.innerHTML += `<div class="message system-msg"><b>🔒 Aapki Free Limit Khatam!</b><br>${data.message}</div>`;
                    document.getElementById("inputArea").style.display = "none";
                    document.getElementById("payBtn").style.display = "block";
                } else {
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
