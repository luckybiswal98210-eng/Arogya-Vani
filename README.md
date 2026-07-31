# 🏥 Arogya Vani - AI-Powered Multilingual Health Assistant

<div align="center">

![Arogya Vani](https://img.shields.io/badge/Health-Assistant-blue)
![Firebase](https://img.shields.io/badge/Firebase-Hosting-orange)
![Languages](https://img.shields.io/badge/Languages-8-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Your AI Health Companion - Voice & Text Support in 8 Indian Languages**

[Live Demo](https://arogya-vani-2c4fb.web.app) | [Report Bug](https://github.com/luckybiswal98210-eng/Arogya-Vani/issues) | [Request Feature](https://github.com/luckybiswal98210-eng/Arogya-Vani/issues)

</div>

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 About

**Arogya Vani** is an intelligent, multilingual health assistant web application designed to provide health advice and symptom analysis in multiple Indian languages. The platform features voice input/output capabilities, making healthcare information accessible to users regardless of their language or literacy level.

### Why Arogya Vani?

- 🌍 **Multilingual Support**: Communicate in 8 Indian languages
- 🎤 **Voice Enabled**: Speak your symptoms, listen to advice
- 🤖 **AI-Powered**: Smart symptom matching and health recommendations
- 📱 **Responsive Design**: Works on all devices
- 🔐 **Secure**: Firebase Authentication & Firestore
- 👨‍⚕️ **Admin Dashboard**: Manage users and appointments

---

## ✨ Features

### 🗣️ Multilingual Chatbot
- **8 Languages Supported**: English, Hindi, Marathi, Tamil, Bengali, Telugu, Kannada, Gujarati
- **Auto Language Detection**: Automatically detects input language
- **Flexible Output**: Choose your preferred response language
- **60+ Health Conditions**: Comprehensive symptom database

### 🎙️ Voice Capabilities
- **Speech-to-Text**: Speak your symptoms naturally
- **Text-to-Speech**: Listen to health advice
- **Pause/Resume Controls**: Full audio playback control
- **Female Voice**: Natural-sounding voice output
- **Multi-language TTS**: Proper pronunciation for all languages

### 👤 User Features
- **User Authentication**: Secure login/signup with Firebase
- **Phone/Email Login**: Flexible authentication options
- **Personal Dashboard**: Track appointments and health records
- **Appointment Booking**: Schedule consultations
- **Audio Recording**: Record symptoms for doctors

### 👨‍💼 Admin Features
- **Admin Dashboard**: Manage all users and appointments
- **User Management**: View and manage registered users
- **Appointment Management**: Track and manage bookings
- **Role-based Access**: Secure admin-only features
- **Analytics**: View registration and appointment data

---

## 🛠️ Tech Stack

### Frontend
- **HTML5/CSS3**: Modern, responsive UI
- **JavaScript (ES6+)**: Interactive functionality
- **Web Speech API**: Voice input/output
- **Firebase SDK**: Authentication & Database

### Backend & Services
- **Firebase Authentication**: User management
- **Cloud Firestore**: NoSQL database
- **Firebase Hosting**: Static site hosting
- **Firebase Storage**: File storage (audio recordings)

### Optional Backend
- **Python Flask**: Alternative chatbot backend
- **Google Translate API**: Translation services

---

## 🚀 Getting Started

### Prerequisites

- Node.js (v14 or higher)
- Firebase CLI
- Git
- Modern web browser (Chrome, Edge, Safari)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/luckybiswal98210-eng/Arogya-Vani.git
   cd Arogya-Vani
   ```

2. **Install Firebase CLI** (if not already installed)
   ```bash
   npm install -g firebase-tools
   ```

3. **Login to Firebase**
   ```bash
   firebase login
   ```

4. **Set up Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com)
   - Create a new project or use existing one
   - Enable Authentication (Email/Password)
   - Enable Firestore Database
   - Enable Storage

5. **Configure Firebase**
   - Update `public/js/firebase.js` with your Firebase config:
   ```javascript
   const firebaseConfig = {
     apiKey: "YOUR_API_KEY",
     authDomain: "YOUR_AUTH_DOMAIN",
     projectId: "YOUR_PROJECT_ID",
     storageBucket: "YOUR_STORAGE_BUCKET",
     messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
     appId: "YOUR_APP_ID"
   };
   ```

6. **Deploy to Firebase**
   ```bash
   firebase deploy
   ```

### Local Development

To run locally:

```bash
firebase serve
```

Visit `http://localhost:5000` in your browser.

---

## 📁 Project Structure

```
Arogya-Vani/
├── public/                      # Public web files
│   ├── index.html              # Unified login page
│   ├── dashboard.html          # User dashboard
│   ├── login.html              # Login redirect page
│   ├── signup.html             # User registration
│   ├── chatbot-new.html        # Enhanced chatbot interface
│   ├── chatbot-data.js         # Multilingual health database
│   ├── fix-admin-access.html   # Admin role management tool
│   │
│   ├── admin/                  # Admin section
│   │   ├── admin-dashboard.html
│   │   └── admin-login.html
│   │
│   ├── css/                    # Stylesheets
│   │   └── style.css
│   │
│   ├── js/                     # JavaScript modules
│   │   ├── firebase.js         # Firebase configuration
│   │   ├── user/               # User-related scripts
│   │   │   ├── user.js
│   │   │   ├── unified-login.js
│   │   │   └── signup.js
│   │   └── admin/              # Admin-related scripts
│   │       ├── admin.js
│   │       └── admin-login.js
│   │
│   └── assets/                 # Images, icons, etc.
│
├── chatbot_backend.py          # Optional Python Flask backend
├── chatbot_requirements.txt    # Python dependencies
├── CHATBOT_README.md          # Chatbot documentation
├── firebase.json              # Firebase configuration
├── .firebaserc                # Firebase project settings
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## ⚙️ Configuration

### Firebase Setup

1. **Authentication**
   - Enable Email/Password authentication
   - Configure authorized domains

2. **Firestore Database**
   - Create collections: `users`, `appointments`, `recordings`
   - Set up security rules (see below)

3. **Storage**
   - Create bucket for audio recordings
   - Configure CORS if needed

### Firestore Security Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
      allow read: if request.auth != null && get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }
    
    match /appointments/{appointmentId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### Admin Setup

To create an admin user:

1. Visit: `https://your-app.web.app/fix-admin-access.html`
2. Enter admin email and password
3. Click "Grant Admin Access"

Or manually in Firebase Console:
1. Go to Firestore Database
2. Find user document
3. Add field: `role: "admin"`

---

## 🌐 Deployment

### Deploy to Firebase Hosting

```bash
# Build and deploy
firebase deploy

# Deploy only hosting
firebase deploy --only hosting

# Deploy with specific project
firebase use your-project-id
firebase deploy
```

### Environment Variables

No environment variables needed for frontend. All configuration is in `firebase.js`.

---

## 📖 Usage

### For Users

1. **Sign Up**: Create account with email/phone
2. **Login**: Access your dashboard
3. **Chat**: Click "Chat with Health Bot"
4. **Select Language**: Choose your preferred response language
5. **Input Symptoms**: Type or speak your symptoms
6. **Get Advice**: Receive health recommendations
7. **Listen**: Click play to hear responses

### For Admins

1. **Login**: Use admin credentials at login page
2. **Select Admin**: Click "Admin" button
3. **Dashboard**: View all users and appointments
4. **Manage**: Handle user requests and bookings

### Chatbot Features

- **Text Input**: Type symptoms in any language
- **Voice Input**: Click 🎤 to speak
- **Language Selection**: Choose output language from dropdown
- **Audio Playback**: Click 🔊 Play to listen
- **Pause/Resume**: Control audio playback
- **Multi-language**: Input in one language, output in another

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Lucky Biswal**
- GitHub: [@luckybiswal98210-eng](https://github.com/luckybiswal98210-eng)
- Project Link: [https://github.com/luckybiswal98210-eng/Arogya-Vani](https://github.com/luckybiswal98210-eng/Arogya-Vani)

---

## 🙏 Acknowledgments

- Firebase for backend services
- Web Speech API for voice capabilities
- Google Fonts for typography
- All contributors and users

---

## 📞 Support

For support, email -> luckybiswal736@gmail.com or open an issue on GitHub.

---

<div align="center">

**Made with ❤️ for accessible healthcare**

⭐ Star this repo if you find it helpful!

</div>
