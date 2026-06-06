import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# HTML Template (Frontend UI)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student AI Tutor - Premium</title>
    <style>
        body { font-family: 'Arial', sans-serif; background: #f4f7f6; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 500px; background: white; margin: 50px auto; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        p { color: #666; font-size: 16px; }
        .price-badge { font-size: 32px; font-weight: bold; color: #2ecc71; margin: 20px 0; }
        .btn-premium { background: #ff4757; color: white; border: none; padding: 15px 30px; font-size: 18px; font-weight: bold; border-radius: 8px; cursor: pointer; transition: 0.3s; width: 100%; }
        .btn-premium:hover { background: #e84118; transform: translateY(-2px); }
        .features { text-align: left; margin: 20px 0; padding-left: 20px; }
        .features li { margin: 10px 0; color: #444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 Student AI Tutor</h1>
        <p>Unlock All Advanced Features & Solutions</p>
        
        <div class="price-badge">₹200 <span style="font-size: 16px; color:#888;">/ monthly</span></div>
        
        <ul class="features">
            <li>✅ Unlimited AI Questions & Answers</li>
            <li>✅ Instant Homework Explanations</li>
            <li>✅ 24/7 Premium Server Speed</li>
            <li>✅ No Ads / No Interruptions</li>
        </ul>

        <!-- Premium Buy Button -->
        <button class="btn-premium" onclick="payNow()">Buy Premium Membership</button>
    </div>

    <!-- Razorpay Payment Integration -->
    <script src="https://razorpay.com"></script>
    <script>
        function payNow() {
            var options = {
                "key": "rzp_test_YOUR_KEY_HERE", // Replace with your Razorpay Key
                "amount": 20000, // 200 INR in paise
                "currency": "INR",
                "name": "Student AI Tutor",
                "description": "Premium Activation",
                "handler": function (response){
                    alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
                    // Add backend logic here to unlock features
                },
                "prefill": {
                    "name": "Student",
                    "email": "student@example.com"
                },
                "theme": {
                    "color": "#ff4757"
                }
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
    # 🟢 Render पर 100% सफल होने के लिए Dynamic Port और Host 0.0.0.0 ज़रूरी है
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
