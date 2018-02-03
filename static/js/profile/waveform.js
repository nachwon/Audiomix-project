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

var tracks = $('.track-obj');
var play_btns = $('.play-btn');
var audios = $('.audio-track');
var wrappers = $('.waveform-wrapper');

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

function setTotalDuration (id) {
    var audio = document.getElementById('track-audio-' + id);
    var duration_total = document.getElementById('playtime-total-' + id);
    duration_total.innerText = format_time(audio.duration)
}

for (var i = 0; i < tracks.length; i++) {
    var track_audio = tracks[i].getElementsByTagName("audio");

    track_audio[0].addEventListener("timeupdate", updateAudioInfo, false)
}

// 플레이 버튼 클릭시 아이콘 변경 및 오디오 재생
// 오디오 재생 중 다른 오디오 클릭 시, 재생 중이던 오디오는 처음으로 돌아가고 정지됨.
function playAudio(id) {
    var audio = document.getElementById("track-audio-" + id);
    var playbtn = $('#play-btn-' + id);
    var isPlaying = audio.getAttribute('data-isPlaying');
    var wrapper = document.getElementById("waveform-wrapper-" + id);

    for (var i = 0; i < audios.length; i++) {
        if (audios[i].id !== "track-audio-" + id) {
            audios[i].pause();
            audios[i].currentTime = 0;
            audios[i].setAttribute("data-isPlaying", "false");
            wrappers[i].style.opacity = '0.5'
        }
        play_btns.find('[data-fa-processed]').removeClass("fa-pause-circle");
        play_btns.find('[data-fa-processed]').addClass("fa-play-circle");

    }

    if (isPlaying === "false") {
        audio.setAttribute("data-isPlaying", "true");
        audio.play();
        playbtn.find('[data-fa-processed]').removeClass("fa-play-circle");
        playbtn.find('[data-fa-processed]').addClass("fa-pause-circle");
        wrapper.style.opacity = '1'
    }
    else {
        audio.setAttribute("data-isPlaying", "false");
        audio.pause();
        playbtn.find('[data-fa-processed]').removeClass("fa-pause-circle");
        playbtn.find('[data-fa-processed]').addClass("fa-play-circle");
        wrapper.style.opacity = '0.5'
    }
}
