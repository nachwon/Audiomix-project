// 초 -> 분:초 로 바꿔주는 함수
function format_time (duration) {
    var min = parseInt(duration / 60);
    var sec = parseInt(duration % 60);
    if (String(min).length === 1) {
        min = "0" + min
    }
    if (String(sec).length === 1) {
        sec = "0" + sec
    }
    return min + ":" + sec
}

// 오디오 정보 실시간 업데이트
function updateAudioInfo (self) {
    var track_id = $(self).attr("data-src");
    var current_time = self.currentTime;
    var total_time = self.duration;
    var track_current = $("#playtime-current-" + track_id);
    var cutter = $("#image-cutter-" + track_id);
    var rel_current = current_time / total_time * 100;

    track_current.text(format_time(current_time));
    cutter.css("width", rel_current + '%');

    updatePlayerProgress(self)
}

// 오디오 총 길이 표시
function setTotalDuration (id) {
    var audio = document.getElementById('track-audio-' + id);
    var duration_total = document.getElementById('playtime-total-' + id);
    duration_total.innerText = format_time(audio.duration)
}

// 웨이브폼 클릭시 업데이트
function updateWaveform (e) {
    var track_id = e.target.getAttribute("data-src");
    var audio = document.getElementById("track-audio-" + track_id);
    var cutter = document.getElementById("image-cutter-" + track_id);
    var back_image = $("#back-image-" + track_id);
    var x = e.pageX - back_image.offset().left;
    var percent_position = x / back_image[0].offsetWidth;
    var rel_duration = audio.duration * percent_position;
    cutter.style.width = x + "px";
    audio.currentTime = rel_duration
}

// 재생이 끝난 경우 처음으로 다시 돌려줌
function resetWaveform (pk) {
    var audio = $("#track-audio-" + pk);
    audio[0].currentTime = 0;
    audio[0].pause();
    audio.attr("data-isPlaying", "false");

    var playbtn = $('#play-btn-' + pk);
    playbtn.find('[data-fa-processed]').removeClass("fa-pause-circle");
    playbtn.find('[data-fa-processed]').addClass("fa-play-circle");

    var wrapper = $("#waveform-wrapper-" + pk);
    wrapper.css("opacity", null)
}

// 재생하려는 트랙을 제외한 나머지 트랙들 모두 초기화
// audio-file 클래스를 audio 태그에 달아주면 등록된다.
function resetAudio(audio) {
    var audios = $('.audio-file');
    var wrappers = $('.waveform-opacity');
    var play_icons = $(".comment-play-icon");
    var track_play_icons = $(".play-btn");

    audios.each(function(index, item) {
        if (item.id !== audio.attr("id")) {
            item.pause();
            item.currentTime = 0;
        }
    });

    wrappers.each(function(index, item) {
        item.style.opacity = null
    });

    play_icons.each(function(index, item){
        $(item).find("[data-fa-processed]").removeClass("fa-pause");
        $(item).find("[data-fa-processed]").addClass("fa-play");
    });

    track_play_icons.each(function(index, item){
        $(item).find("[data-fa-processed]").removeClass("fa-pause-circle");
        $(item).find("[data-fa-processed]").addClass("fa-play-circle");
    });
}

// 플레이 누른 오디오에 loaded 속성 부여
function loadAudio(self) {
    var audio = $("#" + $(self).attr("data-target"));
    var audios = $(".audio-file");

    audios.attr("loaded", null);

    audio.attr("loaded", true)
}

// 플레이 버튼 클릭시 아이콘 변경 및 오디오 재생
// 오디오 재생 중 다른 오디오 클릭 시, 재생 중이던 오디오는 처음으로 돌아가고 정지됨.
function playAudio(pk) {
    var audio = $("[loaded]");
    var playbtn = $('#play-btn-' + pk);
    var wrapper = document.getElementById("waveform-wrapper-" + pk);
    var player_play_btn = $("#player-play-btn");

    resetAudio(audio);

    // 재생 중이지 않으면 재생시키고 재생 버튼 변경
    if (audio[0].paused) {
        audio[0].play();
        playbtn.find('[data-fa-processed]').removeClass("fa-play-circle");
        playbtn.find('[data-fa-processed]').addClass("fa-pause-circle");
        player_play_btn.find('[data-fa-processed]').removeClass("fa-play");
        player_play_btn.find('[data-fa-processed]').addClass("fa-pause");
        wrapper.style.opacity = '1'
    }
    // 재생 중이면 정지시키고 재생 버튼 변경
    else {
        audio[0].pause();
        playbtn.find('[data-fa-processed]').removeClass("fa-pause-circle");
        playbtn.find('[data-fa-processed]').addClass("fa-play-circle");
        player_play_btn.find('[data-fa-processed]').removeClass("fa-pause");
        player_play_btn.find('[data-fa-processed]').addClass("fa-play");
        wrapper.style.opacity = null;
    }
}

