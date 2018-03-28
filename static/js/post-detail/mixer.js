var position_data;

$(document).ready(function() {
    // loadMixer();
    connectFader();
});

function loadMixer() {
    var channels = $(".channel");
    channels.each(function(index, item) {
        var audio = $("#" + $(item).attr("data-target-audio"))[0];
        var AudioContext = window.AudioContext || window.webkitAudioContext;
        var audioCtx = new AudioContext();

        var source = audioCtx.createMediaElementSource(audio);

    })
}

function connectFader() {
    var fader = $(".fader");
    var fader_chrome = document.getElementsByClassName("fader");

    // JQuery의 dataTransfer 에러 때문에 바닐라 자바스크립트로 작성
    for (var i = 0; i < fader_chrome.length; i++) {
        fader_chrome[i].addEventListener("dragstart", function(e) {
            e.dataTransfer.setData('text', e.offsetY);
            position_data = e.offsetY;
            $(fader_chrome[i]).css("pointer-events", "none");
        });
    }

    document.addEventListener("dragover", function(e) {
        for (var i = 0; i < fader_chrome.length; i++) {
            var data = e.dataTransfer.getData('text');
            if (data === "") {
                data = position_data;
            }
            setFaderPosition(e, fader_chrome[i], data)
        }
    });

    fader.each(function(index, item) {
        $(item).on("dragend", function() {
            $(item).css("pointer-events", "visible");
        });
    });
}

function setFaderPosition(e, fader, data) {
    var meter_position = $(fader).parent();

    var position = parseFloat(e.pageY) - parseFloat(meter_position.offset().top) - parseFloat(data);

    if (position > 250) {
        position = 250
    }
    else if (position < 0) {
        position = 0
    }
    $(fader).css("top", position + "px")
}