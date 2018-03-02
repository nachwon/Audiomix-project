function playerDuration() {
    var audio = $("[loaded]");
    var player_total_duration = $("#player-total-duration");
    player_total_duration.text(format_time(audio[0].duration));
}

function playerCurrentTime() {
    var audio = $("[loaded]");
    var player_current_time = $("#player-current-time");
    $(audio).on("timeupdate", function() {
        player_current_time.text(format_time(audio[0].currentTime))
    });
}


// 플레이 리스트에 추가함
function addToPlaylist(self) {
    var target_pk = $(self).data("src");
    var target_obj = $("#track-" + target_pk);
    var target_title = target_obj.data("title");
    var target_audio_id = target_obj.find("audio").attr("id");

    var ul = $("#player-playlist");
    var li = $(".player-playlist-item");
    var list_item = '<li class="player-playlist-item"><a data-target="' + target_audio_id + '" data-target-pk="' + target_pk + '" onclick="playItem(this, event)" href="' + target_audio_id + '">' + target_title + '</a></li>';

    var exists_in_playlist = false;

    li.each(function(index, item) {
        if (item.outerHTML === list_item) {
            exists_in_playlist = item.outerHTML === list_item
        }
    });

    if (exists_in_playlist) {
    }
    else {
        ul.prepend(list_item);
    }
}

// 플레이리스트 내의 아이템 하나를 재생
function playItem(self, e) {
    e.preventDefault();
    var target_pk = $(self).attr("data-target-pk");
    var audio_pk = $(self).attr("href");
    var player_audio = $("#" + audio_pk);
    player_audio.on("loadedmetadata", playerDuration(player_audio[0], true));
    loadAudio(self);
    playAudio(target_pk);
    playerCurrentTime(player_audio[0]);
    updatePlayerProgress(player_audio[0]);
    updatePlayerPostInfo()
}

// 플레이어 진행바 업데이트
function updatePlayerProgress() {
    var audio = $("[loaded]");
    if (audio[0]) {
        var progress_cover = $(".player-progress-cover");
        var current = audio[0].currentTime;
        var total = audio[0].duration;
        var position = current / total * 100;

        audio.on("timeupdate", function() {
            progress_cover.css("width", position + "%")
        });

        playerCurrentTime();
        playerDuration();
    }
}

// 재생버튼 클릭시 player 의 정보 업데이트
function updatePlayerPostInfo() {
    var audio = $("[loaded]");
    var player_post_img = $("#player-post-img");
    var player_post_title = $("#player-post-title");
    var player_post_author = $("#player-post-author");
    var player_author_link = $("#player-author-link");

    var target_obj = audio.parent();
    var target_type = target_obj.data("type");

    if (target_type === "track") {
        var title = target_obj.data("title");
        var author = target_obj.data("author");
        var author_link = target_obj.find(".track-author").parent().attr("href");
        var post_img = target_obj.find(".track-post-img").attr("style");

        // 프로필 이미지
        player_post_img.attr("style", post_img);
        // 포스트 제목
        player_post_title.text(title);
        // 포스트 작성자
        player_post_author.text(author);
        // 작성자 프로필 링크
        player_author_link.attr("href", author_link)
    }
}

