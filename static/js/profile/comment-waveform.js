var comment_obj = $(".comment-obj");

// 커맨트 트랙 재생/일시정지
comment_obj.find(".comment-play-icon").on("click", function () {
    var pk = $(this).attr("data-comment-pk");
    var comment_track = $("#comment-track-" + pk);
    var play_btn = $("#comment-play-btn-" + pk);
    var is_playing = comment_track.attr("data-isPlaying");

    if (is_playing === "true") {
        comment_track[0].pause();
        comment_track.attr("data-isPlaying", "false");
        play_btn.find("[data-fa-processed]").removeClass("fa-pause");
        play_btn.find("[data-fa-processed]").addClass("fa-play");
    }
    else if (is_playing === "false") {
        comment_track[0].play();
        comment_track.attr("data-isPlaying", "true");
        play_btn.find("[data-fa-processed]").removeClass("fa-play");
        play_btn.find("[data-fa-processed]").addClass("fa-pause");
    }
});