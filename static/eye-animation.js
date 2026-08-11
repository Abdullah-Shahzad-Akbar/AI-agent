let img = document.getElementById("img");
let password = document.getElementById("pass");
img.onclick = function () {
    if (password.type == "password") {
        password.type = "text";
        img.src = "static/close-eye.png";
    }
    else {
        password.type = "password";
        img.src = "static/open-eye.png";
    }
}
