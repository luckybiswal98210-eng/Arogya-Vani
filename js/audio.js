import { supabase } from "./supabase.js";
import { db } from "./firebase.js";
import {
  doc,
  updateDoc,
  collection,
  addDoc,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore.js";

export async function uploadAudioToSupabaseAndSave(userId, blob) {
  const fileName = `${userId}_${Date.now()}.webm`;
  const audioFile = new File([blob], fileName, { type: "audio/webm" });

  // 1) Upload to Supabase bucket "audio"
  const { error } = await supabase.storage
    .from("audio")
    .upload(fileName, audioFile, {
      contentType: "audio/webm",
      upsert: true
    });

  if (error) {
    console.error(error);
    throw new Error("Supabase upload failed: " + error.message);
  }

  // 2) Get public URL
  const { data } = supabase.storage.from("audio").getPublicUrl(fileName);
  const audioURL = data.publicUrl;

  // 3) Attach to form registration if exists (BOTH case)
  const registrationId = localStorage.getItem("lastRegistrationId");

  if (registrationId) {
    await updateDoc(doc(db, "registrations", registrationId), {
      audioURL,
      audioOnly: false,
      updatedAt: serverTimestamp()
    });

    return audioURL;
  }

  // 4) Otherwise create audio-only registration
  await addDoc(collection(db, "registrations"), {
    userId,
    formData: null,
    audioURL,
    audioOnly: true,
    createdAt: serverTimestamp()
  });

  return audioURL;
}
