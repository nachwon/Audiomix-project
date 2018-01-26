// waveform 클래스를 가진 div 목록 가져옴
var div_list = document.getElementsByClassName('waveform');
var surfer_list = [];

// 목록을 순회하면서
for (var i = 0; i < div_list.length; i++) {
    // div의 datasrc 속성의 값을 track_url 변수에 저장
    var track_url = div_list[i].getAttribute('datasrc');
    // waveform을 그려줄 각각의 div에 부여할 id값 생성
    var waveform_id = '#waveform-' + (i + 1);
    // waveform 객체 생성
    var wavesurfer = WaveSurfer.create({
        // 대상 객체 id값(필수)
        container: waveform_id,
        // 막대 넓이
        barWidth: 2,
        // 막대 높이
        barHeight: 0.6,
        // 커서 이전 부분 색상
        progressColor: '#E2B026',
        // 커서 색상
        cursorColor: 'transparent',
        // 커서 이후 부분 색상
        waveColor: '#333533',
        // 스크롤바 숨기기
        hideScrollbar: true
    });

    // waveform 객체 로드
    wavesurfer.load(track_url);
    // 로드된 wavesurfer 객체를 리스트에 저장
    surfer_list.push(wavesurfer);

    //
    wavesurfer.on("ready", function() {
        // loader를 없애주는 함수
        waveformLoader();
        playBtnLoader();
    });
}

// 플레이 버튼 설정
var play_btn_list = $(".play-btn");
var waveform_list = $(".waveform-wrapper");
for (i = 0; i < play_btn_list.length; i++) {
    play_btn_list[i].onclick = (function (j) {
        return function () {
            $(this)
                .find('[data-fa-processed]')
                .toggleClass('fas fa-pause-circle fa-3x')
                .toggleClass('fas fa-play-circle fa-3x');

            if (surfer_list[j].isPlaying()) {
                surfer_list[j].pause();
                waveform_list[j].style.opacity = null

            }
            else {
                surfer_list[j].play();
                waveform_list[j].style.opacity = 1
            }
        }
    }(i));

    surfer_list[i].on('finish', function (j) {
        return function () {
            $('#play-btn-' + (j + 1))
                .find('[data-fa-processed]')
                .toggleClass('fas fa-play-circle');
        }
    }(i))
}

// Track 길이 설정
for (i = 0; i < surfer_list.length; i++) {
    surfer_list[i].on('ready', function (j) {
        return function () {
            var total = parseInt(surfer_list[j].getDuration());
            document.getElementById("playtime-total-" + (j + 1)).innerText = format_time(total);
        }
    }(i));

    surfer_list[i].on('audioprocess', function(j) {
        return function () {
            var current = parseInt(surfer_list[j].getCurrentTime());
            document.getElementById("playtime-current-" + (j + 1)).innerText = format_time(current);
        }
    }(i))
}

function format_time (duration) {
    var min = parseInt(duration/60);
    var sec = parseInt(duration%60);
    if (String(min).length === 1) {
        min = "0" + min
    }
    if (String(sec).length === 1) {
        sec = "0" + sec
    }
    return min + ":" + sec
}

// loader를 없애주는 함수
function waveformLoader() {
    // waveform-loader라는 클래스명을 가진 객체 리스트 저장
    var loader = document.getElementsByClassName('waveform-loader');

    // 리스트를 순회하면서 display 속성을 none으로 변경
    for (var i = 0; i < loader.length; i++) {
        loader[i].style.display = 'none';
    }
}

function playBtnLoader() {
    var loader = $('.play-btn-loader');
    var playbtn = $('.play-btn');

    for (var i = 0; i < loader.length; i++) {
        loader[i].style.display = 'none';
        playbtn[i].style.display = 'inline-block';
    }
}