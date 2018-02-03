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

var play_btns = $('.play-btn');
var audios = $('.audio-track');

function Audio(src) {
    this.src = src;
    this.isPlaying = false;
}

function playAudio(id) {
    for (var i = 0; i < audios.length; i++) {
        if (audios[i].id !== "track-audio-" + id) {
            audios[i].pause();
            audios[i].currentTime = 0;
            audios[i].setAttribute("data-isPlaying", "false")
        }

    }

    var audio = document.getElementById('track-audio-' + id);
    var isPlaying = audio.getAttribute('data-isPlaying');

    if (isPlaying === "false") {
        audio.setAttribute("data-isPlaying", "true");
        audio.play()
    }
    else {
        audio.setAttribute("data-isPlaying", "false");
        audio.pause()
    }
}
