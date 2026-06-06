from flask import Flask, send_from_directory, jsonify, request, abort
import os
import sys

# 1. फ्लैस्क ऐप और स्टैटिक फाइल्स कॉन्फ़िगरेशन
app = Flask(__name__, static_folder='.', static_url_path='')

# रेंडर का एनवायरनमेंट पोर्ट (या लोकल टेस्टिंग के लिए 3000)
PORT = int(os.environ.get('PORT', 3000))

# 2. मुख्य होमपेज रूट (यह आपकी index.html को लोड करेगा)
@app.route('/')
def home():
    try:
        # जांचें कि क्या index.html फ़ाइल उसी फ़ोल्डर में मौजूद है
        if not os.path.exists('index.html'):
            print("[ERROR] index.html file not found in the root directory!", file=sys.stderr)
            return "<h1>Error: index.html missing!</h1><p>Please upload your frontend design file.</p>", 404
            
        print("[SUCCESS] Serving index.html to the user.")
        return send_from_directory('.', 'index.html')
    except Exception as e:
        print(f"[CRITICAL] Failed to serve home page: {str(e)}", file=sys.stderr)
        return jsonify({"success": False, "error": "Internal Server Error"}), 500

# 3. एआई ट्यूटर/होमवर्क सबमिशन के लिए एक मजबूत API एंडपॉइंट
@app.route('/api/ask', methods=['POST'])
def ask_ai():
    try:
        # यूजर से आने वाले JSON डेटा को सुरक्षित रूप से पढ़ें
        data = request.get_json(silent=True) or {}
        question = data.get('question', '')
        tool = data.get('tool', 'General')
        
        # इनपुट वैलिडेशन (खाली सवाल रोकने के लिए)
        if not question or question.strip() == "":
            return jsonify({
                "success": False, 
                "message": "Question cannot be empty! Please type something."
            }), 400
            
        # सर्वर लॉग्स में डेटा प्रिंट करें (रेंडर डैशबोर्ड पर दिखेगा)
        print(f"[AI REQUEST] Tool Selected: {tool} | Question Submitted: {question}")
        
        # अभी के लिए एक सफल रिस्पॉन्स भेजें (बाद में यहाँ असली AI API जोड़ सकते हैं)
        return jsonify({
            "success": True,
            "message": f"Your question about '{tool}' has been received successfully by the Python server!"
        }), 200

    except Exception as e:
        print(f"[API ERROR] Something went wrong in /api/ask: {str(e)}", file=sys.stderr)
        return jsonify({"success": False, "message": "An error occurred on the server."}), 500

# 4. 404 क्रैश प्रोटेक्शन (अगर कोई गलत यूआरएल डाले तो सर्वर बंद होने के बजाय होमपेज पर भेज दे)
@app.errorhandler(404)
def page_not_found(e):
    print(f"[404 WARNING] User tried to access an invalid URL: {request.url}")
    return send_from_directory('.', 'index.html')

# 5. ग्लोबल एरर हैंडलर (किसी भी अचानक आई खराबी से सर्वर को बचाने के लिए)
@app.errorhandler(500)
def internal_server_error(e):
    print(f"[500 CRITICAL] Global Server Error: {str(e)}", file=sys.stderr)
    return jsonify({"success": False, "message": "Global Server Error Caught Safely!"}), 500

# 6. सर्वर को रेंडर नेटवर्क पर शुरू करने का मुख्य ब्लॉक
if __name__ == '__main__':
    print("====================================================")
    print("🚀 PYTHON FLASK SECURE SERVER INITIALIZING...")
    print(f"📡 Binding to Host: 0.0.0.0 | Port: {PORT}")
    print("====================================================")
    
    # host='0.0.0.0' रेंडर नेटवर्क के लिए अनिवार्य है [¹]
    app.run(host='0.0.0.0', port=PORT, debug=False)
    
