// التأكد من أن firebase تم تحميله
console.log(firebase);

// تهيئة Firebase Auth
const auth = firebase.auth();
const provider = new firebase.auth.GoogleAuthProvider();

// زر تسجيل الدخول
document.getElementById("google-login").addEventListener("click", function() {
  auth.signInWithPopup(provider)
    .then((result) => {
      const user = result.user;
      alert(`Welcome, ${user.displayName}`);
    })
    .catch((error) => {
      console.error("Error during sign-in:", error.message);
    });
});

// مراقبة حالة المستخدم
firebase.auth().onAuthStateChanged((user) => {
  if (user) {
    console.log("User is signed in:", user);
  } else {
    console.log("No user is signed in.");
  }
});
