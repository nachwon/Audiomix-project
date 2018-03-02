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
    var target_obj = $(self).parent();
    var current_time = self.currentTime;
    var total_time = self.duration;
    var track_current = target_obj.find(".track-duration-current");
    var cutter = target_obj.find(".cutter");
    var rel_current = current_time / total_time * 100;

    track_current.text(format_time(current_time));
    cutter.css("width", rel_current + '%');
}

// 오디오 총 길이 표시
function setTotalDuration (self) {
    var target_obj = $(self).parent();
    var audio = target_obj.find("audio");
    var duration_total = target_obj.find(".track-duration-total");
    duration_total.text(format_time(audio[0].duration))
}

// 웨이브폼 클릭시 업데이트
function seekTrack (e) {
    var target_obj = $(e.target).parent().parent();
    var audio = target_obj.find("audio");
    var cutter = target_obj.find(".cutter");
    var back_image = target_obj.find(".back-image");
    var x = e.pageX - back_image.offset().left;
    var percent_position = x / back_image[0].offsetWidth;
    var rel_duration = audio[0].duration * percent_position;
    cutter.css("width", x + "px");
    audio[0].currentTime = rel_duration
}

// 재생이 끝난 경우 처음으로 다시 돌려줌
function resetWaveform (self) {
    var audio = $(self);

    audio[0].currentTime = 0;
    audio[0].pause();

    toggleBtn(audio, "off");
    toggleOpacity(audio, "off")

}

// 플레이 누른 오디오에 loaded 속성 부여
function loadAudio(self) {
    var audio = $("#" + $(self).attr("data-target"));
    var audios = $(".audio-file");

    audios.attr("loaded", null);

    audio.attr("loaded", true)
}

// 플레이 버튼 클릭시 아이콘 변경 및 오디오 재생
// 오디오 재생 중 다른 오디오 클릭 시, 재생 중이던 오디오는 일시 정지됨.
function playAudio() {
    var audio = $("[loaded]");
    var audios = $(".audio-file");

    if (audio[0].paused) {
        // 모든 오디오 일시정지
        audios.each(function(index, item) {
            toggleBtn($(item), "off");
            toggleOpacity($(item), "off");
            item.pause()
        });
        // 로드된 오디오 재생
        audio[0].play();
        toggleBtn(audio, "on");
        toggleOpacity(audio, "on")
    }
    else {
        // 로드된 오디오 일시정지
        audio[0].pause();
        toggleBtn(audio, "off");
        toggleOpacity(audio, "off")
    }
}

// 재생 버튼 토글
function toggleBtn(audio, status) {
    var target_obj = audio.parent();
    var target_type = target_obj.data("type");
    var player_play_btn = $("#player-play-btn");
    if (target_type === "track") {
        var play_btn = target_obj.find(".play-btn");
        if (status === "on") {
            play_btn.find('[data-fa-processed]').removeClass("fa-play-circle");
            play_btn.find('[data-fa-processed]').addClass("fa-pause-circle");
            player_play_btn.find('[data-fa-processed]').removeClass("fa-play");
            player_play_btn.find('[data-fa-processed]').addClass("fa-pause");
        }
        else if (status === "off") {
            play_btn.find('[data-fa-processed]').removeClass("fa-pause-circle");
            play_btn.find('[data-fa-processed]').addClass("fa-play-circle");
            player_play_btn.find('[data-fa-processed]').removeClass("fa-pause");
            player_play_btn.find('[data-fa-processed]').addClass("fa-play");
        }
    }
}

// waveform 투명도 토글
function toggleOpacity(audio, status) {
    var target_obj = audio.parent();
    var target_type = target_obj.data("type");
    if (target_type === "track") {
        var wrapper = target_obj.find(".waveform-wrapper");

        if (status === "on") {
            wrapper.css("opacity", "1")
        }
        else if (status === "off") {
            wrapper.removeAttr("style")
        }
    }
}
