import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openai import OpenAI

MY_FREE_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai",
    api_key=MY_FREE_KEY,
)

app = FastAPI()

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
        button { background-color: #3498db; color: white; border: none; padding: 12px 25px; font-size: 16px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; }
        #responseBox { margin-top: 20px; text-align: left; background: #eef2f3; padding: 15px; border-radius: 6px; display: none; font-size: 15px; line-height: 1.5; color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Smart Student Helper AI</h1>
        <p>Aditya Kumar jaisa aapka apna AI Tutor! Apni book ka sawaal niche likhein:</p>
        <input type="text" id="userQuery" placeholder="e.g., Python mein Variables kya hain?">
        <button onclick="askAI()">Teacher Se Poochein ✨</button>
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
                let data = await res.text();
                box.innerHTML = "<b>📚 Teacher Ka Jawaab:</b><br><br>" + data.replace(/\\\\n/g, '<br>');
            } catch(e) { box.innerHTML = "Error aa gaya bhai: " + e; }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root(): return html_content

@app.get("/ask")
def ask_ai_endpoint(q: str):
    try:
        response = client.chat.completions.create(
            model="google/gemma-2-9b-it:free",
            messages=[
                {"role": "system", "content": "Aap ek expert school teacher hain. Har jawaab simple Hindi mein dein. Step-by-step samjhayein."},
                {"role": "user", "content": q}
            ]
        )
        return response.choices.message.content
    except Exception as e: return f"Error: {e}"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
  
