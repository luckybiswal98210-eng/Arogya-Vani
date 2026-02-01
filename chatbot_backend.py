#!/usr/bin/env python3
"""
Arogya Vani - Multilingual Health Chatbot Backend
Provides health advice in multiple Indian languages
"""

import unicodedata
from googletrans import Translator
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for web requests

# English response dictionary
RESPONSES_EN = {
    "fever": "Rest well, drink plenty of water or oral rehydration fluids, and consult a doctor if fever is high or lasts more than a few days.",
    "cough": "Try honey with warm water or ginger tea to soothe the throat, and consult a doctor if cough is severe or persistent.",
    "cold": "Rest properly, drink warm fluids like soup or herbal tea, and consider saline nasal spray for congestion.",
    "headache": "Rest in a quiet place, avoid bright lights, stay hydrated, and see a doctor if pain is severe or frequent.",
    "migraine": "Rest in a dark, quiet room, use a cold compress on the forehead, and seek medical care if attacks are frequent.",
    "sinusitis": "Steam inhalation and warm fluids may help relieve pressure; consult a doctor if facial pain or fever occurs.",
    "sore_throat": "Gargle with warm salt water and drink warm fluids like tea or soup; see a doctor if swallowing is painful.",
    "flu": "Get enough rest, drink fluids regularly, and consult a doctor if weakness or fever worsens.",
    "asthma": "Avoid smoke and allergens, use inhalers as prescribed, and seek medical help if breathing becomes difficult.",
    "allergy": "Avoid known triggers, keep surroundings clean, and consult a doctor if symptoms worsen.",
    "bronchitis": "Rest well, drink warm fluids, avoid smoke, and follow doctor-recommended treatment if symptoms persist.",
    "pneumonia": "Seek medical care promptly, rest adequately, and follow professional treatment guidance.",
    "stomach_ache": "Eat light foods, drink water, and consult a doctor if pain is severe or persistent.",
    "indigestion": "Eat smaller meals, avoid spicy food, and drink warm water; see a doctor if discomfort continues.",
    "acidity": "Avoid oily or spicy foods, drink warm water, and consult a doctor if symptoms are frequent.",
    "diarrhea": "Prevent dehydration by drinking oral rehydration solution and water, and avoid greasy foods.",
    "constipation": "Increase fiber intake, drink plenty of water, and stay physically active.",
    "vomiting": "Take small sips of water or ORS and seek medical care if vomiting continues.",
    "nausea": "Rest, avoid strong smells, and sip ginger tea or warm water.",
    "food_poisoning": "Rest, drink ORS and water, and consult a doctor if fever or blood in stool appears.",
    "diabetes": "Monitor blood sugar regularly, follow a healthy diet, and follow your doctor's instructions.",
    "hypertension": "Reduce salt intake, exercise regularly, manage stress, and follow medical advice.",
    "low_blood_pressure": "Drink fluids, rise slowly from sitting, and consult a doctor if dizziness occurs.",
    "chest_pain": "Rest immediately and seek urgent medical care, especially if pain is severe or spreading.",
    "back_pain": "Rest the back, maintain good posture, apply heat if helpful, and consult a doctor if pain persists.",
    "neck_pain": "Avoid strain, do gentle stretches, and use a warm compress if needed.",
    "joint_pain": "Rest affected joints, do gentle movement, and consult a doctor if swelling occurs.",
    "arthritis": "Keep joints active with gentle exercise and follow medical guidance for pain management.",
    "muscle_pain": "Rest the muscle, apply warm compress, and hydrate well.",
    "leg_cramps": "Stretch gently and drink enough water throughout the day.",
    "fatigue": "Ensure adequate sleep, eat balanced meals, and stay hydrated.",
    "dehydration": "Drink water, oral rehydration solution, or coconut water and seek care if symptoms worsen.",
    "dizziness": "Sit or lie down safely, drink fluids, and consult a doctor if fainting occurs.",
    "anxiety": "Practice deep breathing and relaxation techniques, and seek professional help if anxiety interferes with daily life.",
    "depression": "Seek mental health support, talk to a trusted person, and consult a professional for proper care.",
    "stress": "Take breaks, practice relaxation techniques, and maintain a balanced routine.",
    "insomnia": "Maintain a regular sleep schedule, reduce screen time at night, and seek help if sleeplessness continues.",
    "skin_rash": "Keep the area clean and dry, avoid irritants, and consult a doctor if rash spreads.",
    "itching": "Avoid scratching, apply soothing lotion, and seek care if itching is severe.",
    "fungal_infection": "Keep the area dry and clean, and consult a doctor if infection spreads.",
    "ear_pain": "Avoid water entry into the ear and consult a doctor if pain or discharge occurs.",
    "eye_strain": "Rest your eyes, reduce screen time, and use proper lighting.",
    "eye_fatigue": "Rest eyes regularly, reduce screen exposure, and use proper lighting.",
    "ear_blockage": "Avoid inserting objects into the ear, try swallowing or yawning, and consult a doctor if hearing loss occurs.",
    "toothache": "Rinse the mouth with warm salt water, avoid hard foods, and see a dentist if pain persists.",
    "mouth_ulcer": "Avoid spicy foods, rinse with salt water, and consult a doctor if ulcers last more than two weeks.",
    "bad_breath": "Maintain oral hygiene, drink water frequently, and consult a dentist if the problem continues.",
    "dry_mouth": "Sip water often and consult a doctor if dryness is persistent.",
    "bleeding_gums": "Brush gently, floss carefully, and see a dentist if bleeding is frequent.",
    "acne": "Clean skin gently, avoid squeezing pimples, and consult a doctor if acne is severe.",
    "boils": "Keep the area clean and dry, and consult a doctor if fever or pain increases.",
    "dry_skin": "Use moisturizer regularly, avoid hot showers, and drink enough water.",
    "dandruff": "Wash hair regularly with mild shampoo and consult a doctor if scalp irritation occurs.",
    "hair_fall": "Reduce stress, eat nutritious food, and consult a doctor if hair loss is sudden.",
    "urinary_burning": "Drink plenty of water and consult a doctor if pain or fever develops.",
    "menstrual_cramps": "Rest, apply a warm heating pad, and consult a doctor if pain is severe.",
    "night_sweats": "Keep the room cool and consult a doctor if sweating is frequent.",
    "palpitations": "Sit calmly, breathe slowly, and seek urgent care if chest pain occurs.",
    "cold_hands": "Warm hands gradually and consult a doctor if color changes occur.",
    "cold_feet": "Keep feet warm and seek medical advice if numbness develops.",
    "muscle_soreness": "Rest the muscles, hydrate well, and use gentle stretching.",
    "sun_fatigue": "Move to a cool place, rest, and drink water or oral rehydration fluids.",
    "travel_fatigue": "Get adequate rest, hydrate well, and eat light meals.",
    "jet_lag": "Adjust sleep schedule gradually and get natural sunlight during the day.",
    "memory_lapse": "Rest well, reduce stress, and consult a doctor if confusion increases.",
    "concentration_difficulty": "Take short breaks, stay hydrated, and ensure proper sleep.",
    "mental_exhaustion": "Reduce workload, rest adequately, and seek professional help if burnout persists.",
    "mood_swings": "Maintain a regular routine and consult a professional if mood changes are severe.",
    "panic_symptoms": "Sit calmly, focus on slow breathing, and seek urgent care if chest pain occurs.",
    "general_discomfort": "Rest, hydrate, and consult a doctor if symptoms worsen."
}

# Multilingual input keywords mapped to responses
INPUT_KEYWORDS = {
    'hi': {  # Hindi
        "बुखार": "fever", "ताप": "fever", "fever": "fever",
        "खांसी": "cough", "खाँसी": "cough", "cough": "cough",
        "सर्दी": "cold", "जुकाम": "cold", "cold": "cold",
        "सिरदर्द": "headache", "सिर दर्द": "headache", "headache": "headache",
        "माइग्रेन": "migraine", "migraine": "migraine",
        "साइनस": "sinusitis", "sinusitis": "sinusitis",
        "गला खराब": "sore_throat", "गले में दर्द": "sore_throat", "sore throat": "sore_throat",
        "फ्लू": "flu", "flu": "flu",
        "दमा": "asthma", "asthma": "asthma",
        "एलर्जी": "allergy", "allergy": "allergy",
        "पेट दर्द": "stomach_ache", "stomach ache": "stomach_ache", "stomach pain": "stomach_ache",
        "अपच": "indigestion", "indigestion": "indigestion",
        "एसिडिटी": "acidity", "acidity": "acidity",
        "दस्त": "diarrhea", "loose motion": "diarrhea", "diarrhea": "diarrhea",
        "कब्ज": "constipation", "constipation": "constipation",
        "उल्टी": "vomiting", "vomiting": "vomiting",
        "मतली": "nausea", "nausea": "nausea",
        "मधुमेह": "diabetes", "diabetes": "diabetes", "sugar": "diabetes",
        "उच्च रक्तचाप": "hypertension", "high bp": "hypertension", "hypertension": "hypertension",
        "चक्कर": "dizziness", "dizziness": "dizziness",
        "थकान": "fatigue", "fatigue": "fatigue", "weakness": "fatigue",
        "तनाव": "stress", "stress": "stress",
        "चिंता": "anxiety", "anxiety": "anxiety",
        "अवसाद": "depression", "depression": "depression",
        "नींद न आना": "insomnia", "insomnia": "insomnia",
        "त्वचा पर दाने": "skin_rash", "skin rash": "skin_rash", "rash": "skin_rash",
        "खुजली": "itching", "itching": "itching",
        "दांत दर्द": "toothache", "toothache": "toothache",
        "मुंह के छाले": "mouth_ulcer", "mouth ulcer": "mouth_ulcer",
        "बाल झड़ना": "hair_fall", "hair fall": "hair_fall",
        "पीरियड्स में दर्द": "menstrual_cramps", "period pain": "menstrual_cramps",
    },
    'mr': {  # Marathi
        "ताप": "fever", "fever": "fever",
        "खोकला": "cough", "cough": "cough",
        "सर्दी": "cold", "cold": "cold",
        "डोकेदुखी": "headache", "headache": "headache",
        "पोटदुखी": "stomach_ache", "stomach ache": "stomach_ache",
        "जुलाब": "diarrhea", "diarrhea": "diarrhea",
        "बद्धकोष्ठता": "constipation", "constipation": "constipation",
        "मधुमेह": "diabetes", "diabetes": "diabetes",
        "रक्तदाब": "hypertension", "hypertension": "hypertension",
        "चक्कर": "dizziness", "dizziness": "dizziness",
        "थकवा": "fatigue", "fatigue": "fatigue",
    },
    'ta': {  # Tamil
        "காய்ச்சல்": "fever", "fever": "fever",
        "இருமல்": "cough", "cough": "cough",
        "சளி": "cold", "cold": "cold",
        "தலைவலி": "headache", "headache": "headache",
        "வயிற்றுவலி": "stomach_ache", "stomach ache": "stomach_ache",
        "வயிற்றுப்போக்கு": "diarrhea", "diarrhea": "diarrhea",
        "மலச்சிக்கல்": "constipation", "constipation": "constipation",
        "நீரிழிவு": "diabetes", "diabetes": "diabetes",
        "உயர் இரத்த அழுத்தம்": "hypertension", "hypertension": "hypertension",
        "தலைசுற்றல்": "dizziness", "dizziness": "dizziness",
        "சோர்வு": "fatigue", "fatigue": "fatigue",
    },
    'bn': {  # Bengali
        "জ্বর": "fever", "fever": "fever",
        "কাশি": "cough", "cough": "cough",
        "সর্দি": "cold", "cold": "cold",
        "মাথাব্যথা": "headache", "headache": "headache",
        "পেটব্যথা": "stomach_ache", "stomach ache": "stomach_ache",
        "ডায়রিয়া": "diarrhea", "diarrhea": "diarrhea",
        "কোষ্ঠকাঠিন্য": "constipation", "constipation": "constipation",
        "ডায়াবেটিস": "diabetes", "diabetes": "diabetes",
        "উচ্চ রক্তচাপ": "hypertension", "hypertension": "hypertension",
        "মাথা ঘোরা": "dizziness", "dizziness": "dizziness",
        "ক্লান্তি": "fatigue", "fatigue": "fatigue",
    },
    'te': {  # Telugu
        "జ్వరం": "fever", "fever": "fever",
        "దగ్గు": "cough", "cough": "cough",
        "జలుబు": "cold", "cold": "cold",
        "తలనొప్పి": "headache", "headache": "headache",
        "కడుపునొప్పి": "stomach_ache", "stomach ache": "stomach_ache",
        "విరేచనాలు": "diarrhea", "diarrhea": "diarrhea",
        "మలబద్ధకం": "constipation", "constipation": "constipation",
        "మధుమేహం": "diabetes", "diabetes": "diabetes",
        "రక్తపోటు": "hypertension", "hypertension": "hypertension",
        "తలతిరగడం": "dizziness", "dizziness": "dizziness",
        "అలసట": "fatigue", "fatigue": "fatigue",
    },
    'kn': {  # Kannada
        "ಜ್ವರ": "fever", "fever": "fever",
        "ಕೆಮ್ಮು": "cough", "cough": "cough",
        "ಶೀತ": "cold", "cold": "cold",
        "ತಲೆನೋವು": "headache", "headache": "headache",
        "ಹೊಟ್ಟೆ ನೋವು": "stomach_ache", "stomach ache": "stomach_ache",
        "ಅತಿಸಾರ": "diarrhea", "diarrhea": "diarrhea",
        "ಮಲಬದ್ಧತೆ": "constipation", "constipation": "constipation",
        "ಮಧುಮೇಹ": "diabetes", "diabetes": "diabetes",
        "ಅಧಿಕ ರಕ್ತದೊತ್ತಡ": "hypertension", "hypertension": "hypertension",
        "ತಲೆತಿರುಗುವಿಕೆ": "dizziness", "dizziness": "dizziness",
        "ಆಯಾಸ": "fatigue", "fatigue": "fatigue",
    },
    'gu': {  # Gujarati
        "તાવ": "fever", "fever": "fever",
        "ઉધરસ": "cough", "cough": "cough",
        "શરદી": "cold", "cold": "cold",
        "માથાનો દુખાવો": "headache", "headache": "headache",
        "પેટનો દુખાવો": "stomach_ache", "stomach ache": "stomach_ache",
        "ઝાડા": "diarrhea", "diarrhea": "diarrhea",
        "કબજિયાત": "constipation", "constipation": "constipation",
        "ડાયાબિટીસ": "diabetes", "diabetes": "diabetes",
        "હાઈ બીપી": "hypertension", "hypertension": "hypertension",
        "ચક્કર": "dizziness", "dizziness": "dizziness",
        "થાક": "fatigue", "fatigue": "fatigue",
    }
}

# Multilingual responses
MULTILINGUAL_RESPONSES = {
    'hi': {
        "fever": "अच्छी तरह आराम करें, पानी या ओआरएस जैसे तरल पदार्थ पिएँ, और बुखार ज़्यादा हो या कुछ दिनों तक रहे तो डॉक्टर से मिलें।",
        "cough": "गुनगुने पानी में शहद या अदरक की चाय लें; खाँसी ज़्यादा हो या लंबे समय तक रहे तो डॉक्टर से मिलें।",
        "cold": "पूरा आराम करें, सूप या हर्बल चाय जैसे गर्म तरल पिएँ, और नाक बंद हो तो सलाइन स्प्रे का उपयोग करें।",
        "headache": "शांत जगह पर आराम करें, तेज रोशनी से बचें, पानी पिएँ, और दर्द ज़्यादा या बार-बार हो तो डॉक्टर से मिलें।",
        "stomach_ache": "हल्का भोजन करें, पानी पिएँ, और दर्द ज़्यादा या लंबे समय तक रहे तो डॉक्टर से मिलें।",
        "diarrhea": "ओआरएस और पानी पिएँ, तला-भुना न खाएँ, और स्थिति बिगड़े तो डॉक्टर से मिलें।",
        "constipation": "फाइबर युक्त भोजन करें, ज़्यादा पानी पिएँ, और हल्की गतिविधि रखें।",
        "diabetes": "ब्लड शुगर नियमित जाँचें, संतुलित आहार लें, और डॉक्टर की सलाह का पालन करें।",
        "hypertension": "नमक कम लें, नियमित व्यायाम करें, तनाव कम करें, और डॉक्टर की सलाह मानें।",
        "fatigue": "पर्याप्त नींद लें, संतुलित आहार करें, और पानी पिएँ।",
        "stress": "ब्रेक लें, ध्यान/योग करें, और संतुलित दिनचर्या रखें।",
        "anxiety": "गहरी साँस लें, रिलैक्सेशन अपनाएँ, और रोज़मर्रा प्रभावित हो तो मदद लें।",
        "general_discomfort": "आराम करें, पानी पिएँ, और लक्षण बढ़ें तो डॉक्टर से मिलें।"
    },
    'mr': {
        "fever": "पुरेसा आराम करा, पाणी किंवा ओआरएससारखे द्रव प्या, आणि ताप जास्त असेल किंवा काही दिवस टिकला तर डॉक्टरांना भेटा.",
        "cough": "खोकल्यासाठी कोमट पाण्यात मध किंवा आलेाची चहा घ्या; खोकला जास्त किंवा दीर्घकाळ राहिल्यास डॉक्टरांना भेटा.",
        "cold": "पूर्ण विश्रांती घ्या, सूप किंवा हर्बल चहासारखे गरम द्रव प्या, आणि नाक बंद असल्यास सलाईन स्प्रे वापरा.",
        "headache": "शांत ठिकाणी आराम करा, तेज प्रकाश टाळा, पाणी प्या, आणि डोकेदुखी जास्त किंवा वारंवार होत असल्यास डॉक्टरांना भेटा.",
        "stomach_ache": "हलका आहार घ्या, पाणी प्या, आणि वेदना जास्त किंवा दीर्घकाळ राहिल्यास डॉक्टरांना भेटा.",
        "general_discomfort": "विश्रांती घ्या, पाणी प्या, आणि लक्षणे वाढल्यास डॉक्टरांना भेटा."
    },
    'ta': {
        "fever": "நன்றாக ஓய்வு எடுக்கவும், தண்ணீர் அல்லது ORS போன்ற திரவங்களை குடிக்கவும், காய்ச்சல் அதிகமாக இருந்தால் அல்லது சில நாட்கள் நீடித்தால் மருத்துவரை அணுகவும்.",
        "cough": "இருமலுக்கு வெதுவெதுப்பான நீரில் தேன் அல்லது இஞ்சி தேநீர் குடிக்கலாம்; இருமல் அதிகமாக இருந்தால் மருத்துவரை அணுகவும்.",
        "cold": "முழுமையாக ஓய்வு எடுக்கவும், சூப் அல்லது மூலிகை தேநீர் போன்ற சூடான திரவங்களை குடிக்கவும், மூக்கு அடைப்பு இருந்தால் சாலைன் ஸ்ப்ரே பயன்படுத்தலாம்.",
        "headache": "அமைதியான இடத்தில் ஓய்வு எடுக்கவும், பிரகாசமான ஒளியை தவிர்க்கவும், தண்ணீர் குடிக்கவும்; தலைவலி அதிகமாக இருந்தால் மருத்துவரை அணுகவும்.",
        "stomach_ache": "லேசான உணவு எடுத்துக்கொள்ளவும், தண்ணீர் குடிக்கவும், வயிற்றுவலி அதிகமாக இருந்தால் மருத்துவரை அணுகவும்.",
        "general_discomfort": "ஓய்வு எடுக்கவும், தண்ணீர் குடிக்கவும்."
    },
    'bn': {
        "fever": "পর্যাপ্ত বিশ্রাম নিন, পানি বা ORS পান করুন, জ্বর বেশি হলে বা কয়েকদিন থাকলে ডাক্তারের পরামর্শ নিন।",
        "cough": "কাশির জন্য কুসুম গরম পানিতে মধু বা আদা চা পান করুন; বেশি হলে ডাক্তারের পরামর্শ নিন।",
        "cold": "বিশ্রাম নিন, স্যুপ বা গরম তরল পান করুন, নাক বন্ধ হলে স্যালাইন স্প্রে ব্যবহার করুন।",
        "headache": "শান্ত জায়গায় বিশ্রাম নিন, উজ্জ্বল আলো এড়িয়ে চলুন, পানি পান করুন।",
        "stomach_ache": "হালকা খাবার খান, পানি পান করুন।",
        "general_discomfort": "বিশ্রাম নিন ও পানি পান করুন।"
    },
    'te': {
        "fever": "సరైన విశ్రాంతి తీసుకోండి, నీరు లేదా ORS వంటి ద్రవాలు తాగండి, జ్వరం ఎక్కువగా లేదా కొన్ని రోజులు కొనసాగితే డాక్టర్ను సంప్రదించండి.",
        "cough": "దగ్గుకు గోరువెచ్చని నీటిలో తేనె లేదా అల్లం టీ తాగవచ్చు; దగ్గు ఎక్కువగా ఉంటే డాక్టర్ను సంప్రదించండి.",
        "cold": "పూర్తిగా విశ్రాంతి తీసుకోండి, సూప్ లేదా హెర్బల్ టీ వంటి వేడి ద్రవాలు తాగండి, ముక్కు బ్లాక్ అయితే సాలైన్ స్ప్రే ఉపయోగించండి.",
        "headache": "నిశ్శబ్దమైన చోట విశ్రాంతి తీసుకోండి, ప్రకాశవంతమైన వెలుతురు తప్పించండి, నీరు తాగండి; తలనొప్పి ఎక్కువగా ఉంటే డాక్టర్ను సంప్రదించండి.",
        "stomach_ache": "తేలికపాటి ఆహారం తినండి, నీరు తాగండి, కడుపునొప్పి ఎక్కువగా ఉంటే డాక్టర్ను సంప్రదించండి.",
        "general_discomfort": "విశ్రాంతి తీసుకోండి, నీరు తాగండి."
    },
    'kn': {
        "fever": "ಸಾಕಷ್ಟು ವಿಶ್ರಾಂತಿ ಪಡೆಯಿರಿ, ನೀರು ಅಥವಾ ORS ಹೀಗೆ ದ್ರವಗಳನ್ನು ಕುಡಿಯಿರಿ, ಜ್ವರ ಹೆಚ್ಚು ಇದ್ದರೆ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        "cough": "ಕೆಮ್ಮಿಗೆ ಬಿಸಿ ನೀರಲ್ಲಿ ಜೇನು ಅಥವಾ ಶುಂಠಿ ಚಹಾ ಕುಡಿಯಿರಿ; ಹೆಚ್ಚಾದರೆ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        "cold": "ಪೂರ್ಣ ವಿಶ್ರಾಂತಿ ಪಡೆಯಿರಿ, ಸೂಪ್ ಅಥವಾ ಬಿಸಿ ಪಾನೀಯ ಕುಡಿಯಿರಿ, ಮೂಗು ಮುಚ್ಚಿದರೆ ಸಾಲೈನ್ ಸ್ಪ್ರೇ ಬಳಸಿ.",
        "headache": "ಶಾಂತ ಸ್ಥಳದಲ್ಲಿ ವಿಶ್ರಾಂತಿ ಪಡೆಯಿರಿ, ತೀಕ್ಷ್ಣ ಬೆಳಕು ತಪ್ಪಿಸಿ, ನೀರು ಕುಡಿಯಿರಿ.",
        "stomach_ache": "ಹಗುರ ಆಹಾರ ಸೇವಿಸಿ ಮತ್ತು ನೀರು ಕುಡಿಯಿರಿ.",
        "general_discomfort": "ವಿಶ್ರಾಂತಿ ಪಡೆದು ನೀರು ಕುಡಿಯಿರಿ."
    },
    'gu': {
        "fever": "પૂરતો આરામ કરો, પાણી અથવા ORS જેવા પ્રવાહી પીવો; તાવ વધારે હોય તો ડૉક્ટરને સંપર્ક કરો.",
        "cough": "ગરમ પાણીમાં મધ અથવા આદુની ચા પીવો; વધારે થાય તો ડૉક્ટરને સંપર્ક કરો.",
        "cold": "સંપૂર્ણ આરામ લો, સૂપ અથવા ગરમ પ્રવાહી પીવો, નાક બંધ હોય તો સેલાઇન સ્પ્રે વાપરો.",
        "headache": "શાંત જગ્યાએ આરામ કરો, તેજ પ્રકાશથી બચો અને પાણી પીવો.",
        "stomach_ache": "હલકો ખોરાક લો અને પાણી પીવો.",
        "general_discomfort": "આરામ કરો અને પાણી પીવો."
    }
}


def normalize_text(text):
    """Normalize text for better matching"""
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text)
    return text


def detect_language(text):
    """Detect language from text"""
    # Check for language-specific characters
    if any('\u0900' <= char <= '\u097F' for char in text):
        return 'hi'  # Hindi
    elif any('\u0980' <= char <= '\u09FF' for char in text):
        return 'bn'  # Bengali
    elif any('\u0B80' <= char <= '\u0BFF' for char in text):
        return 'ta'  # Tamil
    elif any('\u0C00' <= char <= '\u0C7F' for char in text):
        return 'te'  # Telugu
    elif any('\u0C80' <= char <= '\u0CFF' for char in text):
        return 'kn'  # Kannada
    elif any('\u0A80' <= char <= '\u0AFF' for char in text):
        return 'gu'  # Gujarati
    elif any('\u0900' <= char <= '\u097F' for char in text):
        return 'mr'  # Marathi (overlaps with Hindi range, needs better detection)
    else:
        return 'en'  # Default to English


def find_symptom(user_input, language='en'):
    """Find matching symptom from user input"""
    normalized_input = normalize_text(user_input)
    
    # Try exact match first
    if language in INPUT_KEYWORDS:
        for keyword, symptom in INPUT_KEYWORDS[language].items():
            if normalize_text(keyword) in normalized_input:
                return symptom
    
    # Try English keywords
    for keyword, symptom in INPUT_KEYWORDS.get('hi', {}).items():
        if normalize_text(keyword) in normalized_input:
            return symptom
    
    # Fuzzy match with English symptoms
    for symptom in RESPONSES_EN.keys():
        if symptom.replace('_', ' ') in normalized_input or symptom in normalized_input:
            return symptom
    
    return None


def get_response(symptom, language='en'):
    """Get response for symptom in specified language"""
    if language == 'en' or language not in MULTILINGUAL_RESPONSES:
        return RESPONSES_EN.get(symptom, RESPONSES_EN.get('general_discomfort'))
    
    # Get response in requested language, fallback to English
    lang_responses = MULTILINGUAL_RESPONSES.get(language, {})
    return lang_responses.get(symptom, RESPONSES_EN.get(symptom, RESPONSES_EN.get('general_discomfort')))


@app.route('/chat', methods=['POST'])
def chat():
    """Main chatbot endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        preferred_language = data.get('language', 'auto')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Detect language if auto
        if preferred_language == 'auto':
            detected_lang = detect_language(user_message)
        else:
            detected_lang = preferred_language
        
        # Find symptom
        symptom = find_symptom(user_message, detected_lang)
        
        if symptom:
            response_text = get_response(symptom, detected_lang)
            return jsonify({
                'response': response_text,
                'symptom': symptom,
                'language': detected_lang,
                'status': 'success'
            })
        else:
            return jsonify({
                'response': get_response('general_discomfort', detected_lang),
                'symptom': 'unknown',
                'language': detected_lang,
                'status': 'no_match',
                'suggestion': 'Please describe your symptoms more clearly or consult a doctor.'
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Arogya Vani Chatbot',
        'supported_languages': list(INPUT_KEYWORDS.keys()),
        'total_symptoms': len(RESPONSES_EN)
    })


@app.route('/symptoms', methods=['GET'])
def list_symptoms():
    """List all available symptoms"""
    return jsonify({
        'symptoms': list(RESPONSES_EN.keys()),
        'count': len(RESPONSES_EN)
    })


if __name__ == '__main__':
    print("🏥 Arogya Vani Chatbot Backend Starting...")
    print(f"📊 Loaded {len(RESPONSES_EN)} symptoms")
    print(f"🌐 Supporting {len(INPUT_KEYWORDS)} languages")
    app.run(host='0.0.0.0', port=5000, debug=True)
