<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Studio</title>
    <style>
        /* 1. बेसिक रिसेट और फ़ॉन्ट्स */
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

        /* 2. ग्लोबल टॉप लोडिंग/सर्च लाइन एनीमेशन */
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

        /* 3. पहला पेज (होम स्क्रीन जहां 3 बटन हैं) */
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

        /* बटन कंटेनर स्टाइल */
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

        /* 4. नया फैंसी पर्पल पेज (एनिमेटेड बैकग्राउंड) */
        #studio-page {
            background: linear-gradient(125deg, #120024, #2c004d, #1a0033, #0b031a);
            background-size: 400% 400%;
            animation: gradientMove 12s ease infinite;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* नए पेज का कंटेंट बॉक्स */
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

        /* नया इंग्लिश इनपुट बॉक्स */
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
    </style>
</head>
<body>

    <!-- 1. टॉप सर्च/लोडिंग लाइन -->
    <div id="top-loading-bar"></div>

    <!-- 2. पहला पेज (होम/चैट स्क्रीन का विकल्प) -->
    <div id="home-page" class="page">
        <h2>Select an Option to Build</h2>
        <div class="button-container">
            <!-- आपके तीनों एक्शन बटन -->
            <button class="action-btn btn-create" onclick="triggerPageTransition('Web Design')">Create Web</button>
            <button class="action-btn btn-edit" onclick="triggerPageTransition('Edit Web')">Edit Web</button>
            <button class="action-btn btn-video" onclick="triggerPageTransition('Video AI')">Video AI</button>
        </div>
    </div>

    <!-- 3. नया फैंसी पर्पल पेज -->
    <div id="studio-page" class="page hidden">
        <div class="studio-container">
            <!-- नया इंग्लिश हेडिंग -->
            <h1 id="studio-title">Describe what you have to build</h1>
            <!-- इनपुट बॉक्स -->
            <textarea class="prompt-box" placeholder="Type your design requirements here..."></textarea>
            <!-- इंग्लिश सबमिट बटन -->
            <button class="send-btn">Generate ✨</button>
        </div>
    </div>

    <script>
        function triggerPageTransition(modeName) {
            const loadingBar = document.getElementById('top-loading-bar');
            const homePage = document.getElementById('home-page');
            const studioPage = document.getElementById('studio-page');
            
            // 1. टॉप लाइन एनीमेशन शुरू करना (0% से 100%)
            loadingBar.style.width = '30%';
            
            setTimeout(() => {
                loadingBar.style.width = '70%';
            }, 300);

            setTimeout(() => {
                loadingBar.style.width = '100%';
            }, 600);

            // 2. लोड पूरा होने पर नया पेज खोलना
            setTimeout(() => {
                // होम पेज छुपाएं और नया फैंसी पर्पल पेज दिखाएं
                homePage.classList.add('hidden');
                studioPage.classList.remove('hidden');
                
                // लोडिंग बार को वापस रीसेट करें
                loadingBar.style.width = '0%';
            }, 1000); // 1 सेकंड का लोडिंग टाइमर
        }
    </script>
</body>
</html>
