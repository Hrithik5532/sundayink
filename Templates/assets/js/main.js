$('.oleez-header .dropdown').hover(function() {
    $(this).find('.dropdown-menu').first().stop(true, true).delay(250).slideDown();
}, function() {
    $(this).find('.dropdown-menu').first().stop(true, true).delay(100).slideUp();
});

$('[data-toggle="offCanvasMenu"]').click(function() {
    $('#offCanvasMenu').addClass('open');
});

$('[data-dismiss="offCanvasMenu"]').click(function() {
    $(this).parent('#offCanvasMenu').removeClass('open');
});

$('[data-toggle="searchModal"]').click(function() {
    $('#searchModal').addClass('open');
});

$('[data-dismiss="searchModal"]').click(function() {
    $(this).parent('#searchModal').removeClass('open');
});

mybutton = document.getElementById("myScroll");
window.onscroll = function() {
    scrollFunction()
};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}