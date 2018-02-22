var comment_obj = $(".comment-obj");

comment_obj.find(".comment-play-icon").on("click", function () {
   var pk = $(this).attr("data-comment-pk");
   console.log($("#comment-track-" + pk)[0].play())
});