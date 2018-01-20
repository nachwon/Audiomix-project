$(document).ready(function(){
    $('.signin-btn').click(function(){
        var $href = $(this).attr('href');
        layer_popup($href);
    });
    function layer_popup(el){

        var $el = $(el);        //레이어의 id를 $el 변수에 저장
        var isDim = $el.prev().hasClass('dimBg');   //dimmed 레이어를 감지하기 위한 boolean 변수

        isDim ? $('.dim-layer').fadeIn() : $el.fadeIn();

        var $elWidth = ~~($el.outerWidth()),
            $elHeight = ~~($el.outerHeight()),
            docWidth = $(document).width(),
            docHeight = $(document).height();

        // 화면의 중앙에 레이어를 띄운다.
        if ($elHeight < docHeight || $elWidth < docWidth) {
            $el.css({
                marginTop: -$elHeight /2,
                marginLeft: -$elWidth/2
            })
        } else {
            $el.css({top: 0, left: 0});
        }

        $el.find('a.btn-layerClose').click(function(){
            isDim ? $('.dim-layer').fadeOut() : $el.fadeOut(); // 닫기 버튼을 클릭하면 레이어가 닫힌다.
            return false;
        });

        $('.layer .dimBg').click(function(){
            $('.dim-layer').fadeOut();
            return false;
        });

    }
});


window.onscroll = function() {header_scroll()};

function header_scroll() {
    if (document.body.scrollTop > 30 || document.documentElement.scrollTop > 30) {
        document.getElementById("header").classList.add("header-scrolled");
        document.getElementById("wrapper").classList.add("wrapper-scrolled");
        document.getElementById("title-logo").classList.add("title-logo-scrolled");
        document.getElementById("header-btns").classList.add("header-buttons-scrolled");
        document.getElementById("signup-btn").classList.add("signup-btn-scrolled");
    } else {
        document.getElementById("header").className = "header transition";
        document.getElementById("wrapper").className = "wrapper transition";
        document.getElementById("title-logo").className = "title-logo transition";
        document.getElementById("header-btns").className = "header-buttons transition";
        document.getElementById("signup-btn").className = "signup-btn transition";
    }
}
