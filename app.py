import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# 🌌 सुंदर पर्पल डिज़ाइन + 3 ऑप्शंस + असली AI जवाब + मालिक पासवर्ड लॉजिक
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎓 Student AI Portal</title>
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
        
        .premium-banner { background: #FFFFFF; border: 2px dashed var(--premium-pink); margin: 20px; padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(255, 71, 87, 0.1); }
        .premium-title { font-weight: bold; color: var(--premium-pink); font-size: 18px; margin-bottom: 5px; }
        .premium-price { font-size: 22px; font-weight: 800; color: var(--text-dark); margin: 5px 0; }
        .btn-premium { background: var(--premium-pink); color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; transition: 0.3s; width: 100%; box-shadow: 0 4px 10px rgba(255, 71, 87, 0.3); }
        .btn-premium:hover { background: #E84118; transform: translateY(-1px); }
        
        .owner-zone { margin-top: 12px; display: flex; gap: 8px; justify-content: center; align-items: center; background: #FFF5F5; padding: 8px; border-radius: 6px; }
        .owner-zone input { padding: 6px 10px; border: 1px solid #FFCCD2; border-radius: 4px; outline: none; width: 140px; text-align: center; }
        .btn-owner { background: var(--dark-purple); color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 13px; }
        
        .services-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; padding: 0 20px 20px 20px; }
        .service-card { background: #FCFAFF; border: 1px solid rgba(127, 86, 217, 0.15); padding: 15px 10px; border-radius: 10px; text-align: center; cursor: pointer; transition: 0.2s; font-weight: 600; color: var(--dark-purple); font-size: 14px; }
        .service-card:hover { background: var(--primary-purple); color: white; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(127, 86, 217, 0.2); }
        .service-icon { font-size: 24px; margin-bottom: 8px; display: block; }

        .chat-box { height: 250px; padding: 20px; overflow-y: auto; background: #FFF; border-top: 1px solid #EAECF0; border-bottom: 1px solid #EAECF0; }
        .message { margin-bottom: 15px; padding: 12px 16px; border-radius: 12px; max-width: 80%; font-size: 15px; line-height: 1.4; display: block; clear: both; box-sizing: border-box; }
        .bot { background: var(--light-purple); color: var(--dark-purple); float: left; border-bottom-left-radius: 2px; }
        .user { background: var(--primary-purple); color: white; float: right; border-bottom-right-radius: 2px; }
        
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

    <div class="premium-banner" id="premiumBanner">
        <div class="premium-title">✨ Unlock Ultimate Premium Access ✨</div>
        <div class="premium-price">Only ₹200 <span style="font-size: 14px; font-weight: normal; color: #666;">/ Month</span></div>
        <button class="btn-premium" onclick="payNow()">👑 Activate Premium Membership</button>
        
        <div class="owner-zone">
            <span style="font-size: 12px; color: #555;">🔑 Owner Bypass:</span>
            <input type="password" id="ownerPass" placeholder="Enter Password">
            <button class="btn-owner" onclick="checkOwnerAccess()">Unlock</button>
        </div>
    </div>

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
        <div class="message bot">Welcome! Please click on any option above or type your homework question below! 🚀</div>
    </div>

    <div class="input-area">
        <input type="text" id="userInput" placeholder="Type your question here...">
        <button class="btn-send" onclick="sendMessage()">Ask AI</button>
    </div>
</div>

<script src="https://razorpay.com"></script>
<script>
    let isPremiumUser = false;
    let selectedMode = "AI Tutor";

    function checkOwnerAccess() {
        let passInput = document.getElementById("ownerPass").value;
        let banner = document.getElementById("premiumBanner");
        let chatBox = document.getElementById("chatBox");

        if (passInput === "12306") {
            isPremiumUser = true;
            banner.innerHTML = `<div style="color: var(--success-green); font-weight: bold; padding: 10px; font-size: 18px;">👑 Owner / Admin Access Activated Successfully! 👑</div>`;
            chatBox.innerHTML += `<div class="message bot" style="background: #E8F5E9; color: #2E7D32; float: left; width: 100%;"><b>System:</b> Master Password Accepted! All services unlocked for Admin. 😎</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        } else {
            alert("❌ Wrong Owner Password!");
        }
    }

    function selectService(serviceName) {
        selectedMode = serviceName;
        let chatBox = document.getElementById("chatBox");
        chatBox.innerHTML += `<div class="message user">${serviceName} Service चयनित की गई।</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;

        setTimeout(() => {
            chatBox.innerHTML += `<div class="message bot">Now ready for <b>${serviceName}</b>. Ask your question below! 🎯</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 500);
    }

    async function sendMessage() {
        let input = document.getElementById("userInput");
        let chatBox = document.getElementById("chatBox");
        let text = input.value.trim();
        if(text === "") return;

        chatBox.innerHTML += `<div class="message user">${text}</div>`;
        input.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;

        if (!isPremiumUser) {
            setTimeout(() => {
                chatBox.innerHTML += `<div class="message bot">⚠️ <b>Premium Required:</b> To view the complete verified answer for "${text}", please subscribe to our <b>Premium Plan</b> or log in as Owner! 💎</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 600);
            return;
        }

        chatBox.innerHTML += `<div class="message bot" id="loading-msg">🤖 AI is thinking...</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            let response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: text, mode: selectedMode })
            });
            let data = await response.json();
            
            let loadingEl = document.getElementById("loading-msg");
            if(loadingEl) loadingEl.remove();
            
            chatBox.innerHTML += `<div class="message bot" style="border-left: 4px solid var(--success-green);">✨ <b>[PREMIUM ANSWER]</b><br>${data.answer}</div>`;
        } catch (err) {
            let loadingEl = document.getElementById("loading-msg");
            if(loadingEl) loadingEl.remove();
            chatBox.innerHTML += `<div class="message bot">❌ Server Busy. Please try again!</div>`;
        }
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function payNow() {
        var options = {
            "key": "rzp_test_YOUR_KEY_HERE",
            "amount": 20000, 
            "currency": "INR",
            "name": "Student AI Portal",
            "description": "Unlock All Services",
            "handler": function (response){
                isPremiumUser = true;
                document.getElementById("premiumBanner").innerHTML = `<div style="color: var(--success-green); font-weight: bold; padding: 10px;">✨ Premium Subscription Active! ✨</div>`;
                alert("🎉 Payment Successful!");
            },
            "theme": { "color": "#7F56D9" }
        };
        var rzp1 = new Razorpay(options);
        rzp1.open();
    }
</script>
</body>
</html>"""


@app.route('/')
def home():
