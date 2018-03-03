$(document).ready(function() {
    $(".followers-obj").find("a")
        .on("mouseenter", function() {
            $(this).parent().find(".follow-popover").css("display", "block")
        })
        .on("mouseleave", function() {
            $(this).parent().find(".follow-popover").css("display", "none")
        });

    $(".psuedo-object-wrapper")
        .on("mouseenter", function() {
            $(this).parent().css("display", "block")
        })
        .on("mouseleave", function() {
            $(this).parent().css("display", "none")
        })
});

// 팝오버 창에서 팔로우 버튼 ajax 보내기
function popoverFollow(pk) {
    var csrf_token = $('[name=csrfmiddlewaretoken]').val();
    $.ajax({
        type: "POST",
        url: "/user/" + pk + "/follow/",
        data: {
            "pk": pk,
            "csrfmiddlewaretoken": csrf_token
        },
        dataType: "json",
        success: function(response) {
            if (response) {
                $(".follow-popover-btn")[0].innerText = "Following"
            }
            else {
                $(".follow-popover-btn")[0].innerText = "Follow"
            }
        }
    })
}
