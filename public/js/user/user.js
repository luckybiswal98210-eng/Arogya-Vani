import { auth, db } from "/js/firebase.js";
import { signOut } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";
import {
  collection,
  query,
  where,
  getDocs,
  limit
} from "https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore.js";

const nextEl = document.getElementById("nextVaccineDate");
const logoutBtn = document.getElementById("logoutBtn");

// ✅ Auth check
auth.onAuthStateChanged(async (user) => {
  if (!user) {
    // 🔥 ALWAYS redirect to the SAME login page
    window.location.href = "/login.html";
    return;
  }

  try {
    const q = query(
      collection(db, "vaccinations"),
      where("userId", "==", user.uid),
      limit(1)
    );

    const snap = await getDocs(q);

    if (snap.empty) {
      nextEl.textContent = "No vaccination date found yet.";
      return;
    }

    const data = snap.docs[0].data();
    nextEl.textContent = data.nextVaccineDate || "Not set";
  } catch (err) {
    nextEl.textContent = "Error: " + err.message;
  }
});

// ✅ Logout
logoutBtn.addEventListener("click", async () => {
  try {
    await signOut(auth);

    // 🔥 FORCE correct login page
    window.location.href = "/login.html";
  } catch (e) {
    alert("Logout failed ❌ " + e.message);
  }
});
