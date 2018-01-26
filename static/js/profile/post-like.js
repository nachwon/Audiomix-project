$(document).ready(function() {
    // like 버튼의 초기 상태 설정 및 클릭시 클래스 바꿔주는 함수 실행
    var like_btn_list = document.getElementsByClassName("like-btn");
    for (var i = 0; i < like_btn_list.length; i++) {
        var el = like_btn_list[i];
        get_like_status(el);
        el.onclick = function(el) {
            like(el);
            if (this.className === "like-btn glyphicon glyphicon-heart") {
                this.className = "like-btn glyphicon glyphicon-heart-empty"
            }
            else {
                this.className = "like-btn glyphicon glyphicon-heart"
            }
        };
    }
});


function like(el) {
    var post_pk = el.target.getAttribute('data-post-pk');
    var xhttp = new XMLHttpRequest();
    var csrf_token = $('[name=csrfmiddlewaretoken]').val();

    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 201) {
                var count = JSON.parse(xhttp.responseText).count;
                change_like_count(post_pk, count)
            }
            else if (this.status === 204) {
                var count = document.getElementById("like-count-" + post_pk).innerText;
                change_like_count(post_pk, count - 1)
            }
        }
    };

    xhttp.open("POST", "/post/" + post_pk + "/like/", true);
    xhttp.setRequestHeader('X-CSRFToken', csrf_token);
    xhttp.send({"user": "{{ request.user }}"})
}

function get_like_status(el) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (xhttp.response === "True") {
                el.className = "like-btn glyphicon glyphicon-heart"
            }
            else {
                el.className = "like-btn glyphicon glyphicon-heart-empty"
            }
        }
    };

    var pk = el.getAttribute('data-post-pk');
    xhttp.open("GET", "/post/" + pk + "/like/", true);
    xhttp.send()
}

function change_like_count(id, count) {
    document.getElementById("like-count-" + id).innerHTML = count
}