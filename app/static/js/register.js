document.getElementById("registerForm").addEventListener("submit", function(e){
  e.preventDefault();

  const username = this.username.value;
  const email = this.email.value;
  const password = this.password.value;

  fetch("/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
    credentials: "include"
  })
  .then(res => {
    if (!res.ok) {
      return res.json().then(err => { throw err; });
    }
    return res.json();
  })
  .then(data => {
    alert("Registration successfull!");
    window.location.href = "/api/investigation/investigations/";
  })
  .catch(err => {
    console.error(err);
    alert(err.error || "Error durin registration process");
  });
});