$(document).ready(function() {
    $(".followers-obj")
        .on("mouseenter", function() {
            console.log("btn enter");
            $(this).find(".follow-popover").css("display", "block")
        })
        .on("mouseleave", function() {
            console.log("btn leave");
            $(this).find(".follow-popover").css("display", "none")
        });

    $(".psuedo-object-wrapper")
        .on("mouseenter", function() {
            console.log("popover enter");
            $(this).parent().css("display", "block")
        })
        .on("mouseleave", function() {
            console.log("popover leave");
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
