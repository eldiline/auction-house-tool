document.getElementsByClassName("button-success")[0].addEventListener("click", displaySpinner);

function displaySpinner() {
    document.getElementsByClassName("spinner")[0].style.display = "block";
}
