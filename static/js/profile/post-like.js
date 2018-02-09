
$(document).ready(function() {
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

    $(".like-btn").click(function (){
        var pk = $(this).attr("data-post-pk");
        var url = $(this).attr("data-url");
        var counter = $("#like-count-" + pk);
        var csrf_token = $('[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: "POST",
            url: url,
            data: {'pk': pk, 'csrfmiddlewaretoken': csrf_token},
            async: true,
            dataType: "json",
            success: function(response) {
                counter.html(response.count)
            }
        })
    });
});

