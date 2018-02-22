var comment_obj = $(".comment-obj");

// 커맨트 트랙 재생/일시정지
comment_obj.find(".comment-play-icon").on("click", function () {
    var pk = $(this).attr("data-comment-pk");
    var comment_track = $("#comment-track-" + pk);
    var is_playing = comment_track.attr("data-is-playing");

    if (is_playing === "true") {
        comment_track[0].pause();
        comment_track.attr("data-is-playing", "false")
    }
    else if (is_playing === "false") {
        comment_track[0].play();
        comment_track.attr("data-is-playing", "true")
    }
});