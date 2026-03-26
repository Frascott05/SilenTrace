document.getElementById("loginForm").addEventListener("submit", function(e){
  e.preventDefault();

  const email = this.email.value;
  const password = this.password.value;

  fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
    credentials: "include"
  })
  .then(res => {
    if (!res.ok) {
      return res.json().then(err => { throw err; });
    }
    return res.json();
  })
  .then(data => {
    alert("Login successfull!");
    window.location.href = "/api/investigation/investigations/";
  })
  .catch(err => {
    console.error(err);
    alert(err.error || "Errore during login process");
  });
});