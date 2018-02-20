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
            console.log("enter");
            var _this = this;
            $(this).popover("show");
            $(".popover").on("mouseleave", function() {
                console.log("leave1");
                $(_this).popover("hide");
            });
        })
        .on("mouseleave", function() {
            console.log("leave2");
            var _this = this;
            setTimeout(function () {
                console.log("leave3");
                if (!$(".popover:hover").length) {
                    $(_this).popover("hide");
                }
            }, 0);
        });
});