const changeButton = document.getElementsByClassName("change-name")[0];
const cross = document.getElementById("cross");
const popup = document.getElementsByClassName("change-name-popup")[0];

changeButton.addEventListener("click", () => {
    popup.style.display = "flex";
});

cross.addEventListener("click", () => {
    popup.style.display = "none";
});