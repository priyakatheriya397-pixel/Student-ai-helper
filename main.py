from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# 1. मुख्य रूट जो नया फैंसी इंग्लिश पेज लोड करेगा
@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
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

            /* टॉप सर्च/लोडिंग लाइन एनीमेशन */
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

            /* नया फैंसी पर्पल पेज (कलर बदलने वाला बैकग्राउंड) */
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

        <!-- टॉप सर्च/लोडिंग लाइन -->
        <div id="top-loading-bar"></div>

        <!-- पहला पेज (होम/चैट स्क्रीन का विकल्प) -->
        <div id="home-page" class="page">
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

        <script>
            function triggerPageTransition(modeName) {
                const loadingBar = document.getElementById('top-loading-bar');
                const homePage = document.getElementById('home-page');
                const studioPage = document.getElementById('studio-page');
                
                loadingBar.style.width = '40%';
                
                setTimeout(() => { loadingBar.style.width = '80%'; }, 200);
                setTimeout(() => { loadingBar.style.width = '100%'; }, 400);

                setTimeout(() => {
                    homePage.classList.add('hidden');
                    studioPage.classList.remove('hidden');
                    loadingBar.style.width = '0%';
                }, 700);
            }

            function submitPrompt() {
                alert("Prompt submitted! Connecting to Python backend...");
                // भविष्य में बैकएंड API से कनेक्ट करने का कोड यहाँ आएगा
            }
        </script>
    </body>
    </html>
    """
    return html_content

# 2. बैकएंड प्रोसेसिंग के लिए API रूट (भविष्य में काम आएगा)
@app.post("/generate")
async def generate_response(prompt: str):
    return {"status": "success", "message": f"Processing prompt: {prompt}"}
    
