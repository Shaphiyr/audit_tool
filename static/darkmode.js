document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("dark-mode-toggle");
    const body = document.body;

    // Check and apply stored dark mode preference
    const isDarkMode = localStorage.getItem("darkMode") === "true";
    if (isDarkMode) {
        body.classList.add("dark-mode");
        toggleButton.textContent = "☀️"; // Sun emoji for light mode
    } else {
        toggleButton.textContent = "🌙"; // Moon emoji for dark mode
    }

    // Toggle dark mode on button click
    toggleButton.addEventListener("click", () => {
        body.classList.toggle("dark-mode");
        const darkModeEnabled = body.classList.contains("dark-mode");
        localStorage.setItem("darkMode", darkModeEnabled); // Save preference
        toggleButton.textContent = darkModeEnabled ? "☀️" : "🌙";
    });
});
