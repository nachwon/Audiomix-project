$(document).ready(function() {
    $(".followers-obj").find("a")
        .on("mouseenter", function() {
            $(this).parent().find(".follow-popover").css("display", "block")
        })
        .on("mouseleave", function() {
            $(this).parent().find(".follow-popover").css("display", "none")
        });

    $(".follow-popover")
        .on("mouseenter", function() {
            $(this).css("display", "block")
        })
        .on("mouseleave", function() {
            $(this).css("display", "none")
        })
});

// 팝오버 창에서 팔로우 버튼 ajax 보내기
function popoverFollow(self, pk) {
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
                $(self).text("Following")
            }
            else {
                $(self).text("Follow")
            }
        }
    })
}
