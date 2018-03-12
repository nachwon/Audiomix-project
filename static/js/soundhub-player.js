// 사운드허브 플레이어

// 플레이어 재생
// 플레이어에서 음원 재생 시 (이전/다음 트랙 재생, 플레이리스트에서 재생 등 일시정지 후 다시 재생을 제외한 모든 재생) 초기화 시킨 다음 처음부터 플레이 함.
// 플레이어가 아닌 트랙 목록에서 직접 재생 시 서로 다른 트랙을 재생할 경우 각각의 트랙은 일시정지됨. 플레이어는 현재 플레이 중인 트랙을 표시하도록 업데이트 됨.

// 플레이리스트 항목 삭제
// 플레이리스트에서 플레이 중이던 항목을 삭제시 리스트의 다음 항목을 처음부터 재생
// 플레이리스트에서 일시정지 중이던 항목을 삭제시 다음 항목을 로드만 함
// 마지막 항목을 삭제한 경우 플레이어 초기화





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

// 플레이어 초기화
function resetPlayer() {
    var audio = $("[loaded]");
    var player_post_img = $("#player-post-img");
    var player_post_title = $("#player-post-title");
    var player_post_author = $("#player-post-author");
    var player_author_link = $("#player-author-link");
    var player_current_time = $("#player-current-time");
    var player_total_duration = $("#player-total-duration");

    player_post_img.attr("style", "background-image: url(/static/img/default-post-img.png)");
    player_post_title.text("Audio Track");
    player_post_author.text("Not Loaded");
    player_author_link.attr("href", "");
    player_current_time.text("00:00");
    player_total_duration.text("00:00");

    audio.attr("loaded", null)
}

// 플레이어 나타내기
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
        post_img = target_obj.find(".track-post-img").attr("src");

        // 포스트 이미지
        player_post_img.attr("src", post_img);
        // 포스트 제목
        player_post_title.text($(title[0]).text());
        // 포스트 작성자
        player_post_author.text($(author[0]).text());
        // 작성자 프로필 링크
        player_post_author.attr("href", author_link)
    }
    else if (target_type === "comment") {
        instrument = target_obj.find(".comment-post-title").text();
        uploaded_post = target_obj.find(".comment-instrument").find("a.comment-uploaded-post").text();
        post_img = target_obj.find(".comment-post-img").attr("style");

        // 커맨트 트랙이 업로드된 포스트 이미지
        player_post_img.attr("src", post_img);
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
function togglePlaylist() {
    var playlist = $("#playlist-wrapper");
    playlist.toggleClass("disappear")
}

// 플레이 리스트에 추가함
function addToPlaylist(self) {
    var target_obj = $("#" + $(self).attr("data-target"));
    var target_img = target_obj.find(".track-post-img").attr("src");
    var target_title = target_obj.find(".track-title").text();
    var target_author = target_obj.find(".track-author").text();
    var target_audio_id = target_obj.find("audio").attr("id");
    var target_duration = target_obj.find(".track-duration-total").text();

    var ul = $("#player-playlist");
    var li = $(".player-playlist-item");
    var list_item =
        '<li class="player-playlist-item" data-target="' + target_obj.attr("id") + '">' +
        '<div class="playlist-item-grab-handle"></div>' +
        '<a data-target="' + target_audio_id + '" href="' + target_audio_id + '" onclick="playItem(this, ' + '\'toggle\'' +', event)">' +
        '<img class="player-post-img" src="'+ target_img +'">' +
        '<div class="player-post-info">' +
        '<span class="player-post-title">' + target_title + '</span>' +
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

        var target_title_author = target_title + '-' + target_author;

        // 메세지 박스에 띄울 메세지
        var message =
            '<li class="message-list">' +
            '<img class="message-box-post-img" src="'+ target_img + '">' +
            '<div class="message-box-message-body">' +
            '<div class="message-box-post-title">' + target_title_author + '</div>' +
            '<div class="message-box-message">was added to playlist</div>' +
            '</div>' +
            '<div class="message-box-close">' +
            '<button onclick="$(this).parent().parent().fadeOut()">' +
            '<i class="far fa-times-circle"></i>' +
            '</button>' +
            '</div>' +
            '</li>';

        alertMessageBox(message);

        ul.append(list_item);
        togglePlaylistItem();

        if (li.length === 0) {
            loadAudio($(list_item).find("a"));
            updatePlayerPostInfo()
        }
    }
    showPlayer();
    setPlaylistCookie(list_item);
}

// 플레이리스트 아이템 삭제
function deleteFromPlaylist(self) {
    var target_obj = $("#" + $(self).parent().parent().attr("data-target"));
    var target_audio = target_obj.find("audio");
    var audio = $("[loaded]");
    var current_more_action_menu = $("#more-action-menu");
    var target_id = current_more_action_menu.attr("data-target");
    var playlist = $(".player-playlist-item");

    playlist.each(function(index, item) {
        if ($(item).attr("data-target") === target_id) {
            // 리스트에서 항목 삭제
            $(item).fadeOut("fast");
            current_more_action_menu.addClass("hide-menu");

            setTimeout(function () {
                $(item).remove();
            }, 1000);

            // 재생 중이던 오디오를 목록에서 삭제하는 경우
            if (target_audio[0] === audio[0]) {
                // 재생 중이던 오디오 초기화하고 다음 리스트 아이템 재생
                if (!audio[0].paused) {
                    resetWaveform(audio);
                    playPrevNext("next");
                    // 재생중인 오디오가 마지막 아이템일 때 삭제한 경우
                    if (index === (playlist.length - 1)) {
                        playPrevNext("prev");
                        console.log("playing");
                    }
                }
                // 일시정지 중이던 오디오
                else if (audio[0].paused) {
                    resetWaveform(audio);
                    playPrevNext("next", "pause");
                    // 재생중인 오디오가 마지막 아이템일 때 삭제한 경우
                    if (index === (playlist.length - 1)) {
                        console.log("paused");
                        playPrevNext("prev", "pause")
                    }
                }
            }
        }
    });


// 플레이리스트의 마지막 항목을 삭제한 경우
    if (playlist.length === 1) {
        resetPlayer()
    }


// 삭제 메세지
    var target_img = target_obj.find(".track-post-img").attr("src");
    var target_title = target_obj.find(".track-title").text();
    var target_author = target_obj.find(".track-author").text();
    var target_title_author = target_title + '-' + target_author;

    var message =
        '<li class="message-list">' +
        '<img class="message-box-post-img" src="'+ target_img + '">' +
        '<div class="message-box-message-body">' +
        '<div class="message-box-post-title">' + target_title_author + '</div>' +
        '<div class="message-box-message">was deleted from playlist</div>' +
        '</div>' +
        '<div class="message-box-close">' +
        '<button onclick="$(this).parent().parent().fadeOut()">' +
        '<i class="far fa-times-circle"></i>' +
        '</button>' +
        '</div>' +
        '</li>';

    alertMessageBox(message);
}

// 플레이리스트의 아이템 재생
function playItem(self, action="play", e=null) {
    if (e) {
        e.preventDefault();
    }
    var audio = $("#" + $(self).data("target"));
    var audios = $(".audio-file");

    // 플레이리스트에서 아이탬 재생시 다른 모든 음원 초기화
    audios.each(function(index, item) {
        if (!(audio[0] === item)) {
            resetWaveform(item)
        }
    });

    loadAudio(self);
    playAudio(action);
    updatePlayerPostInfo();
    togglePlaylistItem()
}

// 플레이리스트의 이전/다음 아이템 재생
function playPrevNext(direction, action="play") {
    var audio = $("[loaded]");
    var audios = $(".audio-file");
    var target_id = audio.data("target");
    var target_obj_id = $("#" + target_id).find("audio").attr("id");
    var items = $(".player-playlist-item");
    var next_item;

    // 모든 음원 파일 초기화
    audios.each(function(index, item) {
        resetWaveform(item)
    });

    items.each(function(index, item) {
        // 현재 플레이중인 트랙에 대해서
        if ($(item).find("a").data("target") === target_obj_id) {
            // 다음 버튼은 index + 1 재생
            if (direction === 'next') {
                next_item = $(items[index + 1]).find('a');
            }
            // 이전 버튼은 index - 1 재생
            else if (direction === 'prev') {
                next_item = $(items[index - 1]).find('a');
            }

            if (next_item.length) {
                playItem(next_item[0], action)
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
    var check_played = false;  // 오디오가 현재 재생중인 아이템 이전인지 이후인지 판단

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
        }
        // 다른 메뉴를 호출하면 다른 메뉴로 교체
        else {
            current_more_action_menu
                .removeClass("hide-menu")
                .attr("data-target", target_id)
                .fadeIn("fast")
                .find(".more-action-like").attr("onclick", "like(" + target_pk + ")");
        }
    }
    // 메뉴가 안보이는 상태인 경우
    else {
        current_more_action_menu
            .removeClass("hide-menu")
            .attr("data-target", target_id)
            .fadeIn("fast")
            .find(".more-action-like").attr("onclick", "like(" + target_pk + ")");
    }
}

// more-action-menu 바깥 쪽 클릭시 창 닫기
$(document).on("click", function(e) {
    if (!$(e.target).hasClass("menu-item")) {
        $("#more-action-menu")
            .fadeOut("fast")
            .addClass("hide-menu")
    }
});

// 메세지 팝업 관련 함수

// 메세지 박스 나타내기
function alertMessageBox(message) {
    var message_box = $("#message-box");

    message_box.css('display', 'block');
    message_box.append(message);

    var all_messages = $(".message-list");
    var fade_timeout;

    all_messages.each(function(index, item) {
        // 가만히 두면 3초 후 사라짐
        fade_timeout = setTimeout(function() {
            $(item).fadeOut("fast")
        }, 3000);
        // 마우스를 올리면 사라지지 않음
        $(item).on("mouseenter", function() {
            clearTimeout(fade_timeout);
        });
        // 마우스가 벗어나면 다시 3초 후 사라짐
        $(item).on("mouseleave", function() {
            fade_timeout = setTimeout(function() {
                $(item).fadeOut("fast")
            }, 3000)
        })
    });
}

function setPlaylistCookie(list_item) {
    var target_id = $(list_item).attr("data-target");

    var target_obj = $("#" + target_id);
    var item_url = target_obj.find("source").attr("src");
    var title = target_obj.find(".track-title").text();
    var author = target_obj.find(".track-author").text();
    var post_img = target_obj.find(".track-post-img").attr("src");
    console.log(post_img);

    document.cookie = target_id + "=" + item_url;
    document.cookie = target_id + "-title=" + title;
    document.cookie = target_id + "-author=" + author;
    document.cookie = target_id + "-img=" + post_img;
}

function deletePlaylistCookie() {

}