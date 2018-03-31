$(document).ready(function() {
    loadMixer();
});

function loadMixer() {
    var channels = $(".channel");
    channels.each(function(index, item) {
        var audio = $("#" + $(item).attr("data-target-audio"))[0];
        var AudioContext = window.AudioContext || window.webkitAudioContext;
        var audioCtx = new AudioContext();

        // 오디오 소스 생성
        var source = audioCtx.createMediaElementSource(audio);

        var analyzer = audioCtx.createAnalyser();
        analyzer.maxDecibels = -10;

        analyzer.fftSize = 256;
        var bufferLength = analyzer.frequencyBinCount;
        var dataArray = new Uint8Array(bufferLength);

        // 게인 노드 생성 및 설정
        var gainNode = audioCtx.createGain();
        connectFader(gainNode, audioCtx, index);

        // 피크 관련 변수
        var peak;
        var peakOpacity;
        var peakTime;

        // 오디오 트랙이 재생될 때
        $(audio).on("play", function() {
            // 피크 값, 투명도 초기화
            peak = 0;
            peakOpacity = 1;
            // 미터 그리기 함수 실행
            faderBackgroundDraw();
        });

        // 미터 뒷 배경 캔버스 엘리먼트
        var meterBase = drawFaderBackgroundBase();

        // 미터 뒷 배경을 가져와 그려줄 캔버스 엘리먼트
        var meter = document.getElementsByClassName("meter-base")[index];

        function faderBackgroundDraw() {
            // 반복 실행
            var animationRequest= requestAnimationFrame(faderBackgroundDraw);
            var barHeight;

            // 실시간 프리퀀시 바이트 데이터를 어레이에 저장
            analyzer.getByteFrequencyData(dataArray);

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

            // 재생이 멈추면
            if (audio.paused) {
                // 미터 높이를 1 씩 줄여주어 천천히 줄어드는 효과 적용
                barHeight -= 1;
                peakOpacity -= 0.01;

                // 다 줄어들면 반복 정지
                if (barHeight < 0 && peakOpacity < 0) {
                    cancelAnimationFrame(animationRequest);
                }
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

        // 패너 노드 생성 및 설정
        var pannerNode = audioCtx.createPanner();
        connectPanner(pannerNode, audioCtx, index);
        pannerBackgroundDraw(index);

        // 소스 -> 노드 연결
        var gain_connected = source.connect(gainNode);
        var gain_panner_connected = gain_connected.connect(pannerNode);

        // 노드 -> 애널라이저 -> 데스티네이션으로 연결
        gain_panner_connected.connect(analyzer);
        analyzer.connect(audioCtx.destination);
    })
}

// 미터 뒷 배경 캔버스 함수
function drawFaderBackgroundBase() {
    var meterBase = document.createElement("canvas");
    var r = 266;
    var g = 176;
    var b = 38;
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
            meterBaseCtx.fillStyle = "rgb("+ r +", " + g + ", " + b + ")";
            meterBaseCtx.fillRect(1, i * 3 + 1, 8, 2)
        }
    }

    return meterBase;
}

function connectPanner(pannerNode, audioCtx, index) {
    // 화면 가운데 위치 좌표값 저장
    var WIDTH = window.innerWidth;
    var HEIGHT = window.innerHeight;

    var xPos = Math.floor(WIDTH/2);
    var yPos = Math.floor(HEIGHT/2);
    var zPos = 300;

    // 패너 노드 초기 세팅
    pannerNode.panningModel = 'HRTF';
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

    $(pan_slider[index]).on("mousedown", function(e) {
        var offsetX = e.offsetX;
        $(this).css("pointer-events", "none");
        $(document)
            .on("mousemove", function(e) {
                var panner_position = setPannerPosition(e, pan_slider[index], offsetX) - 30;
                pannerNode.setPosition(xPos + (panner_position * 2), yPos, zPos + 30);

                var panner_value = Math.floor(panner_position / 30 * 100);
                var abs_value = Math.abs(panner_value);


                if (panner_value === 0) {
                    panner_value = "C"
                }
                else if (panner_value < 0) {
                    panner_value = "L" + abs_value;
                    $(pan_slider[index]).siblings(".fill-left").css("width", 50 - (abs_value / 2) + "%");
                    $(pan_slider[index]).siblings(".fill-right").css("width", "50%");

                }
                else if (panner_value > 0) {
                    panner_value = "R" + abs_value;
                    $(pan_slider[index]).siblings(".fill-left").css("width", "50%");
                    $(pan_slider[index]).siblings(".fill-right").css("width", 50 - (abs_value / 2) + "%");
                }

                var panner_value_display = $(".panner").parents(".channel-wrapper").find(".panner-value");
                panner_value_display.text(panner_value);

            })
            .on("mouseup", function() {
                $(this).off("mousemove");
                $(pan_slider[index]).css("pointer-events", "visible");
            })
    })
}

function setPannerPosition(e, pan_slider, offsetX) {
    var panner = $(pan_slider).parent();

    var position = parseFloat(e.pageX) - parseFloat(panner.offset().left) - parseFloat(offsetX);

    if (position < 0) {
        position = 0;
    }
    else if (position > 60) {
        position = 60;
    }

    position -= $(pan_slider).width() / 2;

    $(pan_slider).css("left", position + "px");

    return position + 3
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
                var fader_value_display = $(".fader").parents(".channel-wrapper").find(".fader-value");

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

