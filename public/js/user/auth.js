import { auth, db } from "/js/firebase.js";
import { signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";
import { collection, query, where, getDocs } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore.js";

const form = document.getElementById("loginForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const identifier = document.getElementById("identifier").value.trim();
  const password = document.getElementById("password").value;

  if (!identifier || !password) {
    alert("Please fill all fields");
    return;
  }

  try {
    let emailToUse = identifier;

    // If input is phone, get email from Firestore
    if (!identifier.includes("@")) {
      const q = query(collection(db, "users"), where("phone", "==", identifier));
      const snap = await getDocs(q);

      if (snap.empty) {
        alert("No user found with this phone number");
        return;
      }
      emailToUse = snap.docs[0].data().email;
    }

    await signInWithEmailAndPassword(auth, emailToUse, password);

    // Redirect after login
    window.location.href = "/public/index.html";
  } catch (err) {
    alert("Login failed ❌ " + err.message);
  }
});
