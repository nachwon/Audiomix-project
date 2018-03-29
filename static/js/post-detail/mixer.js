var fader_Y_position;
var panner_X_position;

$(document).ready(function() {
    loadMixer();
});

function loadMixer() {
    var channels = $(".channel");
    channels.each(function(index, item) {
        var audio = $("#" + $(item).attr("data-target-audio"))[0];
        var AudioContext = window.AudioContext || window.webkitAudioContext;
        var audioCtx = new AudioContext();

        var source = audioCtx.createMediaElementSource(audio);

        connectFader(source, audioCtx);
        connectPanner(source, audioCtx);

    })
}

function connectPanner(source, audioCtx) {
    var panner = audioCtx.createPanner();

    var pan_slider = $(".pan-slider");

    for (var i = 0; i < pan_slider.length; i++) {
        pan_slider[i].addEventListener("dragstart", function(e) {
            $(this).attr("drag", "panner");
            e.dataTransfer.setData("text", e.offsetX);
            panner_X_position = e.offsetX;
            $(this). css("pointer-events", "none");
        });

        pan_slider[i].addEventListener("dragend", function() {
            $(this).css("pointer-events", "visible");
            $(this).attr("drag", null);
        })
    }

    document.addEventListener("dragover", function(e) {
        if ($("[drag='panner']").length === 1) {
            for (var i = 0; i < pan_slider.length; i++) {
                // 파이어폭스의 경우 getData로 X축 좌표 가져옴.
                var offsetX = e.dataTransfer.getData('text');
                // 크롬의 경우 전역변수에서 가져옴.
                if (offsetX === "") {
                    offsetX = panner_X_position;
                }
                var panner_value = setPannerPosition(e, pan_slider[i], offsetX);

            }
        }
    });
}

function setPannerPosition(e, pan_slider, offsetX) {
    var panner = $(pan_slider).parent();

    var position = parseFloat(e.pageX) - parseFloat(panner.offset().left) - parseFloat(offsetX);

    if (position < 0) {
        position = 0;
    }
    else if (position > 60) {
        position = 60;
    }

    $(pan_slider).css("left", position + "px");

    return position
}

// 페이더 동작 설정
function connectFader(source, audioCtx) {
    var gainNode = audioCtx.createGain();

    source.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    var fader = document.getElementsByClassName("fader");

    // JQuery의 dataTransfer 에러 때문에 바닐라 자바스크립트로 작성
    for (var i = 0; i < fader.length; i++) {
        // 각 페이더에 드레그스타트 이벤트 등록
        fader[i].addEventListener("dragstart", function(e) {

            $(this).attr("drag", "fader");

            // 드레그시 페이더 내에서의 Y축 좌표값 전달
            e.dataTransfer.setData('text', e.offsetY);
            // 크롬은 dataTransfer가 작동을 안함. 따라서 전역변수를 이용함.
            fader_Y_position = e.offsetY;
            // 드레그시작한 순간 페이더의 포인터 이벤트 제거
            $(this).css("pointer-events", "none");

            // 드레그 고스트이미지 제거
            var crt = document.getElementById("ghost");
            // 크롬: 디스플레이 속성 값을 none으로
            crt.style.display = "none";
            // 파이어폭스: 고스트이미지를 화면 밖으로 보냄
            e.dataTransfer.setDragImage(crt, 10000, 10000);
        });

        // 드레그 끝난 경우 포인터 이벤트 원상복귀
        fader[i].addEventListener("dragend" ,function() {
            $(this).css("pointer-events", "visible");
            $(this).attr("drag", null);
        });
    }

    // 페이지 전체에 드레그오버 이벤트 등록
    document.addEventListener("dragover", function(e) {
        if ($("[drag='fader']").length === 1) {
            for (var i = 0; i < fader.length; i++) {
                // 파이어폭스의 경우 getData로 Y축 좌표 가져옴.
                var offsetY= e.dataTransfer.getData('text');
                // 크롬의 경우 전역변수에서 가져옴.
                if (offsetY=== "") {
                    offsetY= fader_Y_position;
                }
                // 페이더 위치에 따른 볼륨 값을 리턴
                var volume = setFaderPosition(e, fader[i], offsetY);
                // 볼륨 값 스케일링: 기본값 1
                var gain_value = 1.25 - volume / 200;
                // 믹서에서 보여줄 페이더 값: 기본값 0
                var fader_value = Math.round((gain_value - 1) * 100) / 10;

                // 양수일 경우 + 표시
                if (fader_value > 0) {
                    fader_value = "+" + fader_value;
                }
                // -10 데시벨이면 무한대 표시
                else if (fader_value === -10) {
                    fader_value = "-\u221E";
                }

                // 게인노드 값 설정
                gainNode.gain.value = gain_value;
                // 페이더 값 표시
                $(".fader-value")[i].innerText= fader_value;
            }
        }
    });
}

// 페이더 드래그 시 위치 변경
function setFaderPosition(e, fader, offsetX) {
    var meter_position = $(fader).parent();

    var position = parseFloat(e.pageY) - parseFloat(meter_position.offset().top) - parseFloat(offsetX);

    if (position > 250) {
        position = 250
    }
    else if (position < 0) {
        position = 0
    }
    $(fader).css("top", position + "px");

    return position
}