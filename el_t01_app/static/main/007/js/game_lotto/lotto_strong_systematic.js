$(function ($) {
    initSameTicket();
    calcTotalSumLotto();
    $('.js-ui-game-lotto-modal-open').on('click', function () {
        closeGameModal('js-ui-game-lotto-modal-2');
        $('.game-modal__body').find('.ui-game-ball-input').removeClass('js-game-ball-input-selected');
        highlightNumbers();
        openGameModal('js-ui-game-lotto-modal');
    });

    $('.js-ui-game-lotto-modal-2-open').on('click', function () {
        closeGameModal('js-ui-game-lotto-modal');
        $('.game-modal__body').find('.ui-game-ball-input').removeClass('js-game-ball-input-selected');
        highlightNumbers(true);
        openGameModal('js-ui-game-lotto-modal-2');
    });

    $('.js-game-modal-save').on('click', function () {
        closeAllModals();
    });


    $('.js-extra-button').on('click', function () {
        const extraCheckbox = $('#is_extra_btn'),
            extraHiddenInput = $('#is_extra');
        if (extraCheckbox.prop('checked') === true) {
            extraCheckbox.prop('checked', false);
            extraHiddenInput.val(0);
        } else {
            extraCheckbox.prop('checked', true);
            extraHiddenInput.val(1);
        }
        calcTotalSumLotto();
    });
    $("#is_extra_btn").click(function (event) {
        event.stopPropagation();
        const extraHiddenInput = $('#is_extra');
        if (this.checked) {
            extraHiddenInput.val(1);
        } else {
            extraHiddenInput.val(0);
        }
        calcTotalSumLotto();
    });

    $('input[name=regular-double]').on('click', function () {
        closeAllModals();
        if ($(this).val() === 'regular') {
            $('#is_double').val(0);
        } else {
            $('#is_double').val(1);
        }
        calcTotalSumLotto();
    });
    $('.js-input-form-type').on('click', function () {
        const formTypeVal = $(this).val();
        turnFormType(formTypeVal);
        calcTotalSumLotto();
    });

     $('.js-game-reset').on('click', function () {
        const whatDelete = $(this).attr('data-reset');
        reset( whatDelete);
    });

     $('.ui-game-ball-input-line').on('click', function () {
        const thisLine = $(this),
              lineValue = thisLine.val(),
              lineInput = '#nums_line',
              countNumbers = selectedNumbersArray().length,
              game_version = $('#game_version').val();
        let formTypeVal;
        if (game_version === 'lotto_systematic') {
            formTypeVal = $('#form_type').val();
        } else {
            formTypeVal = 7;
        }
        if ($(lineInput).val().includes(`${lineValue};`)) {
            thisLine.removeClass('js-game-ball-input-selected');
            let old_val = $(lineInput).val();
            let new_val = old_val.replace(`${lineValue};`, '');
            $(lineInput).val(new_val);
        } else {
            if (countNumbers < +formTypeVal){
                thisLine.addClass('js-game-ball-input-selected');
                let old_val = $(lineInput).val();
                let new_val = sortedNumbers(old_val + `${lineValue};`);
                $(lineInput).val(new_val);
            }
        }
        turnNumbers(game_version);

    });

     $('.js-game-auto').on('click', function () {
         const game_version = $('#game_version').val();
         autoGame(game_version);
     });

     $('.ui-game-ball-input-strong').on('click', function () {
        const thisStrong = $(this),
              strongValue = thisStrong.val(),
              formTypeVal = $('#form_type').val(),
              strongInput = '#nums_strong',
              game_version = $('#game_version').val(),
              countNumbers = selectedNumbersArray(true).length;
        if (game_version === 'lotto_systematic') {
            if ($(strongInput).val() === strongValue) {
                thisStrong.removeClass('js-game-ball-input-selected');
                $(strongInput).val('');
            } else {
                $('.game-modal__body').find('.ui-game-ball-input').removeClass('js-game-ball-input-selected');
                thisStrong.addClass('js-game-ball-input-selected');
                $(strongInput).val(strongValue);
            }
        } else {
            if ($(strongInput).val().includes(`${strongValue};`)) {
                thisStrong.removeClass('js-game-ball-input-selected');
                let old_val = $(strongInput).val();
                let new_val = old_val.replace(`${strongValue};`, '');
                $(strongInput).val(new_val);
            } else {
                if (countNumbers < +formTypeVal){
                    thisStrong.addClass('js-game-ball-input-selected');
                    let old_val = $(strongInput).val();
                    let new_val = sortedNumbers(old_val + `${strongValue};`, true);
                    $(strongInput).val(new_val);
                }
            }
        }
        turnNumbers(game_version);

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
        calcTotalSumLotto();
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
        calcTotalSumLotto();
    });
     $('input[name=automatic-same]').on('click', function () {
        if ($(this).val() === '1') {
            $('#subscription_automatic').val(1);
        } else {
            $('#subscription_automatic').val(0);
        }
    });
});


function turnFormType(formTypeVal) {
    const game_version = $('#game_version').val();
        $('#form_type').val(formTypeVal);
        if (game_version === 'lotto_systematic') {
            const lineInput = '#nums_line',
                  numbersArr = selectedNumbersArray(),
                  countNumbers = numbersArr.length;
            if (countNumbers > formTypeVal) {
                let new_val = '';
                numbersArr.forEach(function (val, idx) {
                    if (idx < +formTypeVal) {
                        new_val += `${val};`;
                    }
                });
                $(lineInput).val(new_val);
            }
            const allCols = $('.js-ui-game-lotto-modal-open');
            allCols.each(function (index, item) {
                if (index < +formTypeVal) {
                    $(item).removeClass('ui-game-ball-lotto-not-active');
                } else {
                    $(item).addClass('ui-game-ball-lotto-not-active');
                    $(item).html('');
                }
            })
        } else {
            const strongInput = '#nums_strong',
                  numbersArr = selectedNumbersArray(true),
                  countNumbers = numbersArr.length;
            if (countNumbers > formTypeVal) {
                let new_val = '';
                numbersArr.forEach(function (val, idx) {
                    if (idx < +formTypeVal) {
                        new_val += `${val};`;
                    }
                });
                $(strongInput).val(new_val);
            }
            const allCols = $('.js-ui-game-lotto-modal-2-open');
            allCols.each(function (index, item) {
                if (index < +formTypeVal) {
                    $(item).removeClass('ui-game-ball_light-not-active');
                } else {
                    $(item).addClass('ui-game-ball_light-not-active');
                    $(item).html('');
                }
            })
        }
}
function turnNumbers(game_version) {
    const allCols = $('.js-ui-game-lotto-modal-open'),
          allStrongs = $('.js-ui-game-lotto-modal-2-open'),
          selectedNumsCols = selectedNumbersArray(),
          selectedNumsStrong = selectedNumbersArray(true),
          formTypeVal = $('#form_type').val();
    if (game_version === 'lotto_systematic') {
        for (let i=0; i < formTypeVal; i++) {
            let div = allCols[i],
                value = selectedNumsCols[i];
            if (value) {
                if (value[0] === '0') {
                    value = value[1];
                }
                $(div).html(value);
            } else {
                $(div).html('');
            }
        }
        $(allStrongs[0]).html(selectedNumsStrong);
    } else {
        for (let i=0; i < 7; i++) {
            let div = allCols[i],
                value = selectedNumsCols[i];
            if (value) {
                if (value[0] === '0') {
                    value = value[1];
                }
                $(div).html(value);
            } else {
                $(div).html('');
            }
        }
        for (let i=0; i < formTypeVal; i++) {
            let div = allStrongs[i],
                value = selectedNumsStrong[i];
            if (value) {
                if (value[0] === '0') {
                    value = value[1];
                }
                $(div).html(value);
            } else {
                $(div).html('');
            }
        }
    }
    calcTotalSumLotto();
}

function autoGame(game_version) {
    closeAllModals();
    const numbersArray = ['01;', '02;', '03;', '04;', '05;', '06;', '07;', '08;', '09;', '10;', '11;', '12;', '13;',
              '14;', '15;', '16;', '17;', '18;', '19;', '20;', '21;', '22;', '23;', '24;', '25;', '26;', '27;',
              '28;', '29;', '30;', '31;', '32;', '33;', '34;', '35;', '36;', '37;'],
          strongArray = ['1;', '2;', '3;', '4;', '5;', '6;', '7;'],
          formTypeVal = $('#form_type').val(),
          lineInput = '#nums_line',
          strongInput = '#nums_strong',
          randomStrong = strongArray[Math.floor(Math.random() * 7)];
    if (game_version === 'lotto_systematic') {
        let resultLine = '';
        for (let i=0; i< +formTypeVal; i++) {
            let random = numbersArray[Math.floor(Math.random() * 37)]
            while (resultLine.includes(random)) {
                random = numbersArray[Math.floor(Math.random() * 37)]
            }
            resultLine += random;
        }
        $(strongInput).val(randomStrong);
        const newValLine = sortedNumbers(resultLine);
        $(lineInput).val(newValLine);
    } else {
        let resultStrongLine = '';
        for (let i=0; i< +formTypeVal; i++) {
            let random = strongArray[Math.floor(Math.random() * 7)]
            while (resultStrongLine.includes(random)) {
                random = strongArray[Math.floor(Math.random() * 7)]
            }
            resultStrongLine += random;
        }
        const newValStrongLine = sortedNumbers(resultStrongLine, true);
        $(strongInput).val(newValStrongLine);
        let resultLine = '';
        for (let i=0; i< 7; i++) {
            let random = numbersArray[Math.floor(Math.random() * 37)]
            while (resultLine.includes(random)) {
                random = numbersArray[Math.floor(Math.random() * 37)]
            }
            resultLine += random;
        }
        const newValLine = sortedNumbers(resultLine);
        $(lineInput).val(newValLine);
    }
    turnNumbers(game_version);

}

function reset(whatDelete) {
    closeAllModals();
    const allCols = $('.js-ui-game-lotto-modal-open'),
          allStrongs = $('.js-ui-game-lotto-modal-2-open'),
          lineInput = '#nums_line',
          strongInput = '#nums_strong';
    if (whatDelete === 'line') {
        $(lineInput).val('');
        for (let i=0; i<allCols.length; i++) {
            let div = allCols[i];
            $(div).html('');
        }
    } else if (whatDelete === 'strong') {
        $(strongInput).val('');
        for (let i=0; i<allStrongs.length; i++) {
            let div = allStrongs[i];
            $(div).html('');
        }
    } else {
        $(strongInput).val('');
        for (let i=0; i<allStrongs.length; i++) {
            let div = allStrongs[i];
            $(div).html('');
        }
        $(lineInput).val('');
        for (let i=0; i<allCols.length; i++) {
            let div = allCols[i];
            $(div).html('');
        }
    }
    calcTotalSumLotto();
}

function selectedNumbersArray(strongs=false) {
    let cleanedLineInputArray = [];
    let lineInput;
    if (strongs) {
        lineInput = $('#nums_strong').val();
    } else {
        lineInput = $('#nums_line').val();
    }
    if (lineInput) {
        const lineInputArray = lineInput.split(';');
        cleanedLineInputArray = lineInputArray.filter(function(elem) {
            return elem !== '';
        });
    }
    return cleanedLineInputArray;
}

function sortedNumbers(str, strongs=false) {
    let numbersArray = ['01;', '02;', '03;', '04;', '05;', '06;', '07;', '08;', '09;', '10;', '11;', '12;', '13;', '14;',
        '15;', '16;', '17;', '18;', '19;', '20;', '21;', '22;', '23;', '24;', '25;', '26;', '27;', '28;', '29;', '30;',
        '31;', '32;', '33;', '34;', '35;', '36;', '37;'];
    if (strongs) {
        numbersArray = ['1;', '2;', '3;', '4;', '5;', '6;', '7;'];
    }
    let result = '';
    numbersArray.forEach(elem => {
        if (str.includes(elem)) {
            result += elem;
        }
    });
    return result;
}

function highlightNumbers( strong=false) {
    if (strong) {
        const selectedStrong =  selectedNumbersArray(true);
        if (selectedStrong.length !== 0) {
            for (let i = 0; i < selectedStrong.length; i++) {
                $('[data-number-value="' + selectedStrong[i] + '"]').addClass('js-game-ball-input-selected');
            }
        }
    } else {
         const selectedNums = selectedNumbersArray();
         if (selectedNums.length !== 0) {
            for (let i = 0; i < selectedNums.length; i++) {
                $('[data-number-value="' + selectedNums[i] + '"]').addClass('js-game-ball-input-selected');
            }
        }
    }
}

function openGameModal(modalId) {
    $('[data-modal-id="'+modalId+'"]').addClass('game-modal__open');
    $('body').addClass('modal-open');
}

function closeGameModal(modalId) {
    $('[data-modal-id="'+modalId+'"]').removeClass('game-modal__open');
    $('body').removeClass('modal-open');
}

function closeAllModals() {
    closeGameModal('js-ui-game-lotto-modal-2');
    closeGameModal('js-ui-game-lotto-modal');
}


function calcTotalSumLotto() {
    const totalSumBlock = $('#sum_block'),
          totalSumInput = $('#total_sum'),
          formType = $('#form_type').val(),
          isDouble = $('#is_double').val(),
          isExtra = $('#is_extra').val();
    $.ajax({
        type: "POST",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            ticket_type: $('#game_version').val(),
            is_double: isDouble,
            is_extra: isExtra,
            form_type: formType,
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


function gameLottoSave() {
    const gameVersion = $('#game_version').val(),
          gameType = $('#game_type').val(),
          gamesCount = $('#games_count').val(),
          formType = $('#form_type').val(),
          totalSum = $('#total_sum').val(),
          isExtra = $('#is_extra').val(),
          isDouble = $('#is_double').val(),
          nums_line = $('#nums_line').val(),
          nums_strong = $('#nums_strong').val(),
          payMethod = $('.payment-method').find('.single-method.active'),
          selected_nums_line = selectedNumbersArray(),
          selected_nums_strong = selectedNumbersArray(true);
    let m_pay_method = '';
    if (payMethod) {
        m_pay_method = payMethod.data('paymethod');
    }
    if (gameVersion === 'lotto_systematic') {
        if (selected_nums_line.length < +formType || selected_nums_strong.length === 0) {
            Swal.fire({
            icon: 'error',
            title: gettext('ERROR'),
            background: '#cacaca',
            html: gettext("Please fill in the numbers and strong number"),
            confirmButtonText: gettext('Back to form'),
            confirmButtonColor: '#d33',
            });
            return false;
        }
    } else {
        if (selected_nums_line.length < 7 || selected_nums_strong.length < +formType) {
            Swal.fire({
            icon: 'error',
            title: gettext('ERROR'),
            background: '#cacaca',
            html: gettext("Please fill in the numbers and strong numbers"),
            confirmButtonText: gettext('Back to form'),
            confirmButtonColor: '#d33',
            });
            return false;
        }
    }
    $.ajax({
            type: "POST",
            async: false,
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                f_game_version: gameVersion,
                f_game_type: gameType,
                f_is_extra: isExtra,
                f_is_double: isDouble,
                f_games_count: gamesCount,
                f_total_sum: totalSum,
                f_pay_method: m_pay_method,
                f_form_type: formType,
                f_nums_line: nums_line,
                f_nums_strong: nums_strong,
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


function initSameTicket() {
    const form_type_radios = $('.js-input-form-type'),
          form_type_hidden = $('#form_type').val(),
          game_version = $('#game_version').val(),
          extraHiddenInput = $('#is_extra').val(),
          extraCheckbox = $('#is_extra_btn'),
          isDouble = $('#is_double').val();
    turnNumbers(game_version);

    form_type_radios.each(function (index, item) {
        if ($(item).val() === form_type_hidden) {
            $(item).prop('checked', true);
        }
    });
    turnFormType(form_type_hidden);
    if (extraHiddenInput === '1') {
        extraCheckbox.prop('checked', true);
    }
    if (isDouble === '1') {
        $('#double_btn').prop('checked', true);
    }
}

function gameSave() {
    if ($('#subscription').val() === '1') {
        let games,
            numbers = '',
            form_type = $('#form_type').val(),
            extra,
            double;
        if ($('#game_version').val() === 'lotto_systematic' && +form_type === 5) {
            form_type = '5=6'
        }
        if ($('#is_extra').val() === '1') {
            extra = gettext('Yes');
        } else {
            extra = gettext('No');
        }
        if ($('#subscription_automatic').val() === '1') {
            numbers += gettext('Numbers will be inserted automatically');
        } else {
            numbers = gettext('Same numbers');
        }
        if ($('#is_double').val() === '1') {
            double = gettext('Yes');
        } else {
            double = gettext('No');
        }
        if ($('#subscription_day').val() === 'infinity') {
            games = gettext('Infinity');
        } else {
            games = $('#subscription_day').val();
        }
        const text = `${gettext('Games count')}: ${games} <br>
                      ${gettext('Form type')}: ${form_type} <br>
                      ${gettext('Numbers')}: ${numbers} <br>
                      ${gettext('Extra')}: ${extra} <br>
                      ${gettext('Double')}: ${double}`
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
                gameLottoSave();
            }
         });
    }
    else {
       gameLottoSave();
   }
}