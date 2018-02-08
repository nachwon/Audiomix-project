
// like 버튼의 초기 상태 설정 및 클릭시 클래스 바꿔주는 함수 실행
var like_btn_list = document.getElementsByClassName("like-btn");
for (var i = 0; i < like_btn_list.length; i++) {
    var el = like_btn_list[i];
    el.onclick = function() {
        if (this.className === "like-btn glyphicon glyphicon-heart") {
            this.className = "like-btn glyphicon glyphicon-heart-empty"
        }
        else {
            this.className = "like-btn glyphicon glyphicon-heart"
        }
    };
}



// function like(el) {
//     var post_pk = el.target.getAttribute('data-post-pk');
//     var xhttp = new XMLHttpRequest();
//     var csrf_token = $('[name=csrfmiddlewaretoken]').val();
//
//     xhttp.onreadystatechange = function() {
//         if (this.readyState === 4) {
//             if (this.status === 201) {
//                 var count = JSON.parse(xhttp.responseText).count;
//                 change_like_count(post_pk, count)
//             }
//             else if (this.status === 204) {
//                 var count = document.getElementById("like-count-" + post_pk).innerText;
//                 change_like_count(post_pk, count - 1)
//             }
//         }
//     };
//
//     xhttp.open("POST", "/post/" + post_pk + "/like/", true);
//     xhttp.setRequestHeader('X-CSRFToken', csrf_token);
//     xhttp.send()
// }
//
// function change_like_count(id, count) {
//     document.getElementById("like-count-" + id).innerHTML = count
// }

$(document).ready(function () {
    $(".like-btn").click(function (){
        var pk = $(this).attr("data-post-pk");
        var url = $(this).attr("data-url");
        var counter = $("#like-count-" + pk);
        var csrf_token = $('[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: "POST",
            url: url,
            data: {'pk': pk, 'csrfmiddlewaretoken': csrf_token},
            dataType: "json",
            success: function(response) {
                counter.html(response.count)
            }
        })
    });
});
