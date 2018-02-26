var player_play_btn = $("#player-play-btn");

function getCurrentPlaying(self) {
    var target_id = $(self).data("target");
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
            });

            player_play_btn.attr("data-target", target_id);
        }
    });
}


function playerBtn(self) {
    if ($(self).attr("data-target") !== null) {
        var target = $(self).attr("data-target");
        var target_audio = $("#" + target);
        var track_btns = $(".play-btn");
        var comment_btns = $(".comment-play-icon");
        var player_play_btn = $("#player-play-btn");

        if (target_audio.attr("data-isPlaying") === "false") {
            // 재생
            target_audio[0].play();
            target_audio.attr("data-isPlaying", "true");

            track_btns.each(function(index, item) {
                if ($(item).attr("data-target") === target) {
                    $(item).find("[data-fa-processed]").addClass("fa-pause-circle");
                    $(item).find("[data-fa-processed]").removeClass("fa-play-circle");
                }
            });
            comment_btns.each(function(index, item) {
                if ($(item).attr("data-target") === target) {
                    $(item).find("[data-fa-processed]").addClass("fa-pause");
                    $(item).find("[data-fa-processed]").removeClass("fa-play");
                }
            })
        }
        else if (target_audio.attr("data-isPlaying") === "true") {
            // 일시정지
            target_audio[0].pause();
            target_audio.attr("data-isPlaying", "false");

            track_btns.each(function(index, item) {
                if ($(item).attr("data-target") === target) {
                    $(item).find("[data-fa-processed]").removeClass("fa-pause-circle");
                    $(item).find("[data-fa-processed]").addClass("fa-play-circle");
                }
            });
            comment_btns.each(function(index, item) {
                if ($(item).attr("data-target") === target) {
                    $(item).find("[data-fa-processed]").removeClass("fa-pause");
                    $(item).find("[data-fa-processed]").addClass("fa-play");
                }
            })
        }
    }
}