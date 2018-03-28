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

    fader.each(function(index, item) {
        $(item).on("dragstart", function(e) {
            console.log(e.pageY);
            e.originalEvent.dataTransfer.setData('Text', e.pageY);
            $(item).css("pointer-events", "none")
        });

        $(item).on("drag", function(e) {
            console.log(e);
        });

        $(item).on("dragend", function() {
            $(item).css("pointer-events", "visible")
        });

        var meter_position = $(item).parent().parent().find(".meter-position-getter");
        $(document).on("dragover", function(e) {
            e.preventDefault();
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