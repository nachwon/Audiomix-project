function like(pk) {
    var url = "/post/" + pk + "/like/";
    var counter = $("#like-count-" + pk);
    var csrf_token = $('[name=csrfmiddlewaretoken]').val();

    // ajax 요청
    $.ajax({
        type: "POST",
        url: url,
        data: {'pk': pk, 'csrfmiddlewaretoken': csrf_token},
        async: true,
        dataType: "json",
        // 성공시 하트 아이콘 변경, 카운트 갱신
        success: function (response) {
            counter.html(response.count);
            var btn = $("#like-btn-" + pk);
            if (btn[0].className === "like-btn glyphicon glyphicon-heart") {
                btn[0].className = "like-btn glyphicon glyphicon-heart-empty"
            }
            else {
                btn[0].className = "like-btn glyphicon glyphicon-heart"
            }
        }
    })
}
