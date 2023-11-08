$(function ($) {
    gemaTimer();
    gemaSliderPrice();
    setGameThemeColor();
    // initCheckboxMaxCount();
});

function gemaTimer () {
    const  gameTimer =  $( ".js-ui-game-timer" );

    if (!gameTimer) {
        return false
    }

    const timerEnd = gameTimer.data( "timer-sec" );
    const upgradeTime = timerEnd;
    let seconds = upgradeTime;

    const countdownTimer = setInterval(timer, 1000);

    function timer() {
        const days        = Math.floor(seconds/24/60/60);
        const hoursLeft   = Math.floor((seconds) - (days*86400));
        const hours       = Math.floor(hoursLeft/3600);
        const minutesLeft = Math.floor((hoursLeft) - (hours*3600));
        const minutes     = Math.floor(minutesLeft/60);
        const remainingSeconds = seconds % 60;

        $( ".js-game-timer-days" ).text(pad(days));
        $( ".js-game-timer-hours" ).text(pad(hours));
        $( ".js-game-timer-min" ).text(pad(minutes));
        $( ".js-game-timer-sec" ).text(pad(remainingSeconds));

        if (seconds == 0) {
            clearInterval(countdownTimer);
        } else {
            seconds--;
        }
    }

    function pad(n) {
        return (n < 10 ? "0" + n : n);
    }
}

function gemaSliderPrice () {
    const slider = $('.js-ui-game-price-slider');

    if (!slider) {
        return false
    }

    slider.owlCarousel({
        loop: true,
        navText: ['<i class="fa fa-caret-left"></i> ', '<i class="fa fa-caret-right"></i>'],
        nav: true,
        dots: false,
        center: true,
        autoplay: false,
        margin: 0,
        items: 3,
    });

    // Listen to owl events:
    slider.on('changed.owl.carousel', function(event) {
        const all_items = event.target.querySelectorAll('.owl-item'),
              current_item = all_items[event.item.index].querySelector('p'),
              price = current_item.dataset.price,
              game_type = $('#game_type').val();
        $('#price').val(price);
        if (game_type === "chance") {
            calcTotalSumChance();
        }

    })
}

function setGameThemeColor() {
    const gameThemeColorElem =  $( ".js-game-theme-color" );

    if (!gameThemeColorElem) {
        return false
    }

    const gameThemeColor = gameThemeColorElem.data( "game-theme-color" ) || '#60DBA5';
    const gameThemeColorRgb = gameThemeColorElem.data( "game-theme-color-rgb" ) || '96, 219, 165';

    const rootElem = document.querySelector(':root');

    rootElem.style.setProperty('--lotto-color', gameThemeColor);
    rootElem.style.setProperty('--lotto-color-rgb', gameThemeColorRgb);
}
//
// function initCheckboxMaxCount() {
//     const maxCount = $('.js-ui-game-count-selected-checkbox').data('max-count-selected-checkbox');
//
//     $('.js-ui-game-count-selected-checkbox input[type=checkbox]').on('change', function () {
//         if(this.checked) {
//             const currentCount = $(".js-ui-game-count-selected-checkbox input[type=checkbox]:checked").length;
//             if (maxCount < currentCount) {
//                 $(this).prop('checked',false);
//             }
//             return;
//         }
//     })
// }