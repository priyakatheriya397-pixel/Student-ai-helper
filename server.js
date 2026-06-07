const express = require('express');
const path = require('path');
const app = express();

// यह लाइन आपके index.html वाले फोल्डर को सर्व करेगी
app.use(express.static(path.join(__dirname, 'public'))); 

// जब कोई आपकी वेबसाइट खोलेगा, तो उसे नया index.html दिखेगा
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
