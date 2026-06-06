import os
from flask import Flask, render_template_string, request, jsonify
app = Flask(__name__)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎓 Student AI Portal - Admin Access</title>
    <style>
        :root {
            --primary-purple: #7F56D9;
            --light-purple: #F9F5FF;
            --dark-purple: #42307D;
            --text-dark: #1D2939;
            --premium-pink: #FF4757;
            --success-green: #2ECC71;
        }
        body { font-family: 'Segoe UI', sans-serif; background-color: var(--light-purple); margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 95vh; }
        .container { width: 100%; max-width: 650px; background: white; border-radius: 16px; box-shadow: 0 10px 30px rgba(127, 86, 217, 0.15); overflow: hidden; border: 1px solid rgba(127, 86, 217, 0.2); }
        .header { background: linear-gradient(135deg, var(--primary-purple), var(--dark-purple)); color: white; padding: 25px; text-align: center; }
        .header h1 { margin: 0; font-size: 26px; font-weight: 600; }
        .header p { margin: 5px 0 0 0; font-size: 14px; opacity: 0.9; }
        
        /* 👑 प्रीमियम और मालिक लॉगिन सेक्शन */
        .premium-banner { background: #FFFFFF; border: 2px dashed var(--premium-pink); margin: 20px; padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(255, 71, 87, 0.1); }
        .premium-title { font-weight: bold; color: var(--premium-pink); font-size: 18px; margin-bottom: 5px; }
        .premium-price { font-size: 22px; font-weight: 800; color: var(--text-dark); margin: 5px 0; }
        .btn-premium { background: var(--premium-pink); color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; transition: 0.3s; width: 100%; box-shadow: 0 4px 10px rgba(255, 71, 87, 0.3); }
        .btn-premium:hover { background: #E84118; transform: translateY(-1px); }
        
        /* 🔑 मालिक के लिए पासवर्ड बॉक्स */
        .owner-zone { margin-top: 12px; display: flex; gap: 8px; justify-content: center; align-items: center; background: #FFF5F5; padding: 8px; border-radius: 6px; }
        .owner-zone input { padding: 6px 10px; border: 1px solid #FFCCD2; border-radius: 4px; outline: none; width: 140px; text-align: center; }
        .btn-owner { background: var(--dark-purple); color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 13px; }
        
        /* 🛠️ आपके मुख्य 3 ऑप्शंस */
        .services-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; padding: 0 20px 20px 20px; }
        .service-card { background: #FCFAFF; border: 1px solid rgba(127, 86, 217, 0.15); padding: 15px 10px; border-radius: 10px; text-align: center; cursor: pointer; transition: 0.2s; font-weight: 600; color: var(--dark-purple); font-size: 14px; }
        .service-card:hover { background: var(--primary-purple); color: white; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(127, 86, 217, 0.2); }
        .service-icon { font-size: 24px; margin-bottom: 8px; display: block; }

        /* चैट एरिया */
        .chat-box { height: 220px; padding: 20px; overflow-y: auto; background: #FFF; border-top: 1px solid #EAECF0; border-bottom: 1px solid #EAECF0; }
        .message { margin-bottom: 15px; padding: 12px 16px; border-radius: 12px; max-width: 80%; font-size: 15px; line-height: 1.4; }
        .bot { background: var(--light-purple); color: var(--dark-purple); margin-right: auto; border-bottom-left-radius: 2px; }
        .user { background: var(--primary-purple); color: white; margin-left: auto; border-bottom-right-radius: 2px; text-align: right; }
        
        .input-area { display: flex; padding: 15px; background: white; gap: 10px; }
        .input-area input { flex: 1; padding: 12px; border: 1px solid #D0D5DD; border-radius: 8px; font-size: 15px; outline: none; }
        .btn-send { background: var(--primary-purple); color: white; border: none; padding: 0 20px; border-radius: 8px; font-weight: 600; cursor: pointer; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>🎓 Student AI Portal</h1>
        <p>All-in-One AI Assistant & Premium Services</p>
    </div>

    <!-- 👑 ₹200 प्रीमियम प्लान और मालिक के लिए सीक्रेट एंट्री -->
    <div class="premium-banner" id="premiumBanner">
        <div class="premium-title">✨ Unlock Ultimate Premium Access ✨</div>
        <div class="premium-price">Only ₹200 <span style="font-size: 14px; font-weight: normal; color: #666;">/ Month</span></div>
        <button class="btn-premium" onclick="payNow()">👑 Activate Premium Membership</button>
        
        <!-- 🔑 यहाँ आप अपना सीक्रेट पासवर्ड डालेंगे -->
        <div class="owner-zone">
            <span style="font-size: 12px; color: #555;">🔑 Owner Bypass:</span>
            <input type="password" id="ownerPass" placeholder="Enter Password">
            <button class="btn-owner" onclick="checkOwnerAccess()">Unlock</button>
        </div>
    </div>

    <!-- 🌐 आपके वे 3 मुख्य ऑप्शंस -->
    <div class="services-grid">
        <div class="service-card" onclick="selectService('Web Design')">
            <span class="service-icon">💻</span> Web Design
        </div>
        <div class="service-card" onclick="selectService('Video Editor')">
            <span class="service-icon">🎬</span> Video Editor
        </div>
        <div class="service-card" onclick="selectService('AI Tutor')">
            <span class="service-icon">🤖</span> AI Tutor
        </div>
    </div>

    <div class="chat-box" id="chatBox">
        <div class="message bot">Welcome! Please click on any option above (Web Design, Video Editor, AI Tutor) or type your message here to start! 🚀</div>
    </div>

    <div class="input-area">
        <input type="text" id="userInput" placeholder="Type or choose a service above...">
        <button class="btn-send" onclick="sendMessage()">Ask AI</button>
    </div>
</div>

<script src="https://razorpay.com"></script>
<script>
    let isPremiumUser = false; // शुरुआत में प्रीमियम बंद रहेगा

    // 🔒 मालिक का सीक्रेट पासवर्ड चेक करने वाला फंक्शन
    function checkOwnerAccess() {
        let passInput = document.getElementById("ownerPass").value;
        let banner = document.getElementById("premiumBanner");
        let chatBox = document.getElementById("chatBox");

        if (passInput === "12306") {
            isPremiumUser = true;
            banner.innerHTML = `<div style="color: var(--success-green); font-weight: bold; padding: 10px; font-size: 18px;">👑 Owner / Admin Access Activated Successfully! 👑</div>`;
            chatBox.innerHTML += `<div class="message bot" style="background: #E8F5E9; color: #2E7D32;"><b>System:</b> Master Password Accepted! All services are now unlocked forever without payment. 😎</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        } else {
            alert("❌ Wrong Owner Password! Try again.");
        }
    }

    function selectService(serviceName) {
        let chatBox = document.getElementById("chatBox");
        chatBox.innerHTML += `<div class="message user">I want to use ${serviceName} Service</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;

        setTimeout(() => {
            if (isPremiumUser) {
                // अगर मालिक लॉग इन है तो सीधा जवाब मिलेगा
                chatBox.innerHTML += `<div class="message bot" style="border: 2px solid var(--success-green);">✨ <b>[PREMIUM UNLOCKED]</b> Here is your professional <b>${serviceName}</b> generation tool. Ready to use! ✅</div>`;
            } else {
                // आम ग्राहक के लिए पेमेंट की मांग
                chatBox.innerHTML += `<div class="message bot">You selected <b>${serviceName}</b>. To access full premium templates and tools for this service, please activate your <b>Premium Plan</b> above! 💎</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 600);
    }

    function sendMessage() {
        let input = document.getElementById("userInput");
        let chatBox = document.getElementById("chatBox");
        if(input.value.trim() === "") return;

        chatBox.innerHTML += `<div class="message user">${input.value}</div>`;
        input.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;

        setTimeout(() => {
            if (isPremiumUser) {
                chatBox.innerHTML += `<div class="message bot" style="border: 2px solid var(--success-green);">✨ <b>[PREMIUM ANSWER]</b> AI Tutor solved your homework perfectly! (No limits for Owner) 🎯</div>`;
            } else {
                chatBox.innerHTML += `<div class="message bot">Processing... Please subscribe to our <b>Premium Plan</b> above to unlock instant expert generation! 🚀</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 800);
    }

    function payNow() {
        var options = {
            "key": "rzp_test_YOUR_KEY_HERE",
            "amount": 20000, 
            "currency": "INR",
            "name": "Student AI Portal",
            "description": "Unlock All Services & AI Features",
            "handler": function (response){
                isPremiumUser = true;
                document.getElementById("premiumBanner").innerHTML = `<div style="color: var(--success-green); font-weight: bold; padding: 10px;">✨ Premium Subscription Active! ✨</div>`;
                alert("🎉 Payment Successful! ID: " + response.razorpay_payment_id);
            },
            "prefill": { "name": "Premium Student", "email": "student@example.com" },
            "theme": { "color": "#7F56D9" }
        };
        var rzp1 = new Razorpay(options);
        rzp1.open();
    }
</script>

</body>
</html>
