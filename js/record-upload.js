import { auth } from "./firebase.js";
import { uploadAudioToSupabaseAndSave } from "./audio.js";

const startBtn = document.getElementById("startRecBtn");
const stopBtn = document.getElementById("stopRecBtn");
const statusEl = document.getElementById("audioStatus");
const errEl = document.getElementById("audioErr");
const player = document.getElementById("audioPlayer");

let mediaRecorder;
let chunks = [];

function showErr(e) {
  errEl.textContent = String(e?.message || e);
  console.error(e);
}

auth.onAuthStateChanged((user) => {
  if (!user) statusEl.textContent = "Status: Please login first.";
});

startBtn.addEventListener("click", async () => {
  errEl.textContent = "";
  try {
    statusEl.textContent = "Status: Asking mic permission...";
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    chunks = [];
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (e) => chunks.push(e.data);

    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunks, { type: "audio/webm" });
      player.src = URL.createObjectURL(blob);

      const user = auth.currentUser;
      if (!user) { statusEl.textContent = "Status: Not logged in."; return; }

      statusEl.textContent = "Status: Uploading...";
      try {
        const url = await uploadAudioToSupabaseAndSave(user.uid, blob);
        statusEl.textContent = "Status: Uploaded ✅";
        console.log("Audio URL:", url);
      } catch (e) {
        statusEl.textContent = "Status: Upload failed ❌";
        showErr(e);
      }
    };

    mediaRecorder.start();
    statusEl.textContent = "Status: Recording...";
    startBtn.disabled = true;
    stopBtn.disabled = false;

  } catch (e) {
    statusEl.textContent = "Status: Recording failed ❌";
    showErr(e);
  }
});

stopBtn.addEventListener("click", () => {
  try {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
      statusEl.textContent = "Status: Processing...";
      startBtn.disabled = false;
      stopBtn.disabled = true;
    }
  } catch (e) {
    showErr(e);
  }
});
