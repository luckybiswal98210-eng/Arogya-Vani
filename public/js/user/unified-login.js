import { auth, db } from "/js/firebase.js";
import { signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";
import { collection, query, where, getDocs, doc, getDoc } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore.js";

const form = document.getElementById("loginForm");
const errorMsg = document.getElementById("errorMsg");
const loginTypeBtns = document.querySelectorAll(".login-type-btn");
const identifierInput = document.getElementById("identifier");

let currentLoginType = "user"; // Default to user login

// Handle login type selection
loginTypeBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        // Remove active class from all buttons
        loginTypeBtns.forEach(b => b.classList.remove("active"));

        // Add active class to clicked button
        btn.classList.add("active");

        // Update current login type
        currentLoginType = btn.dataset.type;

        // Update placeholder based on login type
        if (currentLoginType === "admin") {
            identifierInput.placeholder = "Admin Email";
        } else {
            identifierInput.placeholder = "Email or Phone Number";
        }

        // Clear error message
        errorMsg.textContent = "";
    });
});

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorMsg.textContent = "";

    const identifier = document.getElementById("identifier").value.trim();
    const password = document.getElementById("password").value;

    if (!identifier || !password) {
        errorMsg.textContent = "Please fill all fields";
        return;
    }

    try {
        let emailToUse = identifier;

        // USER LOGIN - Allow phone or email
        if (currentLoginType === "user") {
            // If input is phone, get email from Firestore
            if (!identifier.includes("@")) {
                const q = query(collection(db, "users"), where("phone", "==", identifier));
                const snap = await getDocs(q);

                if (snap.empty) {
                    errorMsg.textContent = "No user found with this phone number";
                    return;
                }
                emailToUse = snap.docs[0].data().email;
            }

            // Sign in with Firebase Auth
            await signInWithEmailAndPassword(auth, emailToUse, password);

            // Redirect to user dashboard
            window.location.href = "/index.html";
        }
        // ADMIN LOGIN - Check role
        else if (currentLoginType === "admin") {
            // Admin must use email
            if (!identifier.includes("@")) {
                errorMsg.textContent = "Admin must login with email";
                return;
            }

            // Sign in with Firebase Auth
            const cred = await signInWithEmailAndPassword(auth, identifier, password);
            const uid = cred.user.uid;

            // Check if user has admin role
            const userDoc = await getDoc(doc(db, "users", uid));

            if (userDoc.exists() && userDoc.data().role === "admin") {
                // Redirect to admin dashboard
                window.location.href = "/admin/admin-dashboard.html";
            } else {
                // Not an admin - sign out and show error
                await auth.signOut();
                errorMsg.textContent = "Access denied. You are not an admin.";
            }
        }
    } catch (err) {
        console.error("Login error:", err);

        // User-friendly error messages
        if (err.code === "auth/invalid-credential" || err.code === "auth/wrong-password") {
            errorMsg.textContent = "Invalid email/phone or password";
        } else if (err.code === "auth/user-not-found") {
            errorMsg.textContent = "No account found with this email";
        } else if (err.code === "auth/too-many-requests") {
            errorMsg.textContent = "Too many failed attempts. Please try again later.";
        } else {
            errorMsg.textContent = "Login failed: " + err.message;
        }
    }
});
