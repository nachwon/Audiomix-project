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
        volume_control_popup.css("display", "block")
    });
    volume_control.on("mouseleave", function() {
        volume_control_popup.css("display", "none")
    });
    volume_control_popup.on("mouseenter", function() {
        $(this).css("display", "block")
    });
    volume_control_popup.on("mouseleave", function() {
        $(this).css("display", "none")
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
    audio.attr("muted", null);
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
        var current_volume = Number(audio.attr("volume"));
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

// 플레이 리스트 보이기/숨기기
function togglePlaylist(action="toggle") {
    var playlist = $("#playlist-wrapper");
    if (action === "show") {
        playlist.removeClass("disappear")
    }
    else if (action === "hide") {
        playlist.addClass("disappear")
    }
    else if (action === "toggle")
        playlist.toggleClass("disappear")
}

// 플레이 리스트에 추가함
function addToPlaylist(self) {
    var target_obj = $("#" + $(self).attr("data-target"));
    var target_img = target_obj.find(".track-post-img").attr("style");
    var target_title = target_obj.find(".track-title").text();
    var target_author = target_obj.find(".track-author").text();
    var target_audio_id = target_obj.find("audio").attr("id");
    var target_duration = target_obj.find(".track-duration-total").text();

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
        '<span class="player-post-duration">' + target_duration + '</span>' +
        '</a>' +
        '<button class="playlist-item-more menu-item" data-target="' + $(self).data("target") + '" onclick="showMoreActionMenu(this)">' +
        '<span class="no-pointer-event"><i class="fas fa-ellipsis-v"></i></span>' +
        '</button>' +
        '</li>';

    var exists_in_playlist = false;


    li.each(function(index, item) {
        var existing_item = $(item).find("a").data("target");
        var to_be_added_item = $(list_item).find("a").data("target");
        if (existing_item === to_be_added_item) {
            exists_in_playlist = existing_item === to_be_added_item
        }
    });

    if (!exists_in_playlist) {
        ul.append(list_item);
        togglePlaylistItem()
    }
    showPlayer();
}

// 플레이리스트의 아이템 재생
function playItem(self, e=null) {
    if (e) {
        e.preventDefault();
    }
    loadAudio(self);
    playAudio();
    updatePlayerPostInfo();
    togglePlaylistItem()
}

// 플레이리스트의 이전/다음 아이템 재생
function playPrevNext(direction) {
    var audio = $("[loaded]");
    var target_id = audio.data("target");
    var target_obj_id = $("#" + target_id).find("audio").attr("id");
    var items = $(".player-playlist-item");
    var next_item;

    items.each(function(index, item) {
        if ($(item).find("a").data("target") === target_obj_id) {
            if (direction === 'next') {
                next_item = $(items[index + 1]).find('a');
            }
            else if (direction === 'prev') {
                next_item = $(items[index - 1]).find('a');
            }

            if (next_item.length) {
                playItem(next_item[0])
            }
        }
    });
}

// 재생 시 플레이리스트 아이템 상태 변경
function togglePlaylistItem() {
    var audio = $("[loaded]");
    var target_id = audio.data("target");
    var target_obj_id = $("#" + target_id).find("audio").attr("id");
    var playlist_lis = $(".player-playlist-item");
    var check_played;

    playlist_lis.each(function(index, item) {
        // 모든 아이템들 초기화
        $(item).removeClass("played-playlist-item");

        // 루프가 현재 재생중인 아이템에 도달하면
        if ($(item).find("a").data("target") === target_obj_id) {
            check_played = true;

            $(item).addClass("playing");
            if (audio[0].paused) {
                $(item).find(".player-post-duration").text("paused")
            }
            else {
                $(item).find(".player-post-duration").text("playing")
            }
        }

        // 현재 재생중이 아닌 아이템인 경우
        else {
            var target_audio = $("#" + $(item).find("a").data("target"));
            var duration = format_time(target_audio[0].duration);
            $(item).find(".player-post-duration").text(duration);
            $(item).removeClass("playing");

            // 현재 재생중인 아이템 이전의 아이템인 경우
            if (!check_played) {
                check_played = false;
                $(item).addClass("played-playlist-item");
            }
            else if (check_played) {
                $(item).removeClass("played-playlist-item")
            }
        }
    })
}

// 플레이리스트 아이템 세부 메뉴 보이기
function showMoreActionMenu(self) {
    var target_id = $(self).data("target");
    var target_obj = $("#" + target_id);
    var target_pk = target_obj.data("pk");
    var current_more_action_menu = $("#more-action-menu");

    // 메뉴가 나타난 상태인 경우
    if (!current_more_action_menu.hasClass("hide-menu")) {

        // 동일한 메뉴를 다시 부르면 닫기
        if (current_more_action_menu.attr("data-target") === $(self).attr("data-target")) {
            current_more_action_menu.fadeOut("fast")
                .addClass("hide-menu")
                .attr("data-target", target_id)
                .find("button").attr("onclick", "like(" + target_pk + ")");
        }
        // 다른 메뉴를 호출하면 다른 메뉴로 교체
        else {
            current_more_action_menu
                .removeClass("hide-menu")
                .attr("data-target", target_id)
                .fadeIn("fast")
                .find("button").attr("onclick", "like(" + target_pk + ")");
        }
    }
    // 메뉴가 안보이는 상태인 경우
    else {
        current_more_action_menu.removeClass("hide-menu")
            .attr("data-target", target_id)
            .fadeIn("fast")
            .find("button").attr("onclick", "like(" + target_pk + ")");
    }
}

$(document).on("click", function(e) {
    if (!$(e.target).hasClass("menu-item")) {
        $("#more-action-menu")
            .fadeOut("fast")
            .addClass("hide-menu")
    }
});