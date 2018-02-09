var tracklist = $(".tracklist");
var btns = $(".profile-body-menu");
var tracks_loaded = false;
var track_counter = 1;
var comments_loaded = false;
var playlist_loaded = false;

function showAll () {
    for (var i = 0; i < tracklist.length; i++) {
        tracklist[i].style.display = "none";
        btns[i].classList.remove("clicked")
    }
    var tracks_btn = $("#show-all-btn");
    var show_all = $("#show-all");
    tracks_btn.addClass("clicked");
    show_all[0].style.display = "block"
}

// tracks 메뉴를 불러옴
function showTracks () {
    // 먼저 모든 메뉴들을 숨김
    // 모든 메뉴 버튼들의 clicked 클래스 삭제
    for (var i = 0; i < tracklist.length; i++) {
        tracklist[i].style.display = "none";
        btns[i].classList.remove("clicked")
    }
    // 그런 다음 tracks 메뉴의 버튼에 clicked 클래스 추가
    // tracks 의 div 만 숨김 해제
    var tracks_btn = $("#show-tracks-btn");
    var show_tracks = $("#show-tracks");
    tracks_btn.addClass("clicked");
    show_tracks[0].style.display = "block";

    // tracks_loaded 가 true 이면 ajax 를 중복 실행하지 않고 함수 실행 종료
    if (tracks_loaded) return;
    // if (tracks_counter > 1) return;
    // user/pk/tracks 로 POST 요청을 보내어 렌더링된 html 파일을 json 으로 받아옴
    var url = show_tracks.attr("data-url");
    sendAjax(url, track_counter, show_tracks);

    // tracks_loaded 를 true로 바꿔주어 중복 ajax가 실행되지 않도록 해줌.
    tracks_loaded = true;
    track_counter += 1
}

function showMoreTracks() {
    var show_tracks = $("#show-tracks");
    var url = show_tracks.attr("data-url");
    var more_btn = $("#show-more-btn");
    sendAjax(url, track_counter, show_tracks);
    more_btn[0].style.display = "none";
}

function showComments () {
    for (var i = 0; i < tracklist.length; i++) {
        tracklist[i].style.display = "none";
        btns[i].classList.remove("clicked")
    }
    var tracks_btn = $("#show-comments-btn");
    var show_tracks = $("#show-comments");
    tracks_btn.addClass("clicked");
    show_tracks[0].style.display = "block"
}

function showPlaylist () {
    for (var i = 0; i < tracklist.length; i++) {
        tracklist[i].style.display = "none";
        btns[i].classList.remove("clicked")
    }
    var tracks_btn = $("#show-playlist-btn");
    var show_tracks = $("#show-playlist");
    tracks_btn.addClass("clicked");
    show_tracks[0].style.display = "block";
}

function sendAjax (url, counter, target) {
    // user/pk/tracks 로 POST 요청을 보내어 렌더링된 html 파일을 json 으로 받아옴
    if (counter < 4) {
        var csrf_token = $('[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: "POST",
            url: url,
            data:
                {
                    'counter': counter,
                    'csrfmiddlewaretoken': csrf_token
                },
            async: true,
            dataType: "json",
            success: function(response) {
                // 받아온 html을 show-tracks div 안에 붙여준다.
                target.append(response.html)
            }
        });
    }
}
