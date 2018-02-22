

// 커맨트 트랙 재생/일시정지
function playCommentTrack (pk) {
    var play_icons = $(".comment-play-icon");
    var comment_track = $("#comment-track-" + pk);
    var play_btn = $("#comment-play-btn-" + pk);
    var is_playing = comment_track.attr("data-isPlaying");
    var audios = $(".audio-file");
    var track_play_icons = $(".play-btn");

    // 커맨트 트랙 플레이 버튼 클릭시

    // 다른 모든 오디오 정지
    audios.each(function(index, item){
        item.pause();
        item.currentTime = 0;
        $(item).attr("data-isPlaying", "false");
    });
    // 커맨트 트랙 플레이 버튼 변경
    play_icons.each(function(index, item){
        $(item).find("[data-fa-processed]").removeClass("fa-pause");
        $(item).find("[data-fa-processed]").addClass("fa-play");
    });
    // 포스트 트랙 플레이 버튼 변경
    track_play_icons.each(function(index, item){
        $(item).find("[data-fa-processed]").removeClass("fa-pause-circle");
        $(item).find("[data-fa-processed]").addClass("fa-play-circle");
    });

    // 재생&일시정지 토글
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
}
