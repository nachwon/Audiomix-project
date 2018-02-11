function like(pk) {
    var url = "/post/" + pk + "/like/";

    var counter = $("#like-count-" + pk);
    var csrf_token = $('[name=csrfmiddlewaretoken]').val();
    $.ajax({
        type: "POST",
        url: url,
        data: {'pk': pk, 'csrfmiddlewaretoken': csrf_token},
        async: true,
        dataType: "json",
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
