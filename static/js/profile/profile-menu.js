var tracklist = $(".tracklist");
var btns = $(".profile-body-menu");
var tracks_loaded = false;
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

function showTracks () {
    for (var i = 0; i < tracklist.length; i++) {
        tracklist[i].style.display = "none";
        btns[i].classList.remove("clicked")
    }
    var tracks_btn = $("#show-tracks-btn");
    var show_tracks = $("#show-tracks");
    tracks_btn.addClass("clicked");
    show_tracks[0].style.display = "block";

    if (tracks_loaded) return;

    var url = show_tracks.attr("data-url");
    var csrf_token = $('[name=csrfmiddlewaretoken]').val();
    $.ajax({
        type: "POST",
        url: url,
        data: {'csrfmiddlewaretoken': csrf_token},
        dataType: "json",
        success: function(response) {
            console.log(response);
            $("#show-tracks").append(response.html)
        }
    });
    tracks_loaded = true
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
