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

// 오디오 정보 업데이트
function updateAudioInfo (e) {
    var track_id = e.target.getAttribute("data-src");
    var current_time = e.target.currentTime;
    var total_time = e.target.duration;
    var track_current = document.getElementById("playtime-current-" + track_id);
    var cutter = document.getElementById("image-cutter-" + track_id);
    var back_image = document.getElementById("back-image-" + track_id).offsetWidth;
    var re_current = current_time / total_time;

    track_current.innerText = format_time(current_time);
    cutter.style.width = (back_image * re_current) + 'px'
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
    audio[0].setAttribute("data-isPlaying", "false");

    var playbtn = $('#play-btn-' + pk);
    playbtn.find('[data-fa-processed]').removeClass("fa-pause-circle");
    playbtn.find('[data-fa-processed]').addClass("fa-play-circle");

    var wrapper = $("#waveform-wrapper-" + pk);
    wrapper[0].style.opacity = null
}


// 플레이 버튼 클릭시 아이콘 변경 및 오디오 재생
// 오디오 재생 중 다른 오디오 클릭 시, 재생 중이던 오디오는 처음으로 돌아가고 정지됨.
function playAudio(id) {
    var audios = $('.audio-track');
    var wrappers = $('.waveform-wrapper');
    var play_btns = $('.play-btn');
    var audio = document.getElementById("track-audio-" + id);
    var playbtn = $('#play-btn-' + id);
    var isPlaying = audio.getAttribute('data-isPlaying');
    var wrapper = document.getElementById("waveform-wrapper-" + id);

    // 다른 재생 중인 오디오 정지
    for (var i = 0; i < audios.length; i++) {
        if (audios[i].id !== "track-audio-" + id) {
            console.log("hi");
            audios[i].pause();
            audios[i].currentTime = 0;
            audios[i].setAttribute("data-isPlaying", "false");
            wrappers[i].style.opacity = null
        }
        play_btns.find('[data-fa-processed]').removeClass("fa-pause-circle");
        play_btns.find('[data-fa-processed]').addClass("fa-play-circle");
    }

    // 재생 중이지 않으면 재생시키고 재생 버튼 변경
    if (isPlaying === "false") {
        audio.setAttribute("data-isPlaying", "true");
        audio.play();
        playbtn.find('[data-fa-processed]').removeClass("fa-play-circle");
        playbtn.find('[data-fa-processed]').addClass("fa-pause-circle");
        wrapper.style.opacity = '1'
    }
    // 재생 중이면 정지시키고 재생 버튼 변경
    else {
        audio.setAttribute("data-isPlaying", "false");
        audio.pause();
        playbtn.find('[data-fa-processed]').removeClass("fa-pause-circle");
        playbtn.find('[data-fa-processed]').addClass("fa-play-circle");
        wrapper.style.opacity = null
    }
}
