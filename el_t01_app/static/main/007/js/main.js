$(function ($) {
    "use strict";
 
    jQuery(document).ready(function () {


    //   magnific popup activation
    $('.video-play-btn, .play-video').magnificPopup({
        type: 'video'
    });
    
    $('.img-popup').magnificPopup({
        type: 'image'
    });

    // Product deal countdown
    $('[data-countdown]').each(function () {
        var $this = $(this),
            finalDate = $(this).data('countdown');
        $this.countdown(finalDate, function (event) {
            $this.html(event.strftime('<span>%DD : </span> <span>%HH : </span>  <span>%MM : </span> <span>%SS</span>'));
        });
    });

    if ( $(window).width() > 991 ) {
        // Game Slider
        initGameSlider();
    }

    if ( $(window).width() < 991 ) {
        // last winner Slider
        initLastWinnerSlider();
    }



    // payment Slider
    var $method_slider = $('.method-slider');
    $method_slider.owlCarousel({
        loop: true,
        navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
        nav: true,
        dots: false,
        autoplay: false,
        margin: 0,
        autoplayTimeout: 6000,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 2
            },
            500: {
                items: 3
            },
            768: {
                items: 5
            },
            992: {
                items: 6
            },
            1200: {
                items: 7
            },
            1920: {
                items: 7
            }
        }
    });

    // fix for signin: when we open modal from modal - remove class from body
    $('#signin').on('shown.bs.modal', function () {
        $('body').addClass('modal-open')
    })
    modalToggle();

    //sub-footer-slider
    $('.js-sub-footer-slider-slider').owlCarousel({
        rtl: true,
        loop: true,
        nav: false,
        dots: false,
        smartSpeed: 1000,
        items: 1,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
    });

    // testimonial-slider
    var $testimonial_slider = $('.testimonial-slider');
    $testimonial_slider.owlCarousel({
        loop: true,
        navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
        nav: true,
        dots: false,
        autoplay: false,
        margin: 30,
        autoplayTimeout: 6000,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            960: {
                items: 1
            },
            1200: {
                items: 1
            }
        }
    });


});

function initGameSlider () {
    var $game_slider = $('.game-slider');
    $game_slider.owlCarousel({
        rtl: true,
        loop: true,
        navText: ['<span class="game-slider__nav-prev"></span>', '<span class="game-slider__nav-next"></span>'],
        nav: true,
        dots: false,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        margin: 0,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 1
            },
            500: {
                items: 1
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            },
            1200: {
                items: 3
            },
            1920: {
                items: 3
            }
        }
    });
}

function initLastWinnerSlider () {
    var $lastWinnerSlider = $('.js-last-winner-list');
    $lastWinnerSlider.owlCarousel({
        rtl: true,
        loop: true,
        navText: ['<span class="list-winner__nav-prev"></span>', '<span class="list-winner__nav-next"></span>'],
        nav: true,
        dots: true,
        smartSpeed: 1000,
        items: 1,
        autoplay: true,
        autoplayTimeout: 300000,
        autoplayHoverPause: true,
    });
}
  


    /*-------------------------------
        back to top
    ------------------------------*/
    $(document).on('click', '.bottomtotop', function () {
        $("html,body").animate({
            scrollTop: 0
        }, 2000);
    });

    //define variable for store last scrolltop
    var lastScrollTop = '';
    $(window).on('scroll', function () {
        var $window = $(window);
        if ($window.scrollTop( ) > 0 ) {
            $(".header").addClass('nav-fixed');
        } else {
            $(".header").removeClass('nav-fixed');
        }

        /*---------------------------
            back to top show / hide
        ---------------------------*/
        var st = $(this).scrollTop();
        var ScrollTop = $('.bottomtotop');
        if ($(window).scrollTop() > 1000) {
            ScrollTop.fadeIn(1000);
        } else {
            ScrollTop.fadeOut(1000);
        }
        lastScrollTop = st;

    });

    $(window).on('load', function () {
  
    /*---------------------
        Preloader
    -----------------------*/
    var preLoder = $("#preloader");
    preLoder.addClass('hide');
    var backtoTop = $('.back-to-top');
    /*-----------------------------
        back to top
    -----------------------------*/
    var backtoTop = $('.bottomtotop');
    backtoTop.fadeOut(100);
    
    });



    
    /*-----------------------------
        Cart Page Quantity 
    -----------------------------*/
    $(document).on('click', '.qtminus', function () {
        var el = $(this);
        var $tselector = el.parent().parent().find('.qttotal');
        total = $($tselector).text();
        if (total > 1) {
            total--;
        }
        $($tselector).text(total);
    });

    $(document).on('click', '.qtplus', function () {
        var el = $(this);
        var $tselector = el.parent().parent().find('.qttotal');
        total = $($tselector).text();
        if(stock != "")
        {
            var stk = parseInt(stock);
              if(total < stk)
              {
                 total++;
                 $($tselector).text(total);              
              }
        }
        else {
        total++;            
        }

        $($tselector).text(total);
    });

   

});

function modalToggle () {
    var modalLogin = $('#login');
    var modalRecovery = $('#recovery');
    var modalRegister = $('#signin');
    var mobMenu = $('.js-mob-menu');

    $(".js-register-modal-open").click(function(e) {
        e.preventDefault();

        modalLogin.modal('hide');
        modalRecovery.modal('hide');

        mobMenu.collapse('hide');

        modalRegister.modal('show');
    });

    $(".js-login-modal-open").click(function(e) {
        e.preventDefault();

        modalRecovery.modal('hide');
        modalRegister.modal('hide');

        mobMenu.collapse('hide');

        modalLogin.modal('show');
    });
}