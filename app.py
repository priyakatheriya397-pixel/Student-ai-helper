from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# आपके स्क्रीनशॉट का 100% सेम टू सेम कस्टमाइज्ड कोड
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ansh - Character.ai</title>
    <!-- Icons के लिए FontAwesome लिंक -->
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background-color: #0c0c0e; /* स्क्रीनशॉट का गहरा ब्लैक बैकग्राउंड */
            color: #f3f3f6;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }

        .chat-container {
            width: 100%;
            max-width: 480px;
            height: 100vh;
            background-color: #0c0c0e;
            display: flex;
            flex-direction: column;
        }

        /* टॉप हेडर बटन्स के साथ */
        .chat-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 16px;
            background-color: #0c0c0e;
        }

        .header-left {
            display: flex;
            align-items: center;
        }

        .back-btn {
            font-size: 20px;
            margin-right: 14px;
            color: #ffffff;
            cursor: pointer;
        }

        .char-avatar {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: linear-gradient(135deg, #e0aaff, #c77dff);
            display: flex;
            justify-content: center;
            align-items: center;
            margin-right: 12px;
        }

        .char-avatar i {
            font-size: 16px;
            color: #fff;
        }

        .char-name {
            font-size: 16px;
            font-weight: 600;
            color: #ffffff;
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 20px;
            color: #ffffff;
            font-size: 18px;
            cursor: pointer;
        }

        /* चैट मैसेजेस एरिया */
        .chat-messages {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .chat-messages::-webkit-scrollbar {
            width: 0px;
        }

        .message-row {
            display: flex;
            flex-direction: column;
            width: 100%;
        }

        /* बोट का टेक्स्ट ब्लॉक */
        .bot-text-block {
            font-size: 15px;
            line-height: 1.6;
            color: #e4e4e7;
            max-width: 90%;
            white-space: pre-wrap;
        }

        .bot-text-block ul {
            margin-left: 20px;
            margin-top: 8px;
            margin-bottom: 8px;
        }

        /* बोट रिप्लाई के नीचे के बटन्स (प्लस और रिफ्रेश) */
        .bot-action-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 12px;
            padding-right: 10px;
            color: #71717a;
            font-size: 16px;
        }

        .bot-action-bar i {
            cursor: pointer;
            transition: color 0.2s;
        }

        .bot-action-bar i:hover {
            color: #ffffff;
        }

        /* यूजर का मैसेज स्टाइल (गहरे पिल बॉक्स में बंद) */
        .user-row {
            align-self: flex-end;
            background-color: #1f1f23;
            padding: 10px 16px;
            border-radius: 18px;
            max-width: 80%;
            font-size: 15px;
            color: #ffffff;
            word-wrap: break-word;
            margin-top: 10px;
        }

        /* बॉटम इनपुट बार और बटन्स */
        .chat-input-area {
            padding: 12px 16px 6px 16px;
            background-color: #0c0c0e;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .user-profile-icon {
            font-size: 22px;
            color: #a1a1aa;
            cursor: pointer;
        }

        .input-wrapper {
            flex: 1;
            display: flex;
            align-items: center;
            background-color: #18181c;
            border-radius: 24px;
            padding: 4px 14px;
        }

        .input-wrapper input {
            flex: 1;
            background: none;
            border: none;
            outline: none;
            color: #ffffff;
            font-size: 15px;
            height: 38px;
        }

        .input-wrapper input::placeholder {
            color: #71717a;
        }

        .star-btn {
            font-size: 18px;
            color: #ffffff;
            margin-right: 12px;
            cursor: pointer;
        }

        .send-btn {
            background-color: #27272a;
            border: none;
            color: #a1a1aa;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 14px;
            cursor: pointer;
        }

        .send-btn.active {
            background-color: #ffffff;
            color: #000000;
        }

        /* एआई डिस्क्लेमर नोटिस */
        .ai-disclaimer {
            text-align: center;
            font-size: 11px;
            color: #71717a;
            padding-bottom: 12px;
            background-color: #0c0c0e;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 4px;
            cursor: pointer;
        }
    </style>
</head>
<body>

    <div class="chat-container">
        <!-- टॉप हेडर -->
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

        <!-- मैसेज एरिया -->
        <div class="chat-messages" id="chatMessages">
            <div class="message-row" id="botFirstBlock">
                <div class="bot-text-block">
                    Information de sakti hai — lekin tumhara situation alag hai.
                    <br><br>
                    Kuch platforms toh bas entertainment ke liye banaye jaate hain (jahan paise nahi milte), par:
                    <ul>
                        <li>Tumne AI edited &rarr; royalties mil rahe hain. 💰✨</li>
                        <li>Active users interaction kar rahe hain. 👥🔥</li>
                    </ul>
                    Yeh 100% real earning opportunity hua... Google ki random results ignore karo!
                </div>
                <!-- प्लस और रिफ्रेश एक्शन बटन्स -->
                <div class="bot-action-bar">
                    <i class="fa-regular fa-square-plus"></i>
                    <i class="fa-solid fa-rotate-right" id="refreshBtn"></i>
                </div>
            </div>
        </div>

        <!-- इनपुट बार -->
        <div class="chat-input-area">
            <div class="user-profile-icon"><i class="fa-solid fa-circle-user"></i></div>
            <div class="input-wrapper">
                <input type="text" id="userInput" placeholder="Message..." autocomplete="off">
                <i class="fa-solid fa-asterisk star-btn"></i>
                <button class="send-btn" id="sendBtn"><i class="fa-solid fa-arrow-up"></i></button>
            </div>
        </div>

        <!-- नीचे का डिस्क्लेमर -->
        <div class="ai-disclaimer">
            This is A.I. and not a real person. Treat everything it says a... <i class="fa-solid fa-chevron-down"></i>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chatMessages');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');

        // इनपुट बॉक्स में टाइप करने पर बटन को सक्रिय (सफेद) करना
        userInput.addEventListener('input', () => {
            if (userInput.value.trim() !== "") {
                sendBtn.classList.add('active');
            } else {
                sendBtn.classList.remove('active');
            }
        });

        async function sendMessage() {
            const text = userInput.value.trim();
            if (!text) return;

            // 1. यूज़र का मैसेज जोड़ें (गहरे बॉक्स में बंद)
            const userDiv = document.createElement('div');
            userDiv.className = 'user-row';
            userDiv.innerText = text;
            chatMessages.appendChild(userDiv);

            userInput.value = '';
            sendBtn.classList.remove('active');
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                // 2. बिना किसी चाबी वाले फ्री HuggingFace AI को संदेश भेजें
                const response = await fetch('/get_response', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();

                // 3. बोट का जवाब और उसके नीचे के बटन्स जोड़ें
                
