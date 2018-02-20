$(document).ready(function(){
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


// $.ajax({
//     type: "POST",
//     url: url,
//     data:
//         {
//             'counter': counter,
//             'csrfmiddlewaretoken': csrf_token
//         },
//     async: true,
//     dataType: "json",
//     success: function(response) {
//         // 받아온 html을 show-tracks div 안에 붙여준다.
//         target.append(response.html)
//     }
// });