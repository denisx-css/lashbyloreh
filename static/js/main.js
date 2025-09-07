// Smooth Scroll for CTA buttons
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function(e) {
      e.preventDefault();
      document.querySelector(this.getAttribute("href")).scrollIntoView({
        behavior: "smooth"
      });
    });
  });
  
  // Simple form validation
  document.querySelector("form").addEventListener("submit", function(e) {
    let email = this.querySelector("input[name=email]").value;
    if (!email.includes("@")) {
      alert("Please enter a valid email.");
      e.preventDefault();
    }
  });
  

  document.addEventListener("DOMContentLoaded", function () {
    const menuBtn = document.getElementById("menu-btn");
    const navLinks = document.getElementById("nav-links");

    menuBtn.addEventListener("click", () => {
        navLinks.classList.toggle("show");
    });
});
