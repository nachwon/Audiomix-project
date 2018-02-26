var tracklist = $(".tracklist");
var btns = $(".profile-body-menu");

// Tracks
var tracks_loaded = false;
var track_counter = 1;

// Comments
var comments_loaded = false;
var comment_counter = 1;

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
    // 카운터 숫자를 하나씩 올려줌
    track_counter += 1
}

// show more tracks 버튼을 누르면
function showMoreTracks() {
    var show_tracks = $("#show-tracks");
    var url = show_tracks.attr("data-url");
    var more_btn = $(".more-tracks-btn");
    // ajax로 다음 페이지를 불러옴
    sendAjax(url, track_counter, show_tracks);
    // show more 버튼을 지워줌
    for (var i = 0; i < more_btn.length; i++) {
        more_btn[i].style.display = "none";
    }
    track_counter += 1
}

// Comments 메뉴를 불러옴
function showComments () {
    for (var i = 0; i < tracklist.length; i++) {
        tracklist[i].style.display = "none";
        btns[i].classList.remove("clicked")
    }
    var tracks_btn = $("#show-comments-btn");
    var show_comments = $("#show-comments");
    tracks_btn.addClass("clicked");
    show_comments[0].style.display = "block";

    if (comments_loaded) return;

    var url = show_comments.attr("data-url");
    sendAjax(url, comment_counter, show_comments);

    comments_loaded = true;
    comment_counter += 1
}

function showMoreComments () {
    var show_comments = $("#show-comments");
    var url = show_comments.data("url");
    var more_btn = $(".more-comments-btn");

    sendAjax(url, comment_counter, show_comments);

    more_btn.each(function(index, item) {
        $(item).css("display", "none")
    });

    comment_counter += 1;

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

// ajax 요청을 보내는 함수
// 보내는 주소, 페이지 번호, 리턴된 html 을 붙여줄 타겟 엘리먼트를 인자로 받음
function sendAjax (url, counter, target) {
    // user/pk/tracks 로 POST 요청을 보내어 렌더링된 html 파일을 json 으로 받아옴
    // 페이지번호 3 까지만 실행
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
