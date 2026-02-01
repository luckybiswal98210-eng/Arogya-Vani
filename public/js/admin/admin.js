import { auth, db } from "/js/firebase.js";
import { signOut } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";
import {
  collection,
  getDocs,
  addDoc,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore.js";

// -------- ELEMENT REFERENCES --------
const regList = document.getElementById("regList");
const logoutBtn = document.getElementById("logoutBtn");
const addBtn = document.getElementById("addVaccineBtn");

// -------- LOAD REGISTRATIONS --------
async function loadRegistrations() {
  regList.innerHTML = "Loading registrations...";

  const snap = await getDocs(collection(db, "registrations"));
  regList.innerHTML = "";

  if (snap.empty) {
    regList.innerHTML = '<div class="no-data">📭 No registrations found yet.</div>';
    return;
  }

  snap.forEach(doc => {
    const data = doc.data();
    const f = data.formData || {};

    // ----- CHILD PHOTO -----
    const photoHTML = f.childPhotoBase64
      ? `<img src="${f.childPhotoBase64}"
              alt="Child Photo"
              style="width:150px;height:150px;object-fit:cover;border-radius:12px;border:2px solid #667eea;">`
      : `<p style="color:#999;font-style:italic;">No photo available</p>`;

    // ----- AUDIO (URL or Base64) -----
    let audioHTML = `<p style="color:#999;font-style:italic;">No audio available</p>`;
    if (data.audioURL) {
      audioHTML = `
        <audio controls style="width:100%;max-width:300px;">
          <source src="${data.audioURL}">
          Your browser does not support audio.
        </audio>
      `;
    } else if (f.audioUrl) {
      audioHTML = `
        <audio controls style="width:100%;max-width:300px;">
          <source src="${f.audioUrl}">
          Your browser does not support audio.
        </audio>
      `;
    } else if (f.audioBase64) {
      audioHTML = `
        <audio controls style="width:100%;max-width:300px;">
          <source src="${f.audioBase64}">
          Your browser does not support audio.
        </audio>
      `;
    }

    const div = document.createElement("div");
    div.className = "registration-card";
    div.innerHTML = `
      <h4>📋 Registration Details</h4>
      
      <div class="media-section">
        <div class="media-box">
          <h5>👶 Child Photo</h5>
          ${photoHTML}
        </div>
        <div class="media-box">
          <h5>🎤 Audio Message</h5>
          ${audioHTML}
        </div>
      </div>

      <div class="info-grid">
        <div class="info-item">
          <strong>Child Name:</strong>
          <span>${f.childName || "N/A"}</span>
        </div>
        <div class="info-item">
          <strong>Parent Name:</strong>
          <span>${f.parentName || "N/A"}</span>
        </div>
        <div class="info-item">
          <strong>Date of Birth:</strong>
          <span>${f.dateOfBirth || f.dob || "N/A"}</span>
        </div>
        <div class="info-item">
          <strong>Gender:</strong>
          <span>${f.gender || "N/A"}</span>
        </div>
        <div class="info-item">
          <strong>Blood Group:</strong>
          <span>${f.bloodGroup || "N/A"}</span>
        </div>
        <div class="info-item">
          <strong>Phone:</strong>
          <span>${f.phone || "N/A"}</span>
        </div>
        <div class="info-item">
          <strong>Email:</strong>
          <span>${f.mailId || "N/A"}</span>
        </div>
        <div class="info-item">
          <strong>Address:</strong>
          <span>${f.address || "N/A"}</span>
        </div>
      </div>

      <div class="action-buttons">
        <button class="btn-call" onclick="makeCall('${f.phone}')">📞 Call</button>
        <button class="btn-sms" onclick="sendSMS('${f.phone}', '${f.childName}')">💬 SMS</button>
        <button class="btn-email" onclick="sendEmail('${f.mailId}', '${f.childName}')">📧 Email</button>
        <button class="btn-whatsapp" onclick="sendWhatsApp('${f.phone}', '${f.childName}')">🟢 WhatsApp</button>
      </div>
    `;

    regList.appendChild(div);
  });
}

// Load registrations on page load
loadRegistrations();

// -------- ADD VACCINATION --------
addBtn.addEventListener("click", async () => {
  const userId = document.getElementById("userId").value.trim();
  const vaccineName = document.getElementById("vaccineName").value.trim();
  const nextDate = document.getElementById("nextDate").value;

  if (!userId || !vaccineName || !nextDate) {
    alert("Please fill all fields");
    return;
  }

  try {
    await addDoc(collection(db, "vaccinations"), {
      userId,
      vaccineName,
      nextVaccineDate: nextDate,
      createdAt: serverTimestamp()
    });

    alert("Vaccination added successfully ✅");
  } catch (err) {
    alert("Error ❌ " + err.message);
  }
});

// -------- COMMUNICATION FUNCTIONS --------

// 📞 CALL
window.makeCall = function (phone) {
  if (!phone) {
    alert("Phone number not available");
    return;
  }
  window.location.href = `tel:${phone}`;
};

// 💬 SMS
window.sendSMS = function (phone, childName) {
  if (!phone) {
    alert("Phone number not available");
    return;
  }
  const msg = `Reminder: ${childName}'s vaccination is scheduled soon. - Arogya Vani`;
  window.location.href = `sms:${phone}?body=${encodeURIComponent(msg)}`;
};

// 📧 EMAIL
window.sendEmail = function (email, childName) {
  if (!email) {
    alert("Email not available");
    return;
  }
  const subject = "Vaccination Reminder - Arogya Vani";
  const body =
    `Hello,\n\nThis is a reminder that ${childName}'s vaccination is scheduled soon.\n\nRegards,\nArogya Vani`;

  window.location.href =
    `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
};

// 🟢 WHATSAPP
window.sendWhatsApp = function (phone, childName) {
  if (!phone) {
    alert("Phone number not available");
    return;
  }
  const message =
    `Hello! Reminder: ${childName}'s next vaccination is scheduled soon. Please check Arogya Vani app.`;

  const url = `https://wa.me/91${phone}?text=${encodeURIComponent(message)}`;
  window.open(url, "_blank");
};

// -------- LOGOUT --------
logoutBtn.addEventListener("click", async () => {
  await signOut(auth);
  window.location.href = "/login.html";
});