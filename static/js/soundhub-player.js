function getCurrentPlaying() {
    var audios = $(".audio-file");
    var player_total_duration = $("#player-total-duration");
    var player_current_time = $("#player-current-time");

    audios.each(function(index, item){
        if($(item).attr("data-isPlaying") === "true") {
            $(item).on("play", function() {
                player_total_duration.text(format_time(item.duration))
            });
            $(item).on("timeupdate", function() {
                player_current_time.text(format_time(item.currentTime));
            })
        }
    });
}