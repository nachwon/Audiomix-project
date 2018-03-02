// 커맨트 트랙 진행사항 실시간 업데이트
function updateCommentTrack (event) {
    var audio =  event.target;
    var target_obj = $(audio).parent();
    var progress_bar = target_obj.find(".progress-bar-cover");
    var bar_width = audio.currentTime / audio.duration * 100;
    progress_bar.css("width", bar_width + "%");

    // 현재 재생 시간 업데이트
    var current_time_span = target_obj.find(".comment-track-current-time");
    current_time_span.text(format_time(audio.currentTime));
}


// 커맨트 트랙 탐색
function seekCommentTrack (e) {
    var target_obj = $(e.target).parent().parent();
    var indicator = target_obj.find(".position-indicator");
    var click_position = e.pageX - indicator.offset().left;
    var rel_position = click_position / indicator.width();
    var audio = target_obj.find("audio");
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
