$(function ($) {
    // lotto modal
    initSameTicket();
    calcTotalSumLotto();
    $('.js-ui-game-lotto-modal-open').on('click', function () {
        const line = $(this).attr('data-line');
        const isDouble = $('#is_double').val();
        let tab;
        if (isDouble === '0') {
            tab = 'regular';
        } else {
            tab = 'double';
        }
        closeGameModal('js-ui-game-lotto-modal-2');
        $('.js-selected-line').attr("data-selected-line", line);
        $('.js-modal-reset-button-line').attr("data-line", line);
        $('.game-modal__body').find('.ui-game-ball-input').removeClass('js-game-ball-input-selected');
        highlightNumbers(line, tab);
        openGameModal('js-ui-game-lotto-modal');
    });

    $('.js-ui-game-lotto-modal-2-open').on('click', function () {
        const isDouble = $('#is_double').val();
        let tab;
        if (isDouble === '0') {
            tab = 'regular';
        } else {
            tab = 'double';
        }
        closeGameModal('js-ui-game-lotto-modal');
        const line = $(this).attr(`data-strong-num-${tab}`);
        $('.js-selected-line').attr("data-selected-line", line);
        $('.js-modal-reset-button-line').attr("data-line", line);
        $('.game-modal__body').find('.ui-game-ball-input').removeClass('js-game-ball-input-selected');
        highlightNumbers(line, tab, true);
        openGameModal('js-ui-game-lotto-modal-2');
    });
    $('.js-game-modal-save').on('click', function () {
        closeAllModals();
    });
    $('input[name=regular-double]').on('click', function () {
        closeAllModals();
        if ($(this).val() === 'regular') {
            $('#is_double').val(0);
            $('#double_block').attr("hidden", true);
            $('#regular_block').attr("hidden", false);
        } else {
            $('#is_double').val(1);
            $('#regular_block').attr("hidden", true);
            $('#double_block').attr("hidden", false);
        }
        calcTotalSumLotto();
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
    $( "#is_extra_btn" ).click(function( event ) {
        event.stopPropagation();
        const extraHiddenInput = $('#is_extra');
        if (this.checked) {
            extraHiddenInput.val(1);
        } else {
            extraHiddenInput.val(0);
        }
        calcTotalSumLotto();
    });


    $('.ui-game-ball-input-line').on('click', function () {
        const tab = getCurrentTab();
        const thisLine = $(this),
              lineValue = thisLine.val(),
              currentLine = $('.js-selected-line').attr('data-selected-line'),
              lineInput = `#nums_${tab}_line_${currentLine}`,
              countNumbers = selectedNumbersArray(currentLine, tab).length;
        if ($(lineInput).val().includes(`${lineValue};`)) {
            thisLine.removeClass('js-game-ball-input-selected');
            let old_val = $(lineInput).val();
            let new_val = old_val.replace(`${lineValue};`, '');
            $(lineInput).val(new_val);
        } else {
            if (countNumbers < 6){
            thisLine.addClass('js-game-ball-input-selected');
            let old_val = $(lineInput).val();
            let new_val = sortedNumbers(old_val + `${lineValue};`);
            $(lineInput).val(new_val);
            }
        }
        turnNumbers(currentLine, tab);
        if (tab === 'double') {
            turnCountDouble();
        }
    });

    $('.ui-game-ball-input-strong').on('click', function () {
        const tab = getCurrentTab();
        const thisStrong = $(this),
              thisStrongVal = $(thisStrong).val(),
              currentLine = $('.js-selected-line').attr('data-selected-line'),
              strongInput = `#nums_${tab}_strong_${currentLine}`;
        if ($(strongInput).val() === thisStrongVal) {
                thisStrong.removeClass('js-game-ball-input-selected');
                $(strongInput).val('');
            } else {
                $('.game-modal__body').find('.ui-game-ball-input').removeClass('js-game-ball-input-selected');
                thisStrong.addClass('js-game-ball-input-selected');
                $(strongInput).val(thisStrongVal);
            }
        turnNumbers(currentLine, tab);
        if (tab === 'double') {
            turnCountDouble();
        }
    });

    $('.js-game-reset').on('click', function () {
        const currentLine = $(this).attr('data-line'),
              whatDelete = $(this).attr('data-reset'),
              tab = getCurrentTab();
        reset(currentLine, whatDelete);
        if (tab === 'double') {
            turnCountDouble();
        }
        closeAllModals();
    });

    $('.js-game-reset-block').on('click', function () {
        const blocksLines = {1: [1, 2], 2: [3, 4], 3: [5, 6], 4: [7, 8], 5: [9, 10]}
        const currentBlock = $(this).attr('data-block');
        blocksLines[currentBlock].forEach(element => reset(element, 'all'));
        turnCountDouble();
    });

    $('.js-game-auto').on('click', function () {
        const isDouble = $('#is_double').val();
        if (isDouble === '0') {
            const currentLine = $(this).attr('data-line');
            autoGame(currentLine);
        } else {
            const blocksLines = {1: [1, 2], 2: [3, 4], 3: [5, 6], 4: [7, 8], 5: [9, 10]}
            const currentBlock = $(this).attr('data-block');
            blocksLines[currentBlock].forEach(element => autoGame(element));
            turnCountDouble();
        }
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

function reset(currentLine, whatDelete) {
    closeAllModals();
    const tab = getCurrentTab(),
          allCols = $(`[data-line-num-${tab}="${currentLine}"]`).children().not(".ui-game-ball_empty, .strong-number-ball"),
          lineInput = `#nums_${tab}_line_${currentLine}`,
          strongInput = `#nums_${tab}_strong_${currentLine}`,
          strongNumCol = $(`[data-strong-num-${tab}="${currentLine}"]`);

    if (whatDelete === 'line') {
        $(lineInput).val('');
        for (let i=0; i<allCols.length; i++) {
            let div = allCols[i];
            $(div).html('');
        }
    } else if (whatDelete === 'strong') {
        $(strongInput).val('');
        $(strongNumCol).html('');
    } else {
        $(strongInput).val('');
        $(strongNumCol).html('');
        $(lineInput).val('');
        for (let i=0; i<allCols.length; i++) {
            let div = allCols[i];
            $(div).html('');
        }
    }
    calcTotalSumLotto();
}

function autoGame(currentLine) {
    closeAllModals();
    const tab = getCurrentTab(),
          numbersArray = ['01;', '02;', '03;', '04;', '05;', '06;', '07;', '08;', '09;', '10;', '11;', '12;', '13;',
              '14;', '15;', '16;', '17;', '18;', '19;', '20;', '21;', '22;', '23;', '24;', '25;', '26;', '27;',
              '28;', '29;', '30;', '31;', '32;', '33;', '34;', '35;', '36;', '37;'],
          strongArray = ['1', '2', '3', '4', '5', '6', '7'],
          lineInput = `#nums_${tab}_line_${currentLine}`,
          strongInput = `#nums_${tab}_strong_${currentLine}`,
          randomStrong = strongArray[Math.floor(Math.random() * 7)];
    let resultLine = '';
    for (let i=0; i< 6; i++) {
        let random = numbersArray[Math.floor(Math.random() * 37)]
        while (resultLine.includes(random)) {
            random = numbersArray[Math.floor(Math.random() * 37)]
        }
        resultLine += random;
    }
    $(strongInput).val(randomStrong);
    const newValLine = sortedNumbers(resultLine);
    $(lineInput).val(newValLine);
    turnNumbers(currentLine, tab);
}

function getCurrentTab() {
    const isDouble = $('#is_double').val();
    let tab;
    if (isDouble === '0') {
        tab = 'regular';
    } else {
        tab = 'double';
    }
    return tab;
}

function selectedNumbersArray(lineNumber, tab) {
    let cleanedLineInputArray = [];
    const lineInput = $(`#nums_${tab}_line_${lineNumber}`).val();
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
        '31;', '32;', '33;', '34;', '35;', '36;', '37;'];
    let result = '';
    numbersArray.forEach(elem => {
        if (str.includes(elem)) {
            result += elem;
        }
    });
    return result;
}

function turnNumbers(lineNumber, tab) {
    const allCols = $(`[data-line-num-${tab}="${lineNumber}"]`).children().not(".ui-game-ball_empty"),
          selectedNums = selectedNumbersArray(lineNumber, tab),
          selectedStrong = $(`#nums_${tab}_strong_${lineNumber}`).val(),
          strongNumCol = $(`[data-strong-num-${tab}="${lineNumber}"]`);
    for (let i=0; i < 6; i++) {
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
    $(strongNumCol).html(selectedStrong);
    calcTotalSumLotto();
}


function highlightNumbers(lineNumber, tab, strong=false) {
    if (strong) {
        const selectedStrong = $(`#nums_${tab}_strong_${lineNumber}`).val();
        if (selectedStrong !== '') {
            $('[data-number-value="' + selectedStrong + '"]').addClass('js-game-ball-input-selected');
        }
    } else {
         const selectedNums = selectedNumbersArray(lineNumber, tab);
         if (selectedNums.length !== 0) {
            for (let i = 0; i < selectedNums.length; i++) {
                $('[data-number-value="' + selectedNums[i] + '"]').addClass('js-game-ball-input-selected');
            }
        }
    }
}

function countSelectedLinesRegular(saveCheck=false) {
    const nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14];
    let selected = 0;
    let saveCheckRes = true;
     nums.forEach(elem => {
         const clearLineArray = selectedNumbersArray(elem, 'regular'),
               strongVal = $(`#nums_regular_strong_${elem}`).val();
            if (clearLineArray.length === 6 && strongVal !== '') {
                selected++;
           } else if ((clearLineArray.length === 6 && strongVal === '') && saveCheck){
                saveCheckRes = false;
            } else if ((clearLineArray.length === 0 && strongVal !== '') && saveCheck) {
                saveCheckRes = false;
            } else if (clearLineArray.length > 0 && clearLineArray.length < 6 && saveCheck) {
                saveCheckRes = false;
            }
     });
     if (saveCheck) {
         return [saveCheckRes, selected];
     }
     return selected;
}

function countSelectedLinesDouble(saveCheck=false) {
    const nums = [1, 2, 3, 4, 5],
          blocks = {1: [1, 2], 2: [3, 4], 3: [5, 6], 4: [7, 8], 5: [9, 10]};
    let selected = 0;
    let saveCheckRes = true;
    nums.forEach(num => {
        const lines = blocks[num];
        let selectedInBlock = 0;
        lines.forEach(elem => {
            const clearLineArray = selectedNumbersArray(elem, 'double'),
                  strongVal = $(`#nums_double_strong_${elem}`).val();
            if (clearLineArray.length === 6 && strongVal !== '') {
                selectedInBlock++;
            }else if ((clearLineArray.length === 6 && strongVal === '') && saveCheck){
                saveCheckRes = false;
            } else if ((clearLineArray.length === 0 && strongVal !== '') && saveCheck) {
                saveCheckRes = false;
            } else if (clearLineArray.length > 0 && clearLineArray.length < 6 && saveCheck) {
                saveCheckRes = false;
            }
        });
        if (selectedInBlock === 2) {
            selected += 2;
        }
        if (selectedInBlock === 1 && saveCheck) {
            saveCheckRes = false;
        }
    });
    if (saveCheck) {
        return [saveCheckRes, selected];
     }
    const division2 = selected % 2;
    if (selected === 0) {
        selected = 2;
    } else if (division2 === 1) {
        selected--;
    }
    return selected;
}


function turnCountDouble() {
    const allCountBlocks = $('.js-count-blocks').children();
    let selected = countSelectedLinesDouble();
    allCountBlocks.removeClass('ui-game-lotto-row-line-number_selected');
    allCountBlocks.each(function (index, item) {
        if (+$(item).attr('data-count') === selected) {
            $(item).addClass('ui-game-lotto-row-line-number_selected');
        }
    });
}

function calcTotalSumLotto() {
    const totalSumBlock = $('#sum_block'),
          totalSumInput = $('#total_sum'),
          isDouble = $('#is_double').val(),
          isExtra = $('#is_extra').val();
    let countLines;
    if (isDouble === '1') {
        countLines = countSelectedLinesDouble();
    } else {
        countLines = countSelectedLinesRegular();
    }
    $.ajax({
        type: "POST",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            ticket_type: $('#game_version').val(),
            count_lines: countLines,
            is_double: isDouble,
            is_extra: isExtra,
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


function selectNumsSwal() {
        Swal.fire({
            icon: 'error',
            title: gettext('ERROR'),
            background: '#cacaca',
            html: gettext("Please fill to the end or clear selected blocks"),
            confirmButtonText: gettext('Back to form'),
            confirmButtonColor: '#d33',
        });
}

function notDiv2Swal() {
     Swal.fire({
            icon: 'error',
            title: gettext('ERROR'),
            background: '#cacaca',
            html: gettext("The number of completed lines must be 2, 4, 6, 8, 10, 12 or 14"),
            confirmButtonText: gettext('Back to form'),
            confirmButtonColor: '#d33',
        });
}

function atLeast1BlockSwal() {
     Swal.fire({
            icon: 'error',
            title: gettext('ERROR'),
            background: '#cacaca',
            html: gettext("Complete at least 1 block"),
            confirmButtonText: gettext('Back to form'),
            confirmButtonColor: '#d33',
        });
}

function gameLottoSave() {
    const gameVersion = $('#game_version').val(),
          gameType = $('#game_type').val(),
          gamesCount = $('#games_count').val(),
          totalSum = $('#total_sum').val(),
          isExtra = $('#is_extra').val(),
          isDouble = $('#is_double').val(),
          payMethod = $('.payment-method').find('.single-method.active');
    let m_pay_method = '';
    if (payMethod) {
        m_pay_method = payMethod.data('paymethod');
    }
    let data = {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        f_game_version: gameVersion,
        f_game_type: gameType,
        f_is_extra: isExtra,
        f_is_double: isDouble,
        f_games_count: gamesCount,
        f_total_sum: totalSum,
        f_pay_method: m_pay_method,
        f_is_subscription: $('#subscription').val(),
        f_subscription_days: $('#subscription_day').val(),
        f_subscription_automatic: $('#subscription_automatic').val()
    }
    if (isDouble === '0') {
        const selectedCheck = countSelectedLinesRegular(true),
              division2 = selectedCheck[1] % 2;
        if (!selectedCheck[0]) {
            selectNumsSwal();
            return false;
        }
        if (division2 === 1 || selectedCheck[1] === 0) {
            notDiv2Swal();
            return false;
        }
        $('.js_regular_line_hidden_input').each(function(index, currentElement) {
            data[currentElement.id] = currentElement.value;
        });
        $('.js_regular_strong_hidden_input').each(function(index, currentElement) {
            data[currentElement.id] = currentElement.value;
        });
    } else if (isDouble === '1') {
        const selectedCheck = countSelectedLinesDouble(true);
        if (!selectedCheck[0]) {
            selectNumsSwal();
            return false;
        }
        if (selectedCheck[1] === 0) {
            atLeast1BlockSwal();
            return false;
        }
        $('.js_double_line_hidden_input').each(function(index, currentElement) {
            data[currentElement.id] = currentElement.value;
        });
        $('.js_double_strong_hidden_input').each(function(index, currentElement) {
            data[currentElement.id] = currentElement.value;
        });
    }
$.ajax({
        type: "POST",
        async: false,
        data: data,
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
    const tab = getCurrentTab();
    let arr;
    if (tab === 'double') {
         arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
         $('#double_btn').prop('checked', true);
         $('#regular_block').attr("hidden", true);
         $('#double_block').attr("hidden", false);
    } else {
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14];
    }
    arr.forEach(elem => {
        turnNumbers(elem, tab)
    });
    const extraHiddenInput = $('#is_extra').val(),
          extraCheckbox = $('#is_extra_btn');

    if (extraHiddenInput === '1') {
        extraCheckbox.prop('checked', true);
    }
    if (tab === 'double') {
        turnCountDouble();
    }
}

function gameSave() {
    if ($('#subscription').val() === '1') {
        let games,
            numbers = '',
            extra,
            double;
        if ($('#is_extra').val() === '1') {
            extra = gettext('Yes');
        } else {
            extra = gettext('No');
        }
        if ($('#is_double').val() === '1') {
            double = gettext('Yes');
            if ($('#subscription_automatic').val() === '1') {
                let countLines = countSelectedLinesDouble();
                numbers += `${countLines} `;
                numbers += gettext('lines of numbers will be inserted automatically');
            } else {
                numbers = gettext('Same numbers');
            }
        } else {
            double = gettext('No');
            if ($('#subscription_automatic').val() === '1') {
                let countLines = countSelectedLinesRegular();
                numbers += `${countLines} `;
                numbers += gettext('lines of numbers will be inserted automatically');
            } else {
                numbers = gettext('Same numbers');
            }
        }
        if ($('#subscription_day').val() === 'infinity') {
            games = gettext('Infinity');
        } else {
            games = $('#subscription_day').val();
        }
        const text = `${gettext('Games count')}: ${games} <br>
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