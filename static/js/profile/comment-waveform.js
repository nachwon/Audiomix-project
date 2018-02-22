// 커맨트 트랙 진행사항 실시간 업데이트
function updateCommentTrackInfo (event) {
    var audio =  event.target;
    var pk = $(audio).data("comment-pk");
    var progress_bar = $("#progress-bar-cover-" + pk);
    var bar_width = audio.currentTime / audio.duration * 100;
    progress_bar.css("width", bar_width + "%")
}

// 커맨트 트랙 탐색
function seekCommentTrack (event) {
    var el = event.target;
    var pk = $(el).data("comment-pk");
    var click_position = event.pageX - $(el).offset().left;
    var rel_position = click_position / $(el).width();
    var audio = $("#comment-track-" + pk);
    var total_duration = audio[0].duration;

    audio[0].currentTime = total_duration * rel_position
}

// 마우스 오버시 탐색 위치 미리보기
function preSeekCommentTrack (event) {
    var el = event.target;
    var pk = $(el).data("comment-pk");
    var hover_position = event.pageX - $(el).offset().left;
    var rel_position = hover_position / $(el).width() * 100;
    var preseeker = $('#progress-bar-preseeker-' + pk);

    preseeker.css("width", rel_position + "%")
}

function resetSeekCommentTrack (event) {
    var el = event.target;
    var pk = $(el).data("comment-pk");
    var preseeker = $('#progress-bar-preseeker-' + pk);
    preseeker.css("width", 0)
}





// 커맨트 트랙 재생/일시정지
function playCommentTrack (pk) {
    var play_icons = $(".comment-play-icon");
    var track_play_icons = $(".play-btn");
    var comment_track = $("#comment-track-" + pk);
    var play_btn = $("#comment-play-btn-" + pk);
    var is_playing = comment_track.attr("data-isPlaying");
    var audios = $(".audio-file");

    // 커맨트 트랙 플레이 버튼 클릭시

    // 다른 모든 오디오 정지
    audios.each(function(index, item){
        if (item.id !== comment_track[0].id) {
            item.pause();
            item.currentTime = 0;
            $(item).attr("data-isPlaying", "false");
        }
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
