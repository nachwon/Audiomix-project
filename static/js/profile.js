$(document).ready(function() {
    // waveform 클래스를 가진 div 목록 가져옴
    var div_list = document.getElementsByClassName('waveform');
    // 목록을 순회하면서
    for (var i = 0; i < div_list.length; i++) {
        // div의 datasrc 속성의 값을 track_url 변수에 저장
        var track_url = div_list[i].getAttribute('datasrc');
        // waveform을 그려줄 각각의 div에 부여할 id값 생성
        var waveform_id = '#waveform-' + (i + 1);
        // track_url와 waveform_id를 drawTrack 함수에 전달
        drawTrack(track_url, waveform_id)
    }

    // 파일 위치 url과 waveform을 그려줄 div를 지정하는 element_id 인자를 받음
    function drawTrack(url, element_id) {
        // waveform 객체 생성
        var wavesurfer = WaveSurfer.create({
            // 대상 객체 id값(필수)
            container: element_id,
            // 막대 넓이
            barWidth: 2,
            // 막대 높이
            barHeight: 0.6,
            // 커서 이전 부분 색상
            progressColor: '#E2B026',
            // 커서 색상
            cursorColor: 'transparent',
            // 커서 이후 부분 색상
            waveColor: '#333533'
        });
        // waveform 객체 로드
        wavesurfer.load(url);
        // waveform 로딩이 끝나면 함수 실행
        wavesurfer.on("ready", function() {
            // loader를 없애주는 함수
            waveformLoader();
        });
    }

    var btn_list = document.getElementsByClassName("like-btn");
    for (var i = 0; i < btn_list.length; i++) {
        var el = btn_list[i];
        get_like_status(el);
        el.onclick = function(el) {
            like(el);
            if (this.className === "like-btn glyphicon glyphicon-heart") {
                this.className = "like-btn glyphicon glyphicon-heart-empty"
            }
            else {
                this.className = "like-btn glyphicon glyphicon-heart"
            }
        };
    }
});

// loader를 없애주는 함수
function waveformLoader() {
    // waveform-loader라는 클래스명을 가진 객체 리스트 저장
    var loader = document.getElementsByClassName('waveform-loader');

    // 리스트를 순회하면서 display 속성을 none으로 변경
    for (var i = 0; i < loader.length; i++) {
        loader[i].style.display = 'none';
    }
}

function like(el) {
    var post_pk = el.target.getAttribute('data-post-pk');
    var xhttp = new XMLHttpRequest();
    var csrf_token = $('[name=csrfmiddlewaretoken]').val();

    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 201) {
                var count = JSON.parse(xhttp.responseText).count;
                change_like_count(post_pk, count)
            }
            else if (this.status === 204) {
                var count = document.getElementById("like-count-" + post_pk).innerText;
                change_like_count(post_pk, count - 1)
            }
        }
    };

    xhttp.open("POST", "/post/" + post_pk + "/like/", true);
    xhttp.setRequestHeader('X-CSRFToken', csrf_token);
    xhttp.send({"user": "{{ request.user }}"})
}

function get_like_status(el) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (xhttp.response === "True") {
                el.className = "like-btn glyphicon glyphicon-heart"
            }
            else {
                el.className = "like-btn glyphicon glyphicon-heart-empty"
            }
        }
    };

    var pk = el.getAttribute('data-post-pk');
    xhttp.open("GET", "/post/" + pk + "/like/", true);
    xhttp.send()
}

function change_like_count(id, count) {
    document.getElementById("like-count-" + id).innerHTML = count
}