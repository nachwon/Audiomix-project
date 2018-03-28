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
            e.dataTransfer.setData('Text', e.pageY);
            $(fader_chrome[i]).css("pointer-events", "none");
        })
    }

    fader.each(function(index, item) {
        $(item).on("dragend", function() {
            $(item).css("pointer-events", "visible");
        });

        var meter_position = $(item).parent().parent().find(".meter-position-getter");
        $(document).on("dragover", function(e) {
            var position = e.pageY - meter_position.offset().top;
            if (position > 250) {
                position = 250
            }
            else if (position < 0) {
                position = 0
            }
            $(item).css("top", position + "px")
        });
    });
}