function hideBtn() {
    var index = document.getElementsByClassName("active")[0].getAttribute("data-slide-to");
    console.log(index);
    if (index == 0) {
        document.getElementById("prev-btn").style.display = 'none';
    }
    else if (index == 2) {
        document.getElementById("next-btn").style.display = 'none';
    }
    else {
        document.getElementById("prev-btn").style.display = 'block';
        document.getElementById("next-btn").style.display = 'block';
    }
}

$(document).ready(function() {
    hideBtn();
});

