# 🏥 Arogya Vani Chatbot Backend

## Overview
Multilingual health chatbot backend providing medical advice in 8 Indian languages.

## Features
- ✅ **60+ Health Conditions** covered
- 🌐 **8 Languages Supported**: English, Hindi, Marathi, Tamil, Bengali, Telugu, Kannada, Gujarati
- 🔍 **Auto Language Detection**
- 🚀 **REST API** for easy integration
- 💊 **Evidence-based health advice**

## Installation

### 1. Install Dependencies
```bash
pip install -r chatbot_requirements.txt
```

### 2. Run the Server
```bash
python chatbot_backend.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### 1. Chat Endpoint
**POST** `/chat`

Request:
```json
{
  "message": "मुझे बुखार है",
  "language": "auto"
}
```

Response:
```json
{
  "response": "अच्छी तरह आराम करें, पानी या ओआरएस जैसे तरल पदार्थ पिएँ...",
  "symptom": "fever",
  "language": "hi",
  "status": "success"
}
```

### 2. Health Check
**GET** `/health`

Response:
```json
{
  "status": "healthy",
  "service": "Arogya Vani Chatbot",
  "supported_languages": ["hi", "mr", "ta", "bn", "te", "kn", "gu"],
  "total_symptoms": 60
}
```

### 3. List Symptoms
**GET** `/symptoms`

Returns all available symptoms the chatbot can handle.

## Supported Symptoms

### Common Conditions
- Fever, Cough, Cold, Headache, Migraine
- Stomach ache, Indigestion, Acidity, Diarrhea, Constipation
- Diabetes, Hypertension, Asthma, Allergy

### Mental Health
- Anxiety, Depression, Stress, Insomnia

### Pain & Discomfort
- Back pain, Neck pain, Joint pain, Muscle pain
- Toothache, Ear pain, Eye strain

### Skin Conditions
- Rash, Itching, Acne, Dry skin, Dandruff

### And 40+ more conditions!

## Integration with Frontend

### JavaScript Example
```javascript
async function getChatResponse(message) {
  const response = await fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      language: 'auto'
    })
  });
  
  const data = await response.json();
  return data.response;
}
```

### HTML Integration
```html
<script>
  async function askChatbot() {
    const userInput = document.getElementById('userInput').value;
    const response = await getChatResponse(userInput);
    document.getElementById('chatResponse').innerText = response;
  }
</script>
```

## Language Codes
- `en` - English
- `hi` - Hindi (हिंदी)
- `mr` - Marathi (मराठी)
- `ta` - Tamil (தமிழ்)
- `bn` - Bengali (বাংলা)
- `te` - Telugu (తెలుగు)
- `kn` - Kannada (ಕನ್ನಡ)
- `gu` - Gujarati (ગુજરાતી)
- `auto` - Auto-detect

## Deployment

### Local Development
```bash
python chatbot_backend.py
```

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 chatbot_backend:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY chatbot_requirements.txt .
RUN pip install -r chatbot_requirements.txt
COPY chatbot_backend.py .
CMD ["python", "chatbot_backend.py"]
```

## Important Notes

⚠️ **Medical Disclaimer**: This chatbot provides general health information only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## Future Enhancements
- [ ] Add more symptoms and conditions
- [ ] Integrate with medical databases
- [ ] Add voice input/output
- [ ] Implement conversation history
- [ ] Add symptom severity assessment
- [ ] Integration with appointment booking

## Support
For issues or questions, please contact the development team.

---
**Arogya Vani** - Your Health Companion 🏥
