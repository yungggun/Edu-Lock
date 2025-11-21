document.addEventListener("DOMContentLoaded", () => {
    const welcomeScreen = document.getElementById("welcome-screen");
    const pageContent = document.getElementById("page-content");

    pageContent.style.opacity = "0";

    // Gesamtdauer bevor der Screen verschwindet
    setTimeout(() => {
        welcomeScreen.classList.add("fade-out");

        setTimeout(() => {
            welcomeScreen.remove();
            pageContent.style.transition = "opacity 1.1s ease";
            pageContent.style.opacity = "1";
        }, 1200);

    }, 5000); // → bleibt 5 Sekunden sichtbar
});
