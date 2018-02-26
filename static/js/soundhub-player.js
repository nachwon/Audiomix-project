function getCurrentPlaying() {
    var audios = $(".audio-file");
    var player_current_time = $("#player-current-time");

    audios.each(function(index, item){
        if($(item).attr("data-isPlaying") === "true") {
            $(item).on("play", function() {
                console.log(item.id + "playing!!");
                player_current_time.text(format_time(item.duration))
            })
        }
    });
}