$(function ($) {
    initSameTicket();
    calcTotalSum777();
    // 777 modal
    $('.js-ui-game-777-modal-open').on('click', function () {
        const line = $(this).data('line');
        $('.js-selected-line').attr("data-selected-line", line);
        $('.js-modal-reset-button-line').attr("data-line", line);
        $('.game-modal__body').find('.ui-game-ball-input').removeClass('js-game-ball-input-selected');
        highlightNumbers(line);
        openGameModal('js-ui-game-777-modal');
    });
    $('.js-game-modal-save').on('click', function () {
        closeGameModalChance()
    });
    $('.js-game-modal-close').on('click', function () {
        closeGameModal();
    });

    $('.ui-game-ball-input').on('click', function () {
        const thisLine = $(this),
              lineValue = thisLine.val(),
              countCols = $('#count_cols').val(),
              currentLine = $('.js-selected-line').attr('data-selected-line'),
              lineInput = `#nums_line_${currentLine}`,
              countNumbers = selectedNumbersArray(currentLine).length;
        if ($(lineInput).val().includes(`${lineValue};`)) {
                thisLine.removeClass('js-game-ball-input-selected');
                let old_val = $(lineInput).val();
                let new_val = old_val.replace(`${lineValue};`, '');
                $(lineInput).val(new_val);
            } else {
                if (countNumbers < +countCols){
                thisLine.addClass('js-game-ball-input-selected');
                let old_val = $(lineInput).val();
                let new_val = sortedNumbers(old_val + `${lineValue};`);
                $(lineInput).val(new_val);
                }
            }
        turnNumbers(currentLine);
        turnFormType();
    });
    $('.js-game-reset').on('click', function () {
        const currentLine = $(this).data('line'),
              allCols = $('[data-line-num="' + currentLine + '"]').children(),
              lineInput = `#nums_line_${currentLine}`;
        $(lineInput).val('');
        for (let i=0; i<allCols.length; i++) {
            let div = allCols[i];
            $(div).html('');
        }
        turnFormType();
    });

    $('.js-game-auto').on('click', function () {
        const currentLine = $(this).data('line'),
              lineInput = `#nums_line_${currentLine}`,
              countCols = $('#count_cols').val(),
              numbersArray = ['01;', '02;', '03;', '04;', '05;', '06;', '07;', '08;', '09;', '10;', '11;', '12;', '13;',
                  '14;', '15;', '16;', '17;', '18;', '19;', '20;', '21;', '22;', '23;', '24;', '25;', '26;', '27;',
                  '28;', '29;', '30;', '31;', '32;', '33;', '34;', '35;', '36;', '37;', '38;', '39;', '40;', '41;',
                  '42;', '43;', '44;', '45;', '46;', '47;', '48;', '49;', '50;', '51;', '52;', '53;', '54;', '55;',
                  '56;', '57;', '58;', '59;', '60;', '61;', '62;', '63;', '64;', '65;', '66;', '67;', '68;', '69;', '70;'];
        let result = '';
        for (let i=0; i< +countCols; i++) {
            let random = numbersArray[Math.floor(Math.random() * 70)]
            while (result.includes(random)) {
                random = numbersArray[Math.floor(Math.random() * 70)]
            }
            result += random;
        }
        const new_val = sortedNumbers(result);
        $(lineInput).val(new_val);
        turnNumbers(currentLine);
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
        calcTotalSum777();
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
        calcTotalSum777();
    });
    $('input[name=automatic-same]').on('click', function () {
        if ($(this).val() === '1') {
            $('#subscription_automatic').val(1);
        } else {
            $('#subscription_automatic').val(0);
        }
    });
});

function selectedNumbersArray(lineNumber) {
    let cleanedLineInputArray = [];
    const lineInput = $(`#nums_line_${lineNumber}`).val();
    if (lineInput) {
        const lineInputArray = lineInput.split(';');
        cleanedLineInputArray = lineInputArray.filter(function(elem) {
            return elem !== '';
        });
    }
    return cleanedLineInputArray;
}
function sortedNumbers(str) {
    const numbersArray = ['01;', '02;', '03;', '04;', '05;', '06;', '07;', '08;', '09;', '10;', '11;', '12;', '13;', '14;',
        '15;', '16;', '17;', '18;', '19;', '20;', '21;', '22;', '23;', '24;', '25;', '26;', '27;', '28;', '29;', '30;',
        '31;', '32;', '33;', '34;', '35;', '36;', '37;', '38;', '39;', '40;', '41;', '42;', '43;', '44;', '45;', '46;',
        '47;', '48;', '49;', '50;', '51;', '52;', '53;', '54;', '55;', '56;', '57;', '58;', '59;', '60;', '61;', '62;',
        '63;', '64;', '65;', '66;', '67;', '68;', '69;', '70;'];
    let result = '';
    numbersArray.forEach(elem => {
        if (str.includes(elem)) {
            result += elem;
        }
    });
    return result;
}

function turnNumbers(lineNumber) {
    const allCols = $('[data-line-num="' + lineNumber + '"]').children(),
          selectedNums = selectedNumbersArray(lineNumber),
          countCols = $('#count_cols').val();
    for (let i=0; i < +countCols; i++) {
        let div = allCols[i],
            value = selectedNums[i];
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

function highlightNumbers(lineNumber) {
    const selectedNums = selectedNumbersArray(lineNumber);
    if (selectedNums.length !== 0) {
         for (let i = 0; i < selectedNums.length; i++) {
             $('[data-number-value="' + selectedNums[i] + '"]').addClass('js-game-ball-input-selected');
        }
    }
}

function countSelectedLinesInHiddenInputs() {
    let selected = 0;
    const lineInputs = $('.js_nums_line_hidden_input');
    lineInputs.each(function(index, item) {
        if ($(item).val() !== '') {
            selected += 1;
        }
    });
    return selected;
}

function turnFormType() {
    const gameVersion = $('#game_version').val();
    if (gameVersion === 'game777_regular') {
        const selected = countSelectedLinesInHiddenInputs(),
              form_type_hidden = $('#form_type'),
              form_type_radios = $('.ui-game-circle-input-form-type');
        if (selected === 0) {
            form_type_hidden.val(1);
        } else {
            form_type_hidden.val(selected);
        }
        form_type_radios.each(function (index, item) {
            if (+$(item).val() === selected) {
                $(item).prop('checked', true);
            }
        });
        calcTotalSum777();
    }
}

function openGameModal (modalId) {
    $('[data-modal-id="'+modalId+'"]').addClass('game-modal__open');
    $('body').addClass('modal-open');
}

function closeGameModal () {
    const modalId = $('.js-game-modal').data('modal-id')
    $('[data-modal-id="'+modalId+'"]').removeClass('game-modal__open');
    $('body').removeClass('modal-open');
}

function calcTotalSum777() {
    const totalSumBlock = $('#sum_block'),
          totalSumInput = $('#total_sum');
    $.ajax({
        type: "POST",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            ticket_type: $('#game_version').val(),
            form_type: $('#form_type').val(),
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

function selectNumsSwal() {
        Swal.fire({
            icon: 'error',
            title: gettext('ERROR'),
            background: '#cacaca',
            html: gettext("Please select the numbers"),
            confirmButtonText: gettext('Back to form'),
            confirmButtonColor: '#d33',
        });
}

function game777Save() {
    const game_version = $("#game_version").val(),
          game_type = $('#game_type').val(),
          form_type = $("#form_type").val(),
          line_1 = $("#nums_line_1").val(),
          line_2 = $("#nums_line_2").val(),
          line_3 = $("#nums_line_3").val(),
          games_count = $("#games_count").val(),
          total_sum = $('#total_sum').val(),
          pay_method = $('.payment-method').find('.single-method.active'),
          countCols = $('#count_cols').val();
    let m_pay_method = '';
    if (pay_method) {
        m_pay_method = pay_method.data('paymethod');
    }
    if (game_version === 'game777_regular') {
        const line_1_arr = selectedNumbersArray(1),
              line_2_arr = selectedNumbersArray(2);
              line_3_arr = selectedNumbersArray(3);
        if (form_type === '3') {
            if (line_1_arr.length < +countCols || line_2_arr.length < +countCols || line_3_arr.length < +countCols) {
                selectNumsSwal();
                return false;
            }
        } else if (form_type === '2') {
            if ((line_1_arr.length === 0 && (line_2_arr.length + line_3_arr.length) < (+countCols * 2)) ||
                (line_2_arr.length === 0 && (line_1_arr.length + line_3_arr.length) < (+countCols * 2)) ||
                (line_3_arr.length === 0 && (line_1_arr.length + line_2_arr.length) < (+countCols * 2))) {
                    selectNumsSwal();
                    return false;
                }
        } else if (form_type === '1') {
            if ((line_1_arr.length === 0 && line_2_arr.length === 0 && line_3_arr.length < +countCols) ||
                (line_2_arr.length === 0 && line_3_arr.length === 0 && line_1_arr.length < +countCols) ||
                (line_3_arr.length === 0 && line_1_arr.length === 0 && line_2_arr.length < +countCols)) {
                    selectNumsSwal();
                    return false;
            }
        }
    } else if (game_version === 'game777_col8' || game_version === 'game777_col9') {
        const line_1_arr = selectedNumbersArray(1);
        if (line_1_arr.length < +countCols) {
             selectNumsSwal();
             return false;
        }
    }
    $.ajax({
        type: "POST",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            f_game_version: game_version,
            f_game_type: game_type,
            f_form_type: form_type,
            f_line_1: line_1,
            f_line_2: line_2,
            f_line_3: line_3,
            f_games_count: games_count,
            f_total_sum: total_sum,
            f_pay_method: m_pay_method,
            f_is_subscription: $('#subscription').val(),
            f_subscription_days: $('#subscription_day').val(),
            f_subscription_automatic: $('#subscription_automatic').val(),
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

function initSameTicket(){
    turnNumbers(1);
    turnNumbers(2);
    turnNumbers(3);
    turnFormType();
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
            if ($('#game_version').val() === 'game777_regular') {
                numbers += `${$("#form_type").val()} `
                numbers += gettext('lines of numbers will be inserted automatically');
            } else {
                numbers += gettext('Numbers will be inserted automatically');
            }
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
                game777Save();
            }
         });
    }
    else {
       game777Save();
   }
}