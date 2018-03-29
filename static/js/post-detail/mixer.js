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

        connectFader(source, audioCtx, index);
        connectPanner(source, audioCtx);

    })
}

function connectPanner(source, audioCtx) {

    var panner = audioCtx.createPanner();
    panner.panningModel = 'HRTF';
    panner.distanceModel = 'linear';
    panner.refDistance = 1;
    panner.maxDistance = 10000;
    panner.rolloffFactor = 1;
    panner.coneInnerAngle = 360;
    panner.coneOuterAngle = 0;
    panner.coneOuterGain = 0;

    if(panner.orientationX) {
        panner.orientationX.value = 1;
        panner.orientationY.value = 0;
        panner.orientationZ.value = 0;
    } else {
        panner.setOrientation(1,0,0);
    }

    var listener = audioCtx.listener;

    if(listener.forwardX) {
        listener.forwardX.value = 0;
        listener.forwardY.value = 0;
        listener.forwardZ.value = -1;
        listener.upX.value = 0;
        listener.upY.value = 1;
        listener.upZ.value = 0;
    } else {
        listener.setOrientation(0,0,-1,0,1,0);
    }


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
function connectFader(source, audioCtx, index) {
    var gainNode = audioCtx.createGain();

    source.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    var fader = document.getElementsByClassName("fader");

    // 페이더에서 마우스 다운 시
    $(fader[index]).on("mousedown", function(e) {
        // 요소내에서 마우스 다운된 위치의 Y축 좌표 값 저장
        var offsetY = e.offsetY;

        // 포인터 이벤트 없애줌
        $(fader[index]).css("pointer-events", "none");

        // 페이지 전체에 대해
        $(document)
            // mousemove 이벤트 등록해서 Y 축 좌표값에 따라 페이더 이동 및 gainNode gain값 조절
            .on("mousemove", function(e) {
                var volume = setFaderPosition(e, fader[index], offsetY);
                var gain_value = 1.25 - volume / 200;

                gainNode.gain.value = gain_value;

                var fader_value = Math.round((gain_value - 1) * 1000) / 100;
                if (fader_value > 0) {
                    fader_value = "+" + fader_value;
                }
                else if (fader_value === -10) {
                    fader_value = "-\u221E"
                }
                var fader_value_display = $(".fader").parents(".channel-wrapper").find(".fader-value");

                fader_value_display.text(fader_value);
            })
            // 마우스를 떼면 movsemove 이벤트 제거하고 페이더의 포인터 이벤트 원상복구
            .on("mouseup", function() {
                $(document).off("mousemove");
                $(fader[index]).css("pointer-events", "visible");
            });
    });
}

// 페이더 드래그 시 위치 변경
function setFaderPosition(e, fader, offsetY) {
    var meter_position = $(fader).parent();

    var position = parseFloat(e.pageY) - parseFloat(meter_position.offset().top) - parseFloat(offsetY);

    if (position > 250) {
        position = 250
    }
    else if (position < 0) {
        position = 0
    }
    $(fader).css("top", position + "px");

    return position
}