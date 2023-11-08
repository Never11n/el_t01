$(function ($) {
    turnFormType();
    turnPrice();
    $('.number-block-line').on('click', function() {
        const currentBlock = $(this).data('block');
        turnBlockHiddenInput(currentBlock);
        turnFormType();
    });
    // Price block
    $('.ui-game-circle-input-price').on('click', function () {
        if ($(this).val() === 'own') {
            $('.own-price-block').attr("hidden", false);
            $("#price").val($('.own-price-block-input').val());
        }
        else {
            $('.own-price-block').attr("hidden", true);
            $("#price").val($(this).val());
        }
        calcTotalSum123();
    });
    $('.own-price-block-input').on('input', function () {
        $("#price").val($('.own-price-block-input').val());
        calcTotalSum123();
    });
    // Select automatic
    $('.js-game-auto').on('click', function () {
        const numbersArray = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
              currentBlock = $(this).data('block'),
              line1 = $(`input[name=number-block${currentBlock}-line1]`),
              line2 = $(`input[name=number-block${currentBlock}-line2]`),
              line3 = $(`input[name=number-block${currentBlock}-line3]`);
        let random = numbersArray[Math.floor(Math.random() * 10)];
        line1.each(function (index, item) {
            if (+$(item).val() === random) {
                $(item).prop('checked', true);
            }
        });
        random = numbersArray[Math.floor(Math.random() * 10)];
        line2.each(function (index, item) {
            if (+$(item).val() === random) {
                $(item).prop('checked', true);
            }
        });
        random = numbersArray[Math.floor(Math.random() * 10)];
        line3.each(function (index, item) {
            if (+$(item).val() === random) {
                $(item).prop('checked', true);
            }
        });
        turnBlockHiddenInput(currentBlock);
        turnFormType();

    });
    // Reset block
     $('.js-game-reset').on('click', function () {
        const currentBlock = $(this).data('block'),
              line1 = $(`input[name=number-block${currentBlock}-line1]`),
              line2 = $(`input[name=number-block${currentBlock}-line2]`),
              line3 = $(`input[name=number-block${currentBlock}-line3]`);
        line1.each(function (index, item) {
            $(item).prop('checked', false);
        });
        line2.each(function (index, item) {
            $(item).prop('checked', false);
        });
        line3.each(function (index, item) {
            $(item).prop('checked', false);
        });
        turnBlockHiddenInput(currentBlock);
        turnFormType();
     });

     $('.js-subs-day').on('click', function () {
        const allDays = $('.js-subs-day-block').find('.js-subs-day'),
              thisDay = $(this),
              thisDayNum = thisDay.data('day'),
              isSubscription = $('#subscription');
        isSubscription.val('1');
        allDays.removeClass('ui-game-lotto-row-line-number_selected');
        thisDay.addClass('ui-game-lotto-row-line-number_selected');
        $('#subscription_day').val(thisDayNum);
        $('.btn_subscribe').each(function (index, item) {
        if ($(item).val() === '1') {
            $(item).prop('checked', true);
        }
        });
         $('.js-balance-payment-method-hide').attr("hidden", true);
         $('.js-balance-payment-method-hide').find('.single-method.active').removeClass('active');
         $($('.js-other-payment-methods').find('.single-method')[0]).addClass('active');
        calcTotalSum123();
    });
     $('.btn_subscribe').on('click', function () {
        const isSubscription = $('#subscription'),
              allDays = $('.js-subs-day-block').find('.js-subs-day');
        if (isSubscription.val() === '0') {
            isSubscription.val('1');
            // $('#id_btn_subscribe').html(gettext("Don't subscribe"));
            // $('.js-subs-days-hidden-block').attr("hidden", false);
            $('.js-balance-payment-method-hide').attr("hidden", true);
            $('.js-balance-payment-method-hide').find('.single-method.active').removeClass('active');
            $($('.js-other-payment-methods').find('.single-method')[0]).addClass('active');
        } else {
            isSubscription.val('0');
            // $('#id_btn_subscribe').html(gettext("Subscribe"));
            // $('.js-subs-days-hidden-block').attr("hidden", true);
            allDays.removeClass('ui-game-lotto-row-line-number_selected');
            $('#subscription_day').val('');
            $('.js-balance-payment-method-hide').attr("hidden", false);
            $('.js-balance-payment-method-hide').find('.single-method').addClass('active');
            $('.js-other-payment-methods').find('.single-method').removeClass('active');
        }
        calcTotalSum123();
    });
     $('input[name=automatic-same]').on('click', function () {
        if ($(this).val() === '1') {
            $('#subscription_automatic').val(1);
        } else {
            $('#subscription_automatic').val(0);
        }
    });

});

function turnBlockHiddenInput(currentBlock) {
    console.log('turnBlockHiddenInput', currentBlock);
    const line1 = $(`input[name=number-block${currentBlock}-line1]:checked`).val(),
          line2 = $(`input[name=number-block${currentBlock}-line2]:checked`).val(),
          line3 = $(`input[name=number-block${currentBlock}-line3]:checked`).val(),
          blockHiddenInput = $(`#block${currentBlock}`);
    if (line1 && line2 && line3) {
        blockHiddenInput.val(`${line1}${line2}${line3}`);
    } else {
        blockHiddenInput.val('');
    }
}

function turnPrice() {
    const price = $('#price').val();
    $('.ui-game-circle-input-price').each(function (index, item) {
        $(item).prop('checked', false);
        if ($(item).val() === price) {
            $(item).prop('checked', true);
        }
    });

}
function turnFormType() {
    const blocks = [1, 2, 3, 4, 5];
    let filledBlocks = 0;
    blocks.forEach(function (block) {
        let filledLines = 0;
        if ($(`input[name=number-block${block}-line1]:checked`).val()) {
            filledLines++;
        }
        if ($(`input[name=number-block${block}-line2]:checked`).val()) {
            filledLines++;
        }
        if ($(`input[name=number-block${block}-line3]:checked`).val()) {
            filledLines++;
        }
        if (filledLines === 3) {
            filledBlocks++;
        }
    });

    const formTypeHidden = $('#form_type'),
          formTypeRadios = $('.ui-game-circle-input-form-type');
    if (filledBlocks=== 0) {
        formTypeHidden.val(1);
    } else {
        formTypeHidden.val(filledBlocks);
    }
    formTypeRadios.each(function (index, item) {
        if (+$(item).val() === filledBlocks) {
            $(item).prop('checked', true);
        }
    });
    calcTotalSum123();
}

function calcTotalSum123() {
    const totalSumBlock = $('#sum_block'),
          totalSumInput = $('#total_sum');
    $.ajax({
        type: "POST",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            ticket_type: $('#game_version').val(),
            form_type: $('#form_type').val(),
            price: $('#price').val(),
            is_subscription: $('#subscription').val(),
            subscription_days: $('#subscription_day').val()
        },
        url: "/calc_game_lotto_sum/",
        success: function (res) {
            if (res.AnswerCod === '01') {
                totalSumBlock.html(res.AnswerText);
                totalSumInput.val(res.AnswerText);
            }
        },
    });
}

function game123Save() {
    const game_version = $("#game_version").val(),
          game_type = $('#game_type').val(),
          form_type = $("#form_type").val(),
          block1 = $(`#block1`).val(),
          block2 = $(`#block2`).val(),
          block3 = $(`#block3`).val(),
          block4 = $(`#block4`).val(),
          block5 = $(`#block5`).val(),
          price = $("#price").val(),
          games_count = $("#games_count").val(),
          total_sum = $('#total_sum').val(),
          pay_method = $('.payment-method').find('.single-method.active');
    let m_pay_method = '';
    if (pay_method) {
        m_pay_method = pay_method.data('paymethod');
    }
    $.ajax({
        type: "POST",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            f_game_version: game_version,
            f_game_type: game_type,
            f_form_type: form_type,
            f_block1: block1,
            f_block2: block2,
            f_block3: block3,
            f_block4: block4,
            f_block5: block5,
            f_price: price,
            f_games_count: games_count,
            f_total_sum: total_sum,
            f_pay_method: m_pay_method,
            f_is_subscription: $('#subscription').val(),
            f_subscription_days: $('#subscription_day').val(),
            f_subscription_automatic: $('#subscription_automatic').val()
        },
        url: "/cab-game-lotto-save/",
        success: function (res) {
            if (res.AnswerCod === '01') {
                location.href = res.AnswerHref;
            } else {
                Swal.fire({
                    icon: 'error',
                    title: gettext('ERROR'),
                    background: '#cacaca',
                    html: res.AnswerText,
                    confirmButtonText: gettext('Back to form'),
                    confirmButtonColor: '#dd3333',
                });
                return false;
            }
            },
            error: function (res) {
                Swal.fire({
                    icon: 'error',
                    title: gettext('ERROR'),
                    background: '#cacaca',
                    html: gettext("An error occured, please try again later."),
                    confirmButtonText: gettext('Back to form'),
                    confirmButtonColor: '#dd3333',
                });
                return false;
            }
        });
}

function gameSave() {
    if ($('#subscription').val() === '1') {
        let games,
            numbers = '';
        if ($('#subscription_day').val() === 'infinity') {
            games = gettext('Infinity');
        } else {
            games = $('#subscription_day').val();
        }
        if ($('#subscription_automatic').val() === '1') {
            numbers += `${$("#form_type").val()} `
            numbers += gettext('blocks of numbers will be inserted automatically');
        } else {
            numbers = gettext('Same numbers');
        }
        const text = `${gettext('Games count')}: ${games} <br>
                      ${gettext('Numbers')}: ${numbers}`;
        Swal.fire({
            icon: 'warning',
            title: gettext("Please check the details of subscription."),
            html: text,
            showCancelButton: true,
            confirmButtonColor: "#15b284",
            cancelButtonColor: "#DD6B55",
            confirmButtonText: gettext("Yes"),
            cancelButtonText: gettext("No"),
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                game123Save();
            }
         });
    }
    else {
       game123Save();
   }
}