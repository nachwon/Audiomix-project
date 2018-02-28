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

// 커맨트 트랙 재생/일시정지
function playCommentTrack (pk) {
    var play_icons = $(".comment-play-icon");
    var track_play_icons = $(".play-btn");
    var comment_track = $("#comment-track-" + pk);
    var play_btn = $("#comment-play-btn-" + pk);
    var player_play_btn = $("#player-play-btn");

    // 커맨트 트랙 플레이 버튼 클릭시

    // 다른 모든 오디오 정지
    resetAudio(comment_track);

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
    if (comment_track[0].paused) {
        comment_track[0].play();
        play_btn.find("[data-fa-processed]").removeClass("fa-play");
        play_btn.find("[data-fa-processed]").addClass("fa-pause");
        player_play_btn.find('[data-fa-processed]').removeClass("fa-play");
        player_play_btn.find('[data-fa-processed]').addClass("fa-pause");
    }
    else  {
        comment_track[0].pause();
        play_btn.find("[data-fa-processed]").removeClass("fa-pause");
        play_btn.find("[data-fa-processed]").addClass("fa-play");
        player_play_btn.find('[data-fa-processed]').removeClass("fa-pause");
        player_play_btn.find('[data-fa-processed]').addClass("fa-play");
    }
}
