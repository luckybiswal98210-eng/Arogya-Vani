import { auth, db } from "/js/firebase.js";
import { signInWithEmailAndPassword } from
  "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";
import { doc, getDoc } from
  "https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore.js";

const loginBtn = document.getElementById("loginBtn");
const msg = document.getElementById("msg");

loginBtn.addEventListener("click", async () => {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  try {
    const cred = await signInWithEmailAndPassword(auth, email, password);
    const uid = cred.user.uid;

    const snap = await getDoc(doc(db, "users", uid));

    if (snap.exists() && snap.data().role === "admin") {
      window.location.href = "admin-dashboard.html";
    } else {
      msg.innerText = "Access denied. Not an admin.";
    }

  } catch (err) {
    msg.innerText = err.message;
  }
});