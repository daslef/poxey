const changeName = document.getElementsByClassName("change-name")[0];
const changePassword = document.getElementsByClassName("change-password")[0];
const crossName = document.getElementById("crossName");
const crossPassword = document.getElementById("crossPassword");

changeName.addEventListener("click", () => {
    $(".change-password-popup").fadeOut('fast','swing');
    $(".change-name-popup").fadeIn("normal", "linear");
    $(".change-name-popup").css("display", "flex");
});

changePassword.addEventListener("click", () => {
    $(".change-name-popup").fadeOut('fast','swing');
    $(".change-password-popup").fadeIn("normal", "linear");
    $(".change-password-popup").css("display", "flex");
});

crossName.addEventListener("click", () => {
    $(".change-name-popup").fadeOut('fast','swing');
});

crossPassword.addEventListener("click", () => {
    $(".change-password-popup").fadeOut('fast','swing');
});