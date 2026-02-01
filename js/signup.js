import { auth, db } from "./firebase.js";
import { createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";
import { doc, setDoc } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore.js";

const form = document.getElementById("signupForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const phone = document.getElementById("phone").value.trim();
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;

  // Validation
  if (!email || !phone || !password) {
    alert("Please fill all fields");
    return;
  }

  if (password !== confirmPassword) {
    alert("Passwords do not match");
    return;
  }

  if (password.length < 6) {
    alert("Password must be at least 6 characters");
    return;
  }

  try {
    // Create Firebase Auth user
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;

    // Store additional user info (phone) in Firestore
    await setDoc(doc(db, "users", user.uid), {
      email: email,
      phone: phone,
      createdAt: new Date().toISOString()
    });

    alert("Account created successfully! ✅ Please login.");
    window.location.href = "/login.html";
  } catch (err) {
    console.error("Signup error:", err);

    // User-friendly error messages
    let errorMessage = "Signup failed ❌ ";
    if (err.code === "auth/email-already-in-use") {
      errorMessage += "This email is already registered. Please login instead.";
    } else if (err.code === "auth/invalid-email") {
      errorMessage += "Invalid email address.";
    } else if (err.code === "auth/weak-password") {
      errorMessage += "Password is too weak.";
    } else {
      errorMessage += err.message;
    }

    alert(errorMessage);
  }
});
