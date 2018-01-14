window.onscroll = function() {header_scroll()};

function header_scroll() {
    if (document.body.scrollTop > 30 || document.documentElement.scrollTop > 30) {
        document.getElementById("header").className = "header header-scrolled transition container";
        document.getElementById("wrapper").className = "wrapper wrapper-scrolled transition";
        document.getElementById("title-logo").className = "title-logo title-logo-scrolled transition";
    } else {
        document.getElementById("header").className = "header container transition";
        document.getElementById("wrapper").className = "wrapper transition";
        document.getElementById("title-logo").className = "title-logo transition";
    }
};

function dropdown() {
    document.getElementById("myDropdown").classList.toggle("appear");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {

        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('appear')) {
                openDropdown.classList.remove('appear');
            }
        }
    }
}



