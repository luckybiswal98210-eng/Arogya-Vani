import { auth, db } from "./firebase.js";
import {
  collection,
  addDoc,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore.js";

const form = document.getElementById("regForm");
const photoInput = document.getElementById("childPhoto");

auth.onAuthStateChanged((user) => {
  if (!user) window.location.href = "/login.html";
});

// Convert image to Base64
function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const user = auth.currentUser;
  if (!user) return;

  try {
    const childPhotoFile = photoInput.files[0];
    if (!childPhotoFile) {
      alert("Please upload child photo");
      return;
    }

    const childPhotoBase64 = await fileToBase64(childPhotoFile);

    const formData = {
      childName: document.getElementById("childName").value.trim(),
      dob: document.getElementById("dob").value,
      gender: document.getElementById("gender").value,
      parentName: document.getElementById("parentName").value.trim(),
      parentAadhaar: document.getElementById("parentAadhaar").value.trim(),
      bloodGroup: document.getElementById("bloodGroup").value.trim(),
      mailId: document.getElementById("mailId").value.trim(),
      phone: document.getElementById("phone").value.trim(),
      address: document.getElementById("address").value.trim(),
      childPhotoBase64
    };

    // ✅ Create registration doc with audioURL null
    const docRef = await addDoc(collection(db, "registrations"), {
      userId: user.uid,
      formData,
      audioURL: null,
      audioOnly: false,
      createdAt: serverTimestamp()
    });

    // ✅ Save registrationId for attaching audio later (BOTH option)
    localStorage.setItem("lastRegistrationId", docRef.id);

    alert("Registration submitted ✅ You may also record audio from dashboard (optional).");
    window.location.href = "/index.html";
  } catch (err) {
    alert("Submit failed ❌ " + err.message);
  }
});
