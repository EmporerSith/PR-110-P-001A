// document.addEventListener("DOMContentLoaded", function () {
//   const darkModeToggle = document.getElementById("darkModeToggle");
//   const body = document.body;

//   // Check if dark mode was previously enabled
//   const isDarkMode = localStorage.getItem("darkMode") === "enabled";
//   if (isDarkMode) {
//     body.classList.add("dark-mode");
//     darkModeToggle.textContent = "Light Mode";
//   }

//   // Toggle dark mode on button click
//   darkModeToggle.addEventListener("click", function () {
//     body.classList.toggle("dark-mode");
//     if (body.classList.contains("dark-mode")) {
//       localStorage.setItem("darkMode", "enabled");
//       darkModeToggle.textContent = "Light Mode";
//     } else {
//       localStorage.setItem("darkMode", "disabled");
//       darkModeToggle.textContent = "Dark Mode";
//     }
//   });
// });
