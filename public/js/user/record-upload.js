import { auth } from "/js/firebase.js";
import { uploadAudioToSupabaseAndSave } from "/js/user/audio.js";

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
  console.log("Audio recording script loaded");

  const startBtn = document.getElementById("startRecBtn");
  const stopBtn = document.getElementById("stopRecBtn");
  const statusEl = document.getElementById("audioStatus");
  const errEl = document.getElementById("audioErr");
  const player = document.getElementById("audioPlayer");

  // Check if all elements exist
  if (!startBtn || !stopBtn || !statusEl || !errEl || !player) {
    console.error("Audio recording elements not found:", {
      startBtn: !!startBtn,
      stopBtn: !!stopBtn,
      statusEl: !!statusEl,
      errEl: !!errEl,
      player: !!player
    });
    return;
  }

  console.log("All audio elements found successfully");

  let mediaRecorder;
  let chunks = [];

  function showErr(e) {
    const errorMsg = String(e?.message || e);
    errEl.textContent = errorMsg;
    console.error("Audio error:", e);
  }

  auth.onAuthStateChanged((user) => {
    if (!user) {
      statusEl.textContent = "Status: Please login first.";
    } else {
      console.log("User authenticated for audio recording");
    }
  });

  startBtn.addEventListener("click", async () => {
    console.log("Start recording button clicked");
    errEl.textContent = "";

    try {
      statusEl.textContent = "Status: Asking mic permission...";
      console.log("Requesting microphone access...");

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      console.log("Microphone access granted");

      chunks = [];
      mediaRecorder = new MediaRecorder(stream);
      console.log("MediaRecorder created");

      mediaRecorder.ondataavailable = (e) => {
        chunks.push(e.data);
        console.log("Audio data chunk received");
      };

      mediaRecorder.onstop = async () => {
        console.log("Recording stopped, processing...");
        const blob = new Blob(chunks, { type: "audio/webm" });
        player.src = URL.createObjectURL(blob);
        console.log("Audio blob created, size:", blob.size);

        const user = auth.currentUser;
        if (!user) {
          statusEl.textContent = "Status: Not logged in.";
          console.error("User not logged in");
          return;
        }

        statusEl.textContent = "Status: Uploading...";
        console.log("Starting upload to Supabase...");

        try {
          const url = await uploadAudioToSupabaseAndSave(user.uid, blob);
          statusEl.textContent = "Status: Uploaded ✅";
          console.log("Audio uploaded successfully:", url);
        } catch (e) {
          statusEl.textContent = "Status: Upload failed ❌";
          showErr(e);
        }
      };

      mediaRecorder.start();
      statusEl.textContent = "Status: Recording...";
      startBtn.disabled = true;
      stopBtn.disabled = false;
      console.log("Recording started");

    } catch (e) {
      statusEl.textContent = "Status: Recording failed ❌";
      showErr(e);
      console.error("Failed to start recording:", e);
    }
  });

  stopBtn.addEventListener("click", () => {
    console.log("Stop recording button clicked");
    try {
      if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        statusEl.textContent = "Status: Processing...";
        startBtn.disabled = false;
        stopBtn.disabled = true;
        console.log("Stopping recording...");
      } else {
        console.warn("MediaRecorder not recording. State:", mediaRecorder?.state);
      }
    } catch (e) {
      showErr(e);
    }
  });

  console.log("Audio recording event listeners attached");
});
