document.addEventListener("DOMContentLoaded", () => {
  const checkbox = document.querySelector("input[data-toggle-theme]");
  const storedTheme = localStorage.getItem("theme");

  if (checkbox && storedTheme) {
    const [light, dark] = checkbox.dataset.toggleTheme.split(",");
    checkbox.checked = storedTheme === dark;
  }

  // Set a default theme if none exists
  if (!storedTheme) {
    const defaultTheme = "garden";
    localStorage.setItem("theme", defaultTheme);
    document.documentElement.setAttribute("data-theme", defaultTheme);
  }
});
