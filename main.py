<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Studio</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: #0b031a;
            color: #ffffff;
            overflow-x: hidden;
        }

        /* 1. टॉप सर्च/लोडिंग लाइन एनीमेशन */
        #top-loading-bar {
            position: fixed;
            top: 0;
            left: 0;
            height: 4px;
            background: linear-gradient(90deg, #ff007f, #7f00ff, #00f0ff);
            width: 0%;
            z-index: 9999;
            transition: width 0.4s ease;
            box-shadow: 0 0 10px #7f00ff, 0 0 20px #ff007f;
        }

        .page {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .hidden {
            display: none !important;
        }

        /* ब्रांडिंग हेडर स्टाइल */
        .brand-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 30px;
        }

        .brand-logo {
            font-size: 32px;
            filter: drop-shadow(0 0 8px #00f0ff);
        }

        .brand-name {
            font-size: 28px;
            font-weight: bold;
            letter-spacing: 1px;
            background: linear-gradient(45deg, #00f0ff, #7f00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }

        /* एक्शन बटन स्टाइल */
        .button-container {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }

        .action-btn {
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            color: white;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }

        .btn-create { background: linear-gradient(135deg, #4d66ff, #2544ff); }
        .btn-edit { background: linear-gradient(135deg, #ff9f43, #ff6b6b); }
        .btn-video { background: linear-gradient(135deg, #a55eea, #8854d0); }

        .action-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(127, 0, 255, 0.4);
        }

        /* 2. आपका पसंदीदा फैंसी पर्पल पेज (कलर बदलने वाला बैकग्राउंड) */
        #studio-page {
            background: linear-gradient(125deg, #120024, #2c004d, #1a0033, #0b031a);
            background-size: 400% 400%;
            animation: gradientMove 12s ease infinite;
        }

        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .studio-container {
            text-align: center;
            width: 100%;
            max-width: 600px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px rgba(255, 255, 255, 0.1) solid;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .studio-container h1 {
            font-size: 24px;
            margin-bottom: 20px;
            font-weight: 500;
            letter-spacing: 0.5px;
        }

        /* इंग्लिश इनपुट बॉक्स */
        .prompt-box {
            width: 100%;
            height: 120px;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            color: white;
            padding: 15px;
            font-size: 16px;
            resize: none;
            outline: none;
            transition: border 0.3s;
            margin-bottom: 20px;
        }

        .prompt-box:focus {
            border-color: #8854d0;
            box-shadow: 0 0 10px rgba(136, 84, 208, 0.5);
        }

        .send-btn {
            background: linear-gradient(135deg, #7f00ff, #ff007f);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(255, 0, 127, 0.6);
        }

        /* 3. पृथक हेल्प चैट विजेट स्टाइल */
        #help-widget-container {
            position: fixed;
            bottom: 25px;
            right: 25px;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }

        .help-trigger-btn {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #00f0ff, #7f00ff);
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0, 240, 255, 0.4);
            display: flex;
            justify-content: center;
            align-items: center;
            transition: transform 0.3s;
        }

        .help-trigger-btn:hover {
            transform: scale(1.1) rotate(5deg);
        }

        .help-chat-box {
            width: 320px;
            height: 400px;
            background: #150c2a;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.6);
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .help-chat-header {
            background: linear-gradient(90deg, #1a0a3a, #2c004d);
            padding: 12px 15px;
            font-weight: 600;
            font-size: 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .close-help {
            cursor: pointer;
            opacity: 0.7;
            background: none;
            border: none;
            color: white;
            font-size: 16px;
        }

        .close-help:hover { opacity: 1; }

        .help-chat-messages {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            font-size: 13px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            color: #ffffff;
        }

        .msg {
            padding: 8px 12px;
            border-radius: 12px;
            max-width: 85%;
        }

        .msg.bot {
            background: rgba(255, 255, 255, 0.08);
            align-self: flex-start;
            border-bottom-left-radius: 2px;
        }

        .help-chat-input-area {
            padding: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            gap: 8px;
            background: #0b031a;
        }

        .help-input {
            flex: 1;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 8px 14px;
            color: white;
            font-size: 13px;
            outline: none;
        }

        .help-input:focus { border-color: #00f0ff; }

        .help-send-btn {
            background: #7f00ff;
            border: none;
            color: white;
            padding: 0 15px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 600;
        }
    </style>
</head>
<body>

    <!-- टॉप सर्च/लोडिंग लाइन -->
    <div id="top-loading-bar"></div>

    <!-- पहला पेज (होम स्क्रीन) -->
    <div id="home-page" class="page">
        <div class="brand-header">
            <span class="brand-logo">🤖</span>
            <span class="brand-name">Chatbot</span>
        </div>
        <h2>Select an Option to Build</h2>
        <div class="button-container">
            <button class="action-btn btn-create" onclick="triggerPageTransition('Web Design')">Create Web</button>
            <button class="action-btn btn-edit" onclick="triggerPageTransition('Edit Web')">Edit Web</button>
            <button class="action-btn btn-video" onclick="triggerPageTransition('Video AI')">Video AI</button>
        </div>
    </div>

    <!-- नया फैंसी पर्पल पेज -->
    <div id="studio-page" class="page hidden">
        <div class="studio-container">
            <h1>Describe what you have to build</h1>
            <textarea class="prompt-box" placeholder="Type your design requirements here..."></textarea>
            <button class="send-btn" onclick="submitPrompt()">Generate ✨</button>
        </div>
    </div>

    <!-- फ्लोटिंग हेल्प चैट विजेट -->
    <div id="help-widget-container">
        <div id="helpChatBox" class="help-chat-box hidden">
            <div class="help-chat-header">
                <span>💬 Assistant Help Support</span>
                <button class="close-help" onclick="toggleHelpChat()">✕</button>
            </div>
            <div class="help-chat-messages">
                <div class="msg bot">Hello! How can I help you build or edit your project today?</div>
            </div>
            <div class="help-chat-input-area">
                <input type="text" class="help-input" placeholder="Ask a support question...">
                <button class="help-send-btn">Send</button>
            </div>
        </div>
        
