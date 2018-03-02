// 커맨트 트랙 진행사항 실시간 업데이트
function updateCommentTrack (event) {
    var audio =  event.target;
    var pk = $(audio).data("comment-pk");
    var progress_bar = $("#progress-bar-cover-" + pk);
    var bar_width = audio.currentTime / audio.duration * 100;
    progress_bar.css("width", bar_width + "%");

    // 현재 재생 시간 업데이트
    var current_time_span = $("#comment-track-current-duration-" + pk);
    current_time_span[0].innerText = format_time(audio.currentTime);

    // player 업데이트
    updatePlayerProgress(audio);
}

// 재생 끝났을 때 오디오 탐색 리셋
function endCommentTrack (event) {
    var audio =  event.target;
    var pk = $(audio).data("comment-pk");
    var progress_bar = $("#progress-bar-cover-" + pk);
    var play_btn = $("#comment-play-btn-" + pk);
    // 진행바 초기화
    progress_bar.css("width", 0);
    // 아이콘 변경
    play_btn.find("[data-fa-processed]").removeClass("fa-pause");
    play_btn.find("[data-fa-processed]").addClass("fa-play");
    // 오디오 탐색 초기화
    $(audio).attr("data-isPlaying", "false");
    audio.currentTime = 0
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

// 마우스가 나가면 탐색 미리보기 제거
function resetSeekCommentTrack (event) {
    var el = event.target;
    var pk = $(el).data("comment-pk");
    var preseeker = $('#progress-bar-preseeker-' + pk);
    preseeker.css("width", 0)
}

//
function getCommentTrackTotalDuration(event) {
    var audio =  event.target;
    var pk = $(audio).data("comment-pk");
    var total_duration_span = $("#comment-track-total-duration-" + pk);
    total_duration_span.text(format_time(audio.duration));
}
