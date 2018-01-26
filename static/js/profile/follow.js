// 페이지 로딩이 끝난 후 함수 실행
$(document).ready(function() {
    // follow-btn 을 클릭했을 때 follow 함수 실행
    document.getElementById("follow-btn").onclick = function() {
        follow();
    };

    get_follow_status();

    // 팔로우 버튼 텍스트 바꿔주는 함수
    function get_follow_status() {
        var xhttp = new XMLHttpRequest();
        var user_pk = document.getElementById("follow-btn").getAttribute("data-follow-user");
        xhttp.onreadystatechange = function() {
            if (xhttp.responseText === "True") {
                document.getElementById("follow-btn").innerHTML = "Following";
            }
            else {
                document.getElementById("follow-btn").innerHTML = "Follow";
            }
        };
        // views:user:follow 뷰에 요청보내서 결과를 가져옴
        // follow 뷰는 현재 유저가 보고있는 유저를 팔로우하고 있으면 True, 아니면 False
        xhttp.open("GET", user_pk, true);
        xhttp.send()
    }

    // count를 받아서 follower-count의 텍스트에 넣어줌
    function change_follower_count(count) {
        document.getElementById("follower-count").innerHTML = count
    }

    // follow 함수
    function follow() {
        // 새로운 HttpRequest 객체 생성
        var xhttp = new XMLHttpRequest();
        // CSRF 토큰 가져와 변수에 저장
        var csrf_token = $('[name=csrfmiddlewaretoken]').val();
        var follow_user = document.getElementById("follow-btn").getAttribute("data-follow-user");
        // readyState가 변할 때 마다 실행할 함수 설정
        xhttp.onreadystatechange = function() {
            // 요청의 readyState가 4(complete)인 경우 함수 실행
            if (this.readyState === 4) {

                // 요청 결과의 status code가 201인 경우
                if (this.status === 201) {
                    // 버튼의 텍스트를 Following으로 변경
                    document.getElementById("follow-btn").innerHTML = "Following";
                    // change_follower_count 함수에 응답으로 받은 count 입력
                    var count = JSON.parse(xhttp.responseText).count;
                    change_follower_count(count);
                }

                // 요청 결과의 status code가 204인 경우
                else if (this.status === 204) {
                    // 버튼의 텍스트를 Follow로 변경
                    document.getElementById("follow-btn").innerHTML = "Follow";
                    // count 변수에 현재 follower-count 저장
                    var count = document.getElementById("follower-count").innerText;
                    // change_follower_count 함수에 count -1 입력
                    change_follower_count(count - 1);
                }
            }
        };

        // /user/pk/follow로 POST 요청을 비동기로 보냄
        xhttp.open("POST", follow_user, true);
        // 요청의 헤더에 CSRF 토큰 포함
        xhttp.setRequestHeader('X-CSRFToken', csrf_token);
        // user키의 값으로 요청 보내는 유저 객체 전달
        xhttp.send();
    }
});