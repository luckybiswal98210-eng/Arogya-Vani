// js/firebase.js

import { initializeApp } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore.js";

// 🔑 Firebase configuration (PASTE YOUR VALUES HERE)
const firebaseConfig = {
  apiKey: "AIzaSyDZy_N-s3PC3S2aQvNjGCsQSb0XUYqYkBs",
  authDomain:"arogya-vani-2c4fb.firebaseapp.com",
  projectId: "arogya-vani-2c4fb",
  storageBucket: "arogya-vani-2c4fb.firebasestorage.app",
  messagingSenderId:  "36916357856",
  appId: "1:36916357856:web:4d5ce0c837c87d77ca3e85",
};

// 🚀 Initialize Firebase
const app = initializeApp(firebaseConfig);

// 🔐 Firebase services
export const auth = getAuth(app);
export const db = getFirestore(app);
