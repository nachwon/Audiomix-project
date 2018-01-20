window.onscroll = function() {header_scroll()};

function header_scroll() {
    if (document.body.scrollTop > 30 || document.documentElement.scrollTop > 30) {
        document.getElementById("header").classList.add("header-scrolled");
        document.getElementById("wrapper").classList.add("wrapper-scrolled");
        document.getElementById("title-logo").classList.add("title-logo-scrolled");
        document.getElementById("current-user").classList.add("current-user-scrolled");
        document.getElementById("dropdown").classList.add("dropdown-scrolled");

    } else {
        document.getElementById("header").className = "header transition";
        document.getElementById("wrapper").className = "wrapper transition";
        document.getElementById("title-logo").className = "title-logo transition";
        document.getElementById("current-user").className = "current-user transition";
        document.getElementById("dropdown").className = "dropdown  transition";
    }
};

function dropdown() {
    document.getElementById("myDropdown").classList.toggle("appear");
    document.getElementById("drop-btn").classList.toggle("focused");
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
        var dropdownbtn = document.getElementById("drop-btn");
        if (dropdownbtn.classList.contains('focused')) {
            dropdownbtn.classList.remove('focused');
        }
    }
}