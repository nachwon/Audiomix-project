// 플레이어 정보 업데이트 관련 함수들

// 플레이어 초기 설정
$(".soundhub-player").ready(function () {
    var indicator = $(".player-position-indicator");
    var pointer = $(".player-progress-pointer");
    var volume_control = $(".player-volume-control");
    var volume_control_popup = $(".volume-control-popup");

    // 진행바 포인터 세팅
    indicator.on("mouseenter", function () {
        pointer.animate({
            opacity: "1"
        }, 0.1)
    });
    indicator.on("mouseleave", function () {
        pointer.animate({
            opacity: "0"
        }, 0.1)
    });

    // 볼륨 컨트롤 세팅
    volume_control.on("mouseenter", function() {
        volume_control_popup.fadeIn("fast")
    });
    volume_control.on("mouseleave", function() {
        volume_control_popup.fadeOut("fast")
    });
    volume_control_popup.on("mouseenter", function() {
        $(this).fadeIn("fast")
    });
    volume_control_popup.on("mouseleave", function() {
        $(this).fadeOut("fast")
    })

});

function showPlayer() {
    var player = $(".soundhub-player");
    player.removeClass("hide-player");
}

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

    // 제목 자리
    var title;
    var instrument;

    // 작성자 자리
    var author;
    var uploaded_post;

    // 링크
    var author_link;

    // 이미지
    var post_img;

    if (target_type === "track") {
        title = target_obj.find(".track-title");
        author = target_obj.find(".track-author");
        author_link = author.parent().attr("href");
        post_img = target_obj.find(".track-post-img").attr("style");

        // 포스트 이미지
        player_post_img.attr("style", post_img);
        // 포스트 제목
        player_post_title.text(title.text());
        // 포스트 작성자
        player_post_author.text(author.text());
        // 작성자 프로필 링크
        player_author_link.attr("href", author_link)
    }
    else if (target_type === "comment") {
        instrument = target_obj.find(".comment-post-title").text();
        uploaded_post = target_obj.find(".comment-instrument").find("a.comment-uploaded-post").text();
        post_img = target_obj.find(".comment-post-img").attr("style");

        // 커맨트 트랙이 업로드된 포스트 이미지
        player_post_img.attr("style", post_img);
        // 악기
        player_post_title.text(instrument);
        // 업로드된 포스트
        player_post_author.text(uploaded_post)
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

        progress_cover.css("width", position + "%");

        playerCurrentTime();
        playerDuration();
    }
}

// 플레이어 진행바에서 오디오 탐색
function seekFromPlayer(self, e) {
    var progress_bar = $(e.target).parent();
    var progress_cover = progress_bar.find(".player-progress-cover");
    var audio = $("[loaded]");

    if (audio[0]) {
        var position = (e.pageX - progress_bar.offset().left) / $(self).width() * 100;
        var track_position = audio[0].duration * position;
        progress_cover.css("width", position + "%");
        audio[0].currentTime = track_position / 100
    }
}

// 볼륨 관련 함수

// 볼륨 컨트롤 클릭하여 볼륨 조절
function playerVolumeControl(self, e) {
    var audio = $("[loaded]");
    var indicator = $(self);
    var position = (e.pageX - indicator.offset().left);
    var volume_level_cover = $(".volume-control-bar-cover");
    var current_volume;

    // 클릭 포지션 만큼 볼륨 막대 길이 설정
    volume_level_cover.css("width", position);
    // 클릭 포지션 100 넘으면 볼륨 최대
    if (position > 100) {
        current_volume = 1;
    }
    // 클릭 포지션 10 보다 작으면 볼륨 최소
    else if (position < 10) {
        current_volume = 0;
    }
    // 나머지의 경우 클릭한 위치만큼 볼륨 설정
    else {
        current_volume = position / 100;
    }
    // 볼륨에 맞게 아이콘 변경

    audio[0].volume = current_volume;
    changeVolumeIcon(current_volume);
    // 오디오 태그에 볼륨 속성 설정
    audio.attr("volume", current_volume)
}

// 재생 시 현재 볼륨으로 플레이어 업데이트
function getCurrentVolume() {
    var audio = $("[loaded]");
    var volume_level_cover = $(".volume-control-bar-cover");
    var current_volume;
    // 뮤트 되었을 때
    if (audio.attr("muted")) {
        current_volume = 0;
    }
    // 볼륨 조절되었을 때
    else if (audio.attr("volume")) {
        current_volume = audio.attr("volume")
    }
    // 처음 재생 시
    else {
        audio.attr("volume", 1);
        current_volume = 1
    }
    volume_level_cover.css("width", (current_volume * 100) + "px");
    changeVolumeIcon(current_volume)
}

// 볼륨 크기에 따라 볼륨 아이콘 변경
function changeVolumeIcon(volume) {
    var audio = $("[loaded]");
    var volume_icon = $(".player-volume-control").find("[data-fa-processed]");
    var volume_level_cover = $(".volume-control-bar-cover");

    volume_level_cover.css("width", volume * 100);

    if (volume === 0 || audio.attr("muted")) {
        volume_icon.removeClass("fa-volume-down");
        volume_icon.removeClass("fa-volume-up");
        volume_icon.addClass("fa-volume-off")
    }
    else if (volume < 0.5) {
        volume_icon.removeClass("fa-volume-up");
        volume_icon.removeClass("fa-volume-off");
        volume_icon.addClass("fa-volume-down")
    }
    else if (volume > 0.5) {
        volume_icon.removeClass("fa-volume-down");
        volume_icon.removeClass("fa-volume-off");
        volume_icon.addClass("fa-volume-up")
    }
}

// 뮤트 토글
function muteVolumeToggle () {
    var audio = $("[loaded]");
    var volume_level_cover = $(".volume-control-bar-cover");

    // 뮤트 해제
    if (audio.attr("muted")) {
        var current_volume = audio.attr("volume");
        audio[0].volume = current_volume;
        volume_level_cover.css("width", (current_volume * 100) + "px");
        audio.attr("muted", null);
        changeVolumeIcon(current_volume)
    }
    // 뮤트
    else {
        audio[0].volume = 0;
        volume_level_cover.css("width", 0);
        audio.attr("muted", true);
        changeVolumeIcon(0)
    }
}


// 플레이 리스트 관련 함수들

// 플레이 리스트에 추가함
function addToPlaylist(self) {
    var target_obj = $("#" + $(self).data("target"));
    var target_img = target_obj.find(".track-post-img").attr("style");
    var target_title = target_obj.find(".track-title").text();
    var target_author = target_obj.find(".track-author").text();
    var target_audio_id = target_obj.find("audio").attr("id");

    var ul = $("#player-playlist");
    var li = $(".player-playlist-item");
    var list_item =
        '<li class="player-playlist-item">' +
        '<div class="playlist-item-grab-handle"></div>' +
        '<a data-target="' + target_audio_id + '" href="' + target_audio_id + '" onclick="playItem(this, event)">' +
        '<div class="player-post-img" style="'+ target_img +'"></div>' +
        '<div class="player-post-info">' +
        '<span class="player-post-title">' + target_title + '</span>' + '<br>' +
        '<span class="player-post-author">' + target_author + '</span>' +
        '</div>' +
        '</a>' +
        '</li>';

    var exists_in_playlist = false;

    li.each(function(index, item) {
        if (item.outerHTML === list_item) {
            exists_in_playlist = item.outerHTML === list_item
        }
    });

    if (!exists_in_playlist) {
        ul.prepend(list_item);
    }
    showPlayer()
}

// 플레이리스트의 아이템 재생
function playItem(self, e) {
    e.preventDefault();
    loadAudio(self);
    playAudio();
    updatePlayerPostInfo()
}