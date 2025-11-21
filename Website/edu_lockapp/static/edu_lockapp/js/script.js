document.addEventListener("DOMContentLoaded", () => {
    const welcomeScreen = document.getElementById("welcome-screen");
    const pageContent = document.getElementById("page-content");

    // Default sichtbar machen, falls kein welcome-screen
    pageContent.style.opacity = welcomeScreen ? "0" : "1";

    if (welcomeScreen) {
        setTimeout(() => {
            welcomeScreen.classList.add("fade-out");

            setTimeout(() => {
                welcomeScreen.remove();
                pageContent.style.transition = "opacity 1.1s ease";
                pageContent.style.opacity = "1";
            }, 1200);

        }, 5000); // 5 Sekunden Anzeige
    }
});
