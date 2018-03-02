// 플레이어 정보 업데이트 관련 함수들

// 현재 재생중인 트랙 총 길이 업데이트
function playerDuration() {
    var audio = $("[loaded]");
    var player_total_duration = $("#player-total-duration");
    player_total_duration.text(format_time(audio[0].duration));
}

// 현재 재생중인 트랙 현재 위치 업데이트
function playerCurrentTime() {
    var audio = $("[loaded]");
    var player_current_time = $("#player-current-time");
    $(audio).on("timeupdate", function() {
        player_current_time.text(format_time(audio[0].currentTime))
    });
}

// 재생버튼 클릭시 플레이어의 트랙 정보 업데이트
function updatePlayerPostInfo() {
    var audio = $("[loaded]");
    var player_post_img = $("#player-post-img");
    var player_post_title = $("#player-post-title");
    var player_post_author = $("#player-post-author");
    var player_author_link = $("#player-author-link");

    var target_obj = audio.parent();
    var target_type = target_obj.data("type");

    if (target_type === "track") {
        var title = target_obj.find(".track-title");
        var author = target_obj.find(".track-author");
        var author_link = author.parent().attr("href");
        var post_img = target_obj.find(".track-post-img").attr("style");

        // 프로필 이미지
        player_post_img.attr("style", post_img);
        // 포스트 제목
        player_post_title.text(title.text());
        // 포스트 작성자
        player_post_author.text(author.text());
        // 작성자 프로필 링크
        player_author_link.attr("href", author_link)
    }
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

// 플레이 리스트 관련 함수들

// 플레이 리스트에 추가함
function addToPlaylist(self) {
    var target_obj = $("#" + $(self).data("target"));
    var target_title = target_obj.find(".track-title").text();
    var target_audio_id = target_obj.find("audio").attr("id");

    var ul = $("#player-playlist");
    var li = $(".player-playlist-item");
    var list_item = '<li class="player-playlist-item"><a data-target="' + target_audio_id + '" href="' + target_audio_id + '" onclick="playItem(this, event)">' + target_title + '</a></li>';

    var exists_in_playlist = false;

    li.each(function(index, item) {
        if (item.outerHTML === list_item) {
            exists_in_playlist = item.outerHTML === list_item
        }
    });

    if (!exists_in_playlist) {
        ul.prepend(list_item);
    }
}

function playItem(self, e) {
    e.preventDefault();
    loadAudio(self);
    playAudio();
    updatePlayerPostInfo()
}