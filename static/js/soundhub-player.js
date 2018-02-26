function getCurrentPlaying() {
    var audios = $(".audio-file");
    audios.each(function(index, item){
        if($(item).attr("data-isPlaying") === "true") {
            console.log(item)
        }
    });

}