// यूजर का सवाल भेजने वाला मजबूत फंक्शन
function sendMessageToAI(userText) {
    // बैकएंड के /chat रूट पर डेटा भेजना
    fetch('/chat', {
        method: 'POST', // यहाँ POST होना ही सबसे ज़रूरी है
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userText }) // यूजर का सवाल भेजा
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('नेटवर्क या सर्वर में कोई समस्या है।');
        }
        return response.json();
    })
    .then(data => {
        if (data.response) {
            // चैट स्क्रीन पर AI का सही जवाब दिखाएँ
            displayBotResponse(data.response); 
        } else if (data.error) {
            displayBotResponse("त्रुटि: " + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        displayBotResponse("तकनीकी खराबी: सर्वर से जवाब नहीं मिल पाया।");
    });
}

// यह सिर्फ एक उदाहरण फंक्शन है जो स्क्रीन पर जवाब दिखाएगा (इसे अपने हिसाब से बदल सकते हैं)
function displayBotResponse(responseText) {
    console.log("AI का सही जवाब:", responseText);
    // यहाँ अपना वो कोड डालें जो चैट स्क्रीन के बॉक्स में टेक्स्ट दिखाता है
}
