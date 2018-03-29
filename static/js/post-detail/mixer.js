var position_data;

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

    })
}

// 페이더 동작 설정
function connectFader(source, audioCtx) {
    var gainNode = audioCtx.createGain();

    source.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    var fader = $(".fader");
    var fader_chrome = document.getElementsByClassName("fader");

    // JQuery의 dataTransfer 에러 때문에 바닐라 자바스크립트로 작성
    for (var i = 0; i < fader_chrome.length; i++) {
        fader_chrome[i].addEventListener("dragstart", function(e) {
            e.dataTransfer.setData('text', e.offsetY);
            position_data = e.offsetY;
            $(fader_chrome[i]).css("pointer-events", "none");

            var crt = document.getElementById("ghost");
            crt.style.display = "none";
            e.dataTransfer.setDragImage(crt, 10000, 10000);
        });
    }

    document.addEventListener("dragover", function(e) {
        for (var i = 0; i < fader_chrome.length; i++) {
            var data = e.dataTransfer.getData('text');
            if (data === "") {
                data = position_data;
            }
            var volume = setFaderPosition(e, fader_chrome[i], data);
            var gain_value = 1.25 - volume / 200;
            var fader_value = Math.round((gain_value - 1) * 100) / 10;

            if (fader_value === -10) {
                fader_value = "-\u221E";
            }

            gainNode.gain.value = gain_value;
            $(".fader-value").text(fader_value);
        }
    });

    fader.each(function(index, item) {
        $(item).on("dragend", function() {
            $(item).css("pointer-events", "visible");
        });
    });
}

// 페이더 드래그 시 위치 변경
function setFaderPosition(e, fader, data) {
    var meter_position = $(fader).parent();

    var position = parseFloat(e.pageY) - parseFloat(meter_position.offset().top) - parseFloat(data);

    if (position > 250) {
        position = 250
    }
    else if (position < 0) {
        position = 0
    }
    $(fader).css("top", position + "px");

    return position
}