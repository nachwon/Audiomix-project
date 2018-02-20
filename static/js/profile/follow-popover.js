$(document).ready(function(){
    // follow 팝오버 창 동작 설정
    $('.follow-hover-up').popover(
        {
            html: true,
            trigger: "manual",
            placement: "top"
        })
        .on("mouseenter", function() {
            var _this = this;
            $(this).popover("show");
            $(".popover").on("mouseleave", function() {
                $(_this).popover("hide");
            });
        })
        .on("mouseleave", function() {
            var _this = this;
            setTimeout(function () {
                if (!$(".popover:hover").length) {
                    $(_this).popover("hide");
                }
            }, 0);
        });
    $('.follow-hover-down').popover(
        {
            html: true,
            trigger: "manual",
            placement: "bottom"
        })
        .on("mouseenter", function() {
            var _this = this;
            $(this).popover("show");
            $(".popover").on("mouseleave", function() {
                $(_this).popover("hide");
            });
        })
        .on("mouseleave", function() {
            var _this = this;
            setTimeout(function () {
                if (!$(".popover:hover").length) {
                    $(_this).popover("hide");
                }
            }, 0);
        });
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
