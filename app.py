import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# 🌌 सुंदर पर्पल डिज़ाइन और AI इंटरफ़ेस का HTML/CSS कोड
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎓 Student AI Tutor - Premium</title>
    <style>
        :root {
            --primary-purple: #7F56D9;
            --light-purple: #F9F5FF;
            --dark-purple: #42307D;
            --text-dark: #1D2939;
            --premium-pink: #FF4757;
        }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--light-purple); margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 90vh; }
        .chat-container { width: 100%; max-width: 600px; background: white; border-radius: 16px; box-shadow: 0 10px 30px rgba(127, 86, 217, 0.15); overflow: hidden; border: 1px solid rgba(127, 86, 217, 0.2); }
        .header { background: linear-gradient(135deg, var(--primary-purple), var(--dark-purple)); color: white; padding: 20px; text-align: center; position: relative; }
        .header h1 { margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 0.5px; }
        .header p { margin: 5px 0 0 0; font-size: 14px; opacity: 0.9; }
        
        /* 👑 प्रीमियम कार्ड डिज़ाइन */
        .premium-banner { background: #FFFFFF; border: 2px dashed var(--premium-pink); margin: 15px; padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(255, 71, 87, 0.1); }
        .premium-title { font-weight: bold; color: var(--premium-pink); font-size: 18px; margin-bottom: 5px; }
        .premium-price { font-size: 22px; font-weight: 800; color: var(--text-dark); margin: 5px 0; }
        .btn-premium { background: var(--premium-pink); color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; transition: 0.3s; width: 100%; box-shadow: 0 4px 10px rgba(255, 71, 87, 0.3); }
        .btn-premium:hover { background: #E84118; transform: translateY(-1px); }
        
        .chat-box { height: 300px; padding: 20px; overflow-y: auto; background: #FCFAFF; border-bottom: 1px solid #EAECF0; }
        .message { margin-bottom: 15px; padding: 12px 16px; border-radius: 12px; max-width: 80%; font-size: 15px; line-height: 1.4; }
        .bot { background: var(--light-purple); color: var(--dark-purple); margin-right: auto; border-bottom-left-radius: 2px; }
        .user { background: var(--primary-purple); color: white; margin-left: auto; border-bottom-right-radius: 2px; text-align: right; }
        
        .input-area { display: flex; padding: 15px; background: white; gap: 10px; }
        .input-area input { flex: 1; padding: 12px; border: 1px solid #D0D5DD; border-radius: 8px; font-size: 15px; outline: none; transition: 0.2s; }
        .input-area input:focus { border-color: var(--primary-purple); box-shadow: 0 0 0 3px rgba(127, 86, 217, 0.2); }
        .btn-send { background: var(--primary-purple); color: white; border: none; padding: 0 20px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .btn-send:hover { background: var(--dark-purple); }
    </style>
</head>
<body>

<div class="chat-container">
    <!-- हेडर -->
    <div class="header">
        <h1>🎓 Student AI Tutor</h1>
        <p>Your Smart Personalized AI Learning Assistant</p>
    </div>

    <!-- 👑 ₹200 प्रीमियम प्लान अनुभाग -->
    <div class="premium-banner">
        <div class="premium-title">✨ Unlock Ultimate AI Power ✨</div>
        <div class="premium-price">Only ₹200 <span style="font-size: 14px; font-weight: normal; color: #666;">/ Month</span></div>
        <p style="margin: 0 0 12px 0; font-size: 13px; color: #475467;">Get unlimited answers, PDF explanations & faster server speed!</p>
        <button class="btn-premium" onclick="payNow()">👑 Activate Premium Membership</button>
    </div>

    <!-- चैट एरिया -->
    <div class="chat-box" id="chatBox">
        <div class="message bot">Hello! I am your AI Tutor. Ask me any homework question, and I will help you solve it instantly! 🎯</div>
    </div>

    <!-- इनपुट बॉक्स -->
    <div class="input-area">
        <input type="text" id="userInput" placeholder="Ask your AI Tutor anything...">
        <button class="btn-send" onclick="sendMessage()">Ask AI</button>
    </div>
</div>

<!-- रेज़रपे पेमेंट इंटीग्रेशन -->
<script src="https://razorpay.com"></script>
<script>
    function sendMessage() {
        let input = document.getElementById("userInput");
        let chatBox = document.getElementById("chatBox");
        if(input.value.trim() === "") return;

        // User Message
        chatBox.innerHTML += `<div class="message user">${input.value}</div>`;
        let tempUserText = input.value;
        input.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;

        // Mock Bot Response
        setTimeout(() => {
            chatBox.innerHTML += `<div class="message bot">Analyzing your question... To unlock the complete step-by-step verified solution, please subscribe to our <b>Premium Plan</b> above! 🚀</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 800);
    }

    function payNow() {
        var options = {
            "key": "rzp_test_YOUR_KEY_HERE", // अपनी असली Razorpay key यहाँ बदलें
            "amount": 20000, // ₹200 (पैसे में)
            "currency": "INR",
            "name": "Student AI Tutor",
            "description": "Unlock Premium AI Features",
            "handler": function (response){
                alert("🎉 Payment Successful! ID: " + response.razorpay_payment_id + "\\nYour Premium Account is now Active!");
            },
            "prefill": {
                "name": "Premium Student",
                "email": "student@example.com"
            },
            "theme": { "color": "#7F56D9" }
        };
        var rzp1 = new Razorpay(options);
        rzp1.open();
    }
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    # 🟢 100% सफल डिप्लॉयमेंट (हरा टिक) के लिए आवश्यक डायनामिक पोर्ट सेटिंग्स
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
  
