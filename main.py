from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chatbot Studio AI</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            body {
                background: linear-gradient(135deg, #2e1a47, #120c1f);
                color: #ffffff;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                width: 100%;
                max-width: 650px;
                text-align: center;
            }
            h1 {
                font-size: 2.2rem;
                margin-bottom: 10px;
                font-weight: 600;
                background: linear-gradient(to right, #b388ff, #ea80fc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            p {
                color: #b3a4cb;
                margin-bottom: 30px;
                font-size: 1rem;
            }
            .search-box {
                background: rgba(255, 255, 255, 0.07);
                border: 1px solid rgba(179, 136, 255, 0.3);
                border-radius: 16px;
                padding: 15px;
                display: flex;
                flex-direction: column;
                gap: 10px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
                backdrop-filter: blur(4px);
                margin-bottom: 35px;
            }
            .search-box textarea {
                background: transparent;
                border: none;
                color: #ffffff;
                resize: none;
                font-size: 1.1rem;
                outline: none;
                width: 100%;
                height: 80px;
            }
            .search-box textarea::placeholder {
                color: #796693;
            }
            .search-btn {
                background: #7c4dff;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 12px;
                font-weight: bold;
                cursor: pointer;
                align-self: flex-end;
                transition: 0.3s;
            }
            .search-btn:hover {
                background: #651fff;
                transform: translateY(-2px);
            }
            .options-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 12px;
                width: 100%;
            }
            .option-card {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 20px 10px;
                cursor: pointer;
                transition: 0.3s;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 10px;
            }
            .option-card:hover {
                background: rgba(124, 77, 255, 0.15);
                border-color: #7c4dff;
                transform: translateY(-3px);
            }
            .icon {
                font-size: 1.5rem;
            }
            .option-title {
                font-size: 0.9rem;
                font-weight: 500;
                color: #e0d8f0;
            }
            .response-box {
                margin-top: 20px;
                padding: 15px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                border: 1px solid rgba(179, 136, 255, 0.2);
                display: none;
                text-align: left;
                color: #e0d8f0;
            }
            @media (max-width: 480px) {
                .options-grid {
                    grid-template-columns: 1fr;
                }
                h1 {
                    font-size: 1.8rem;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Chatbot Studio AI</h1>
            <p>What would you like to create today?</p>
            
            <div class="search-box">
                <textarea id="userInput" placeholder="Describe what you have to build..."></textarea>
                <button class="search-btn" onclick="generateResponse()">Generate</button>
            </div>
            
            <div class="options-grid">
                <div class="option-card" onclick="selectOption('Web Design')">
                    <div class="icon">🌐</div>
                    <div class="option-title">Web Design</div>
                </div>
                <div class="option-card" onclick="selectOption('Video Editor')">
                    <div class="icon">🎬</div>
                    <div class="option-title">Video Editor</div>
                </div>
                <div class="option-card" onclick="selectOption('AI Agent')">
                    <div class="icon">🤖</div>
                    <div class="option-title">AI Agent</div>
                </div>
            </div>

            <div id="responseBox" class="response-box"></div>
        </div>

        <script>
            function generateResponse() {
                const input = document.getElementById('userInput').value;
                const responseBox = document.getElementById('responseBox');
                if(input.trim() === "") {
                    alert("Please write something first!");
                    return;
                }
                responseBox.style.display = "block";
                responseBox.innerHTML = "<strong>AI Response:</strong> Working on creating: " + input;
            }

            function selectOption(optionName) {
                document.getElementById('userInput').value = "Help me build a " + optionName;
            }
        </script>
    </body>
    </html>
    """
    return html_content
    
