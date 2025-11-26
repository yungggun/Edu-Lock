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
<<<<<<< HEAD
        }, 200);

    }, 1000); // → bleibt 5 Sekunden sichtbar
=======
        }, 1200);

    }, 5000); // → bleibt 5 Sekunden sichtbar
>>>>>>> 791a39d86f5272bb4f13927b5cda6de149304c60
});
