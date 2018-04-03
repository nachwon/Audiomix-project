var addToMixerBtn = $(".add-to-mixer-btn");
var contextArray = [];

addToMixerBtn.on("click", function() {
    var targetId = $(this).data("target");
    var targetInst = $(this).data("instrument");
    var targetAuthor = $(this).data("author");
    var isLoaded = false;
    var channels = $(".channel");
    var emptyChannel = [];
    var channel, instrument, author;
    var icon = $(this).find(".glyphicon");
    var text = $(this).find(".to-mixer-text");

    channels.each(function (index, item) {
        if (!$(item).attr("data-target-audio")) {
            emptyChannel.push(index);
        }
        if ($(item).attr("data-target-audio") === targetId) {
            isLoaded = index;
        }
    });

    if (isLoaded) {
        channel = $(channels[isLoaded]);
        channel.attr("data-target-audio", "");
        instrument = channel.find(".channel-instrument");
        author = channel.find(".channel-author");
        instrument.text("Not");
        author.text("Loaded");

        channel.removeClass("channel-loaded");
        icon.removeClass("glyphicon-minus-sign");
        icon.addClass("glyphicon-plus-sign");
        text.text("Add to Mixer");

        alertMessageBox("", targetInst + " track by " + targetAuthor, "was removed to mixer")
    }
    else {
        channel = $(channels[emptyChannel.min()]);
        channel.attr("data-target-audio", targetId);
        instrument = channel.find(".channel-instrument");
        author = channel.find(".channel-author");
        instrument.text(targetInst);
        author.text(targetAuthor);

        channel.addClass("channel-loaded");
        icon.addClass("glyphicon-minus-sign");
        icon.removeClass("glyphicon-plus-sign");
        text.text("Remove from Mixer");

        alertMessageBox("", targetInst + " track by " + targetAuthor, "was added to mixer")
    }
});

// ------- Mixer ------- //

var loadMixerBtn = $(".load-mixer-btn");
var mixerLoaded = false;
var ctxLoaded = false;
var animationArray = new Array(8);

var AudioContext = window.AudioContext || window.webkitAudioContext;

// 믹서 버튼 클릭 시
loadMixerBtn.on("click", function () {
    // 믹서 로딩이 안되어있으면
    if (!mixerLoaded) {
        // 오디오 콘텍스트 연결
        loadMixer(true);
        // 믹서 내려오기
        toggleMixer();
        // 마스크 페이드 인
        $(".mixer-mask").fadeIn("fast");

        mixerLoaded = true;
    }
    // 믹서 로딩이 되어있으면
    else if (mixerLoaded) {
        loadMixer(false);
        // 믹서 올리기
        toggleMixer();
        // 마스크 페이드 아웃
        $(".mixer-mask").fadeOut("fast");

        mixerLoaded = false;
    }
});

// 믹서 올리기/내리기 토글 함수
function toggleMixer() {
    var mixer = $("#mixer");
    var mixerWidth = mixer.width();
    var mixerHeight = mixer.height();

    if (!mixer.attr("mixer-loaded")) {
        // 믹서 가운데 배치
        mixer.css("left", "calc(50% - " + mixerWidth / 2 + "px)");
        mixer.css("top", "calc(50% - " + mixerHeight / 2 + "px)");

        mixer.attr("mixer-loaded", true)
    }
    else {
        mixer.css("top", "-1000px");
        mixer.attr("mixer-loaded", null)
    }
}

function createAudioCtx(channels) {
    contextArray = [];
    channels.each(function(index, item) {
        var audioCtx = new AudioContext();
        contextArray.push([index, audioCtx])
    });
    ctxLoaded = true;
}

// sourceArray와 .channel 요소들을 비교하여 오디오 컨텍스트 로딩
// channel의 타겟 오디오가 sourceArray에 있으면 Audio Context를 새로 생성하지 않고 어레이에서 꺼내온 다음 함수 실행 종료
// 없으면 새로 생성하고 노드 연결까지 수행
function loadMixer(connect=true) {
    var channels = $(".channel");

    if (!ctxLoaded) {
        createAudioCtx(channels);
    }

    channels.each(function(index, item) {
        var targetId = $(item).attr("data-target-audio");

        if (!targetId) {
            return
        }

        var audio = $("#" + targetId)[0];

        if (!connect) {
            $(contextArray).each(function (index, item) {
                item[1].close();
                ctxLoaded = false;
            });
        }

        // contextArray 에서 audioCtx 꺼내옴
        var audioCtx = contextArray[index][1];
        var source = getAudioData(targetId, audioCtx);
        audioCtx.connected = source;

        // 분석 노드 생성
        var analyser = audioCtx.createAnalyser();

        // 분석 노드 설정
        analyser.maxDecibels = -10;
        analyser.fftSize = 256;
        var bufferLength = analyser.frequencyBinCount;
        var dataArray = new Uint8Array(bufferLength);

        // 게인 노드 생성 및 설정
        var gainNode = audioCtx.createGain();
        connectFader(gainNode, audioCtx, index);

        // 피크 관련 변수
        var peak = 0;
        var peakOpacity = 1;
        var peakTime;

        // 미터 뒷 배경 캔버스 엘리먼트
        var meterBase = drawFaderBackgroundBase();

        // 미터 뒷 배경을 가져와 그려줄 캔버스 엘리먼트
        var meter = document.getElementsByClassName("meter-base")[index];

        // 미터 막대 그리기 함수
        function faderBackgroundDraw() {
            animationArray[index] = requestAnimationFrame(faderBackgroundDraw);

            var barHeight;

            // 실시간 프리퀀시 바이트 데이터를 어레이에 저장
            analyser.getByteFrequencyData(dataArray);

            // 페이더 미터 표시 설정
            // dataArray의 평균값을 구한 다음 페이더의 높이에 비례하게 설정
            // 그럴싸하게 표시되도록 때려맞춘 값이기 때문에 실제 피크 미터가 작동하는 방식과는 차이가 있을 듯...
            var sum = dataArray.reduce(function(a, b) { return a + b; });
            var avg = sum / dataArray.length;

            var fader = document.getElementsByClassName("fader")[index];
            var faderHeight = $(fader).css("top");
            var extractNum = /([\d+.]*)px/i;
            var threshold = 250 - parseFloat(faderHeight.match(extractNum)[1]);
            barHeight = threshold * (avg / 70);

            // 피크 값 갱신 설정
            // 막대 높이 보다 피크값이 작으면 막대 높이를 피크 값에 할당
            // 피크 값이 갱신되는 경우 피크 타임 초기화, 피크 투명도 초기화
            if (peak < barHeight) {
                peak = barHeight;
                peakTime = 80;
                peakOpacity = 1;
            }

            // barHeight 값에 따라 미터와 피크값을 그려줌
            if (meter.getContext) {
                var meterCtx = meter.getContext('2d');
                var width = 10;
                var height = 300;
                // 캔버스 초기화
                meterCtx.clearRect(0, 0, width, height);
                // 피크 타임이 10 이하로 내려온 경우 Opacity 1씩 빼줌
                if (peakTime < 10 && peakTime > 0) {
                    peakOpacity -= 0.1;
                }
                // 피크 타임이 0 이하로 내려간 경우 피크 관련 값들 리셋해주어 새로운 피크가 표시되도록 함
                else if (peakTime < 0) {
                    peak = 0;
                    peakOpacity = 1;
                    peakTime = 80;
                }
                // 피크 그리기
                meterCtx.fillStyle = "rgb(219, 47, 47, " + peakOpacity + ")";
                meterCtx.fillRect(1, height - peak, 8, 2);
                // 피크 타임 줄여줌
                peakTime -= 1;
                // 미터 그리기
                meterCtx.drawImage(meterBase,
                    1, height - barHeight,
                    width, height,
                    1, height - barHeight,
                    width, height)
            }
        }

        var mixerPlayBtn = $(".mixer-play-btn");

        mixerPlayBtn.on("click", function() {
            playLoadedChannels();
        });

        // 패너 노드 생성 및 설정
        var pannerNode = audioCtx.createPanner();
        connectPanner(pannerNode, audioCtx, index);
        pannerBackgroundDraw(index);

        // 소스 -> 패너 노드 -> 게인 노드 연결
        var panner_connected = source.connect(pannerNode);
        var gain_panner_connected = panner_connected.connect(gainNode);

        // 게인 노드 -> 분석 노드 -> 데스티네이션(스피커)으로 연결
        // 분석노드는 루트의 어느 곳에 연결되든 상관 없음
        gain_panner_connected.connect(analyser);

        analyser.connect(audioCtx.destination);
        if (!audio.paused) {
            audio.pause();
        }

        if (connect) {
            // 미터 그리기 함수 실행
            faderBackgroundDraw();
        }
    });
    if (!connect) {
        $(animationArray).each(function(index, item) {
            cancelAnimationFrame(item)
        });
    }
}

function getAudioData(commentPk, audioCtx) {
    console.log(commentPk);
    var source = audioCtx.createBufferSource();

    var request = new XMLHttpRequest();
    var csrf_token = $('[name=csrfmiddlewaretoken]').val();

    var commentPattern = /comment-track-(\d+)/i;
    var authorPattern = /track-(\d+)-author-audio/i;

    var pk = commentPk.match(commentPattern);
    var requestUrl;

    if (pk) {
        pk = pk[1];
        requestUrl = "/post/comment/" + pk + "/";
    }
    else {
        pk = commentPk.match(authorPattern)[1];
        requestUrl = "/post/" + pk + "/author-track/"
    }

    request.open("POST", requestUrl);

    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.responseType = 'arraybuffer';

    request.onload = function () {
        var audioData = request.response;
        audioCtx.decodeAudioData(audioData, function (buffer) {
            source.buffer = buffer;
        });
    };

    request.send();

    return source
}


function playLoadedChannels(func, stop=false,) {
    $(contextArray).each(function(index, item) {
        if (item[1].connected) {
            item[1].connected.start(0);
        }
    })
}

// 미터 뒷 배경 캔버스 함수
function drawFaderBackgroundBase() {
    var meterBase = document.createElement("canvas");
    var h = 38;
    var s = 100;
    var l = 45;
    meterBase.width = 10;
    meterBase.height = 300;

    if (meterBase.getContext) {

        var meterBaseCtx = meterBase.getContext('2d');
        meterBaseCtx.fillStyle = "#242424";
        meterBaseCtx.clearRect(0, 0, 10, 300);
        var meterHeight = meterBase.height;

        // 미터 한 칸 두깨 2px, 사이 공간 1px 총 3px이 필요함
        // 미터 전체 높이를 3으로 나눈 뒤 3px 씩 그려줌
        for (var i = 0; i < meterHeight/3; i++) {
            l += 0.5;
            meterBaseCtx.fillStyle = "hsl("+ h +", " + s + "% , " + l + "%)";
            meterBaseCtx.fillRect(1, meterHeight - (i * 3 + 1), 8, 2)
        }
    }

    return meterBase;
}

// 페이더 동작 설정
function connectFader(gainNode, audioCtx, index) {
    var fader = document.getElementsByClassName("fader");

    // 페이더에서 마우스 다운 시
    $(fader[index]).on("mousedown", function(e) {
        // 요소내에서 마우스 다운된 위치의 Y축 좌표 값 저장
        var offsetY = e.offsetY;

        // 포인터 이벤트 없애줌
        $(this).css("pointer-events", "none");

        // 페이지 전체에 대해
        $(document)
        // mousemove 이벤트 등록해서 Y 축 좌표값에 따라 페이더 이동 및 gainNode gain값 조절
            .on("mousemove", function(e) {
                var volume = setFaderPosition(e, fader[index], offsetY);
                var gain_value = 1.25 - volume / 200;

                gainNode.gain.value = gain_value;

                var fader_value = Math.round((gain_value - 1) * 1000) / 100;
                if (fader_value > 0) {
                    fader_value = "+" + fader_value;
                }
                else if (fader_value === -10) {
                    fader_value = "-\u221E"
                }
                var fader_value_display = $(fader[index]).parents(".channel-wrapper").find(".fader-value");

                fader_value_display.text(fader_value);
            })
            // 마우스를 떼면 movsemove 이벤트 제거하고 페이더의 포인터 이벤트 원상복구
            .on("mouseup", function() {
                $(this).off("mousemove");
                $(fader[index]).css("pointer-events", "visible");
            });
    });
}

// 페이더 드래그 시 위치 변경
function setFaderPosition(e, fader, offsetY) {
    var meter_position = $(fader).parent();

    var position = parseFloat(e.pageY) - parseFloat(meter_position.offset().top) - parseFloat(offsetY);

    if (position > 250) {
        position = 250
    }
    else if (position < 0) {
        position = 0
    }
    $(fader).css("top", position + "px");

    return position
}

function connectPanner(pannerNode, audioCtx, index) {
    // 화면 가운데 위치 좌표값 저장
    var WIDTH = window.innerWidth;
    var HEIGHT = window.innerHeight;

    var xPos = Math.floor(WIDTH/2);
    var yPos = Math.floor(HEIGHT/2);
    var zPos = 300;

    // 패너 노드 초기 세팅
    pannerNode.panningModel = 'equalpower';
    pannerNode.distanceModel = 'linear';
    pannerNode.refDistance = 1;
    pannerNode.maxDistance = 10000;
    pannerNode.rolloffFactor = 1;
    pannerNode.coneInnerAngle = 360;
    pannerNode.coneOuterAngle = 0;
    pannerNode.coneOuterGain = 0;

    if(pannerNode.orientationX) {
        pannerNode.orientationX.value = 1;
        pannerNode.orientationY.value = 0;
        pannerNode.orientationZ.value = 0;
    } else {
        pannerNode.setOrientation(1,0,0);
    }

    // 리스너 세팅
    var listener = audioCtx.listener;

    if(listener.forwardX) {
        listener.forwardX.value = 0;
        listener.forwardY.value = 0;
        listener.forwardZ.value = -1;
        listener.upX.value = 0;
        listener.upY.value = 1;
        listener.upZ.value = 0;
    } else {
        listener.setOrientation(0,0,-1,0,1,0);
    }

    // 리스너 위치 세팅
    listener.setPosition(xPos, yPos, zPos);
    // 패너 위치 세팅
    pannerNode.setPosition(xPos, yPos, zPos + 30);

    var pan_slider = document.getElementsByClassName("pan-slider");

    // 팬 슬라이더에 마우스 다운 시
    $(pan_slider[index]).on("mousedown", function(e) {
        // 마우스 클릭 한 부분 그대로에서부터 이동시키도록 해주기 위한 값
        var offsetX = e.offsetX;

        // 오작동 방지를 위한 포인터이벤트 제거
        $(this).css("pointer-events", "none");

        $(document)
        // 팬 슬라이더 클릭 후 누르고 있는 상태 유지시(=마우스 다운) 문서 전체에서 마우스 움직임 감지
            .on("mousemove", function(e) {
                // 팬 슬라이더 위치 값 0 ~ 60 에서
                // 가운데를 0으로 하기 위해서 30을 빼줌: -30 ~ 30
                var panner_position = setPannerPosition(e, pan_slider[index], offsetX) - 30;

                // 팬 슬라이더 위치에 따라 패너 노드 위치값 변경
                pannerNode.setPosition(xPos + (panner_position * 2), yPos, zPos + 30);

                // 팬 슬라이더 위치 값을 % 단위로 변경 -100 ~ 100
                var panner_value = Math.floor(panner_position / 30 * 100);
                // % 단위 값을 절대값으로 변경
                var abs_value = Math.abs(panner_value);

                // 슬라이더가 가운데에 있을 때는 C 표시
                if (panner_value === 0) {
                    panner_value = "C"
                }
                // 0 보다 작을 경우, 즉, 왼쪽으로 패닝 할 경우 L + % 단위 절대값 표시
                else if (panner_value < 0) {
                    panner_value = "L" + abs_value;
                    // 배경을 가리고 있는 div 넓이 왼쪽으로 줄여줌
                    $(pan_slider[index]).siblings(".fill-left").css("width", 50 - (abs_value / 2) + "%");
                    $(pan_slider[index]).siblings(".fill-right").css("width", "50%");

                }
                // 0 보다 클 경우, 즉, 오른쪽으로 패닝 할 경우 R + % 단위 절대값 표시
                else if (panner_value > 0) {
                    panner_value = "R" + abs_value;
                    // 배경을 가리고 있는 div 넓이 오른쪽으로 줄여줌
                    $(pan_slider[index]).siblings(".fill-left").css("width", "50%");
                    $(pan_slider[index]).siblings(".fill-right").css("width", 50 - (abs_value / 2) + "%");
                }

                // panner_value 를 패너 디스플레이에 표시
                var panner_value_display = $(pan_slider[index]).parents(".channel-wrapper").find(".panner-value");
                panner_value_display.text(panner_value);

            })

            // 전체 창 위에서 마우스 때면
            .on("mouseup", function() {
                // 마우스무프 이벤트 제거
                $(this).off("mousemove");
                // 슬라이더 포인터 이벤트 원상복구
                $(pan_slider[index]).css("pointer-events", "visible");
            })
    })
}

// 마우스 움직임에 따라 팬 슬라이더 위치값 변경해주는 함수
function setPannerPosition(e, pan_slider, offsetX) {
    var panner = $(pan_slider).parent();
    var pannerCenter = $(pan_slider).width() / 2;



    // 전체 페이지에 대하여 계산한 이벤트 발생 위치 X축 값
    // - 패너 요소의 왼쪽 부분이 전체 페이지의 가장 왼쪽으로부터 떨어진 거리
    // - 팬 슬라이더 가장 왼쪽부터 잰 마우스 다운 이벤트 발생 위치 X축 값 (한 이벤트 사이클 내에서는 고정 된 값)
    var position = parseFloat(e.pageX) - parseFloat(panner.offset().left) - parseFloat(offsetX);

    // 슬라이더가 양쪽 끝으로 움직였을 때 양쪽 모두에서 슬라이더의 가운데 까지만 밖으로 나가도록 설정
    // 즉 슬라이더의 가운데를 기준으로 포지션 설정
    // 최소값 0
    if (position < 0 - pannerCenter) {
        position = 0 - pannerCenter;
    }
    // 최대값 60
    else if (position > 60 - pannerCenter ) {
        position = 60 - pannerCenter;
    }

    // 슬라이더 위치 지정
    $(pan_slider).css("left", position + "px");

    // 패너 값에 넘겨줄 포지션 값 리턴
    // 슬라이더의 가운데를 기준으로 패너 값 설정하기 위해 슬라이더 넓이의 반 만큼을 더해줌
    return position + $(pan_slider).width() / 2;
}

// 패너 뒷 바탕 채우기
function pannerBackgroundDraw(index) {
    var canvas = document.getElementsByClassName("panner-background")[index];
    var width = $(canvas).width();

    if (canvas.getContext) {
        var ctx = canvas.getContext('2d');

        for (var i = 0; i < width/3; i++) {
            ctx.fillStyle = "rgb(226, 176, 38, 0.9)";
            ctx.fillRect(i * 3 + 1, 1, 2, 5);
        }
    }
}




