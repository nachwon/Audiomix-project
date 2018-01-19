function hideBtn() {
    var index = document.getElementsByClassName("active")[0].getAttribute("data-slide-to");
    if (index == 0) {
        document.getElementById("next-btn").style.display = 'block';
        document.getElementById("prev-btn").style.display = 'none';
    }
    else if (index == 1) {
        document.getElementById("next-btn").style.display = 'none';
        document.getElementById("prev-btn").style.display = 'block';
    }
    else {
        document.getElementById("prev-btn").style.display = 'block';
        document.getElementById("next-btn").style.display = 'block';
    }
}

$(document).ready(function() {
    hideBtn();
});

