$(function ($) {
    initSameTicket();
    calcTotalSumChance();
    // chance modal
    $('.js-ui-game-single-card').on('click', function () {
        if ($(this).hasClass('ui-game-single-card_not-active')) {
            return;
        }
        const suit = $(this).data('card-suit');
        $('.js-selected-suit').attr("data-selected-suit", suit)


        $('.game-modal__body').find('.ui-game-single-card').removeClass('js-single-card-selected');
        let card_input = $('#card_' + suit).val();
        if (card_input !== "") {
            $('[data-card-value="' + card_input + '"]').addClass('js-single-card-selected');
        }

        const game_type = $('#game_version').val();
        if (game_type === 'chance_systematic') {
            const all_4_cards = $('[data-card-suit="' + suit + '"]');
            all_4_cards.addClass('js-single-card-selected');
            highlightCards(suit);
        } else {
            $('.js-ui-game-single-card').removeClass('js-single-card-selected');
            $(this).addClass('js-single-card-selected');
        }
        openGameModal('js-game-modal-single', $(this));
    });

    $('.js-game-modal-save').on('click', function () {
        closeGameModalChance()
    })

    $('.js-game-modal-close').on('click', function () {
        const game_type = $('#game_type').val();
        if (game_type === "chance") {
            const current_suit = $('.js-selected-suit').attr('data-selected-suit'),
                card_input = `#card_${current_suit}`,
                choosescard = $('[data-card-suit="' + current_suit + '"]');
            $(card_input).val("");
            $('.game-modal__body').find('.ui-game-single-card').removeClass('js-single-card-selected');

            choosescard.removeClass('ui-game-card-suit');
            choosescard.removeClass(`ui-game-card-suit__${current_suit}`);
            choosescard.find('.js-game-single-card_img').attr("hidden", false);
            choosescard.find('.js-game-single-card_text').attr("hidden", true);
            choosescard.find('.js-game-single-card_text').html("");
            closeGameModalChance();
        }
        closeGameModal();
    });

    $('.ui-game-circle-input-form-type').on('click', function () {
        closeGameModalChance();
        const game_version = $('#game_version').val(),
              mtotalcard = $(this).val(),
              cards_hidden_inputs = $('.js_card_hidden_input'),
              selected = countSelectedCardInHiddenInputs();
        if (selected > +mtotalcard) {
            let counter = selected - +mtotalcard;
            if (game_version === "chance_regular" || game_version === 'chance_multi') {
            const mkards = $('.ui-game-single-cards').find('.ui-game-single-card');
            $(mkards).get().reverse().forEach(function (elem) {
                if (counter > 0) {
                   if ($(elem).find('.js-game-single-card_img').is(":hidden")) {
                        $(elem).find('.js-game-single-card_text').attr("hidden", true);
                        $(elem).find('.js-game-single-card_img').attr("hidden", false);
                        counter -= 1;
                   }
                }
                // }
            });
            } else if (game_version === "chance_systematic") {
                const mkards = $('.ui-game-single-cards-multi');
                mkards.each(function () {
                if ($(this).data('card-num') > +mtotalcard) {
                    let all_cards = $(this).find('.ui-game-single-card');
                    all_cards.find('.js-game-single-card_img').attr("hidden", false);
                    all_cards.find('.js-game-single-card_text').attr("hidden", true);
                    all_cards.find('.js-game-single-card_text').html("");
                    }
                });
            }
            cards_hidden_inputs.each(function(idx, elem) {
            if ($(elem).data('card-num') > +mtotalcard) {
                $(elem).val('');
            }
        });
        }
        $('#form_type').val(mtotalcard);
        calcTotalSumChance();
    })
    $('.js-card-for-select').on('click', function () {
        const thiscard = $(this),
              cardvalue = thiscard.attr('data-card-value'),
              current_suit = $('.js-selected-suit').attr('data-selected-suit'),
              card_input = `#card_${current_suit}`;
        const game_type = $('#game_version').val();
        if (game_type === 'chance_systematic') {
            if ($(card_input).val().includes(cardvalue)) {
                thiscard.removeClass('js-single-card-selected');
                let old_val = $(card_input).val()
                let new_val = old_val.replace(cardvalue, '');
                $(card_input).val(new_val);
            } else {
                if ($(card_input).val().length < 4){
                thiscard.addClass('js-single-card-selected');
                let old_val = $(card_input).val();
                let new_val = sortedCards(old_val + cardvalue);
                $(card_input).val(new_val);
                }
            }
            turnCards(current_suit);
        } else {
            $('.game-modal__body').find('.ui-game-single-card').removeClass('js-single-card-selected');
            thiscard.addClass('js-single-card-selected');
            $(card_input).val(cardvalue);
            const choosescard = $('[data-card-suit="' + current_suit + '"]');
            choosescard.addClass('ui-game-card-suit');
            choosescard.addClass(`ui-game-card-suit__${current_suit}`);
            choosescard.find('.js-game-single-card_img').attr("hidden", true);
            choosescard.find('.js-game-single-card_text').attr("hidden", false);
            choosescard.find('.js-game-single-card_text').html(cardvalue);
        }
        const selected = countSelectedCardInHiddenInputs(),
              form_type_hidden = $('#form_type'),
              form_type_radios = $('.ui-game-circle-input-form-type');
        if (selected > +form_type_hidden.val()) {
                form_type_hidden.val(selected);
                form_type_radios.each(function (index, item) {
                    if (+$(item).val() === selected) {
                        $(item).prop('checked', true);
                    }
                });
            }
        calcTotalSumChance();
    })
    $('.ui-game-circle-input-games-count').on('click', function () {
        const games_count = $(this).val();
        $('#games_count').val(games_count);
        calcTotalSumChance();
    })

    $('.js-game-reset').on('click', function () {
        const game_type = $('#game_type').val(),
              game_version = $('#game_version').val();
        if (game_type === "chance") {
            $('#card_hearts').val("");
            $('#card_spades').val("");
            $('#card_diamonds').val("");
            $('#card_clubs').val("");
            let all_cards;
            if (game_version === "chance_regular" || game_version === 'chance_multi') {
                all_cards = $('.ui-game-single .ui-game-single-cards');
            } else if (game_version === "chance_systematic") {
                all_cards = $('.ui-game-single-card');
            }
            if (all_cards) {
                all_cards.find('.js-game-single-card_img').attr("hidden", false);
                all_cards.find('.js-game-single-card_text').attr("hidden", true);
                all_cards.find('.js-game-single-card_text').html("");
            }
        }
        closeGameModalChance();
    })

    $('.js-game-auto').on('click', function () {
         closeGameModalChance();
         const game_type = $('#game_version').val();
         if (game_type === "chance_regular" || game_type === 'chance_multi') {
             const cardArray = ['7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
                   formType = $('#form_type').val(),
                   cards_hidden_inputs = $('.js_card_hidden_input');
             let toTurn = +formType;
             cards_hidden_inputs.each(function(index, item) {
                 $(item).val('');
                 if (toTurn !== 0) {
                     toTurn -= 1;
                     const card_id = $(item).attr('id'),
                           current_suit = card_id.split('_')[1],
                           cardvalue = cardArray[Math.floor(Math.random() * 8)],
                           choosescard = $('[data-card-suit="' + current_suit + '"]');
                     $(item).val(cardvalue);
                     choosescard.addClass('ui-game-card-suit');
                     choosescard.addClass(`ui-game-card-suit__${current_suit}`);
                     choosescard.find('.js-game-single-card_img').attr("hidden", true);
                     choosescard.find('.js-game-single-card_text').attr("hidden", false);
                     choosescard.find('.js-game-single-card_text').html(cardvalue);
                 }
             });
         } else if (game_type === 'chance_systematic') {
             const formType = $('#form_type').val(),
                   cards_hidden_inputs = $('.js_card_hidden_input');
             let selected_suits = 0,
                 inputsToTurn = [];
             cards_hidden_inputs.each(function(index, item) {
                 $(item).val('');
                 if (selected_suits < +formType) {
                     inputsToTurn.push($(item));
                     selected_suits++;
                    }
             });
             inputsToTurn.forEach(function(item) {
                 const current_suit =$(item).attr('id').split('_')[1];
                 let cards4 = addCardsToBe4($(item).val());
                 let cards4Sorted = sortedCards(cards4);
                 $(item).val(cards4Sorted);
                 turnCards(current_suit);
             });
         }
         calcTotalSumChance();
    });

     $('.js-not-carousel-games-count').on('click', function () {
         const price = $(this).val();
         $('#price').val(price);
         calcTotalSumChance();
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
        calcTotalSumChance();
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
        calcTotalSumChance();
    });
    $('input[name=automatic-same]').on('click', function () {
        if ($(this).val() === '1') {
            $('#subscription_automatic').val(1);
        } else {
            $('#subscription_automatic').val(0);
        }
    });
});

function openGameModal (modalId) {
    $('[data-modal-id="'+modalId+'"]').addClass('game-modal__open');
    $('body').addClass('modal-open');
}

function closeGameModal () {
    const modalId = $('.js-game-modal').data('modal-id')
    $('[data-modal-id="'+modalId+'"]').removeClass('game-modal__open');
    $('body').removeClass('modal-open');
}

function closeGameModalChance() {
        $('.js-ui-game-single-card').removeClass('js-single-card-selected');
        closeGameModal();
}

function selectCardsSwal() {
        Swal.fire({
            icon: 'error',
            title: gettext('ERROR'),
            background: '#cacaca',
            html: gettext("Please select a cards"),
            confirmButtonText: gettext('Back to form'),
            confirmButtonColor: '#d33',
        });
}

function gameChanceSave() {
    const game_version = $("#game_version").val(),
          game_type = $('#game_type').val(),
          form_type = $("#form_type").val(),
          card_hearts = $("#card_hearts").val(),
          card_spades = $("#card_spades").val(),
          card_diamonds = $("#card_diamonds").val(),
          card_clubs = $("#card_clubs").val(),
          price = $("#price").val(),
          games_count = $("#games_count").val(),
          total_sum = $('#total_sum').val(),
          pay_method = $('.payment-method').find('.single-method.active'),
          selected = countSelectedCardInHiddenInputs();
    let m_pay_method = '';
    if (pay_method) {
        m_pay_method = pay_method.data('paymethod');
    }
    if (selected < +form_type) {
        selectCardsSwal();
        return false;
    }
    $.ajax({
        type: "POST",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            f_game_version: game_version,
            f_game_type: game_type,
            f_form_type: form_type,
            f_card_hearts: card_hearts,
            f_card_spades: card_spades,
            f_card_diamonds: card_diamonds,
            f_card_clubs: card_clubs,
            f_price: price,
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

function gameSave() {
    if ($('#subscription').val() === '1') {
        let games,
            cards = '';
        if ($('#subscription_day').val() === 'infinity') {
            games = gettext('Infinity');
        } else {
            games = $('#subscription_day').val();
        }
        if ($('#subscription_automatic').val() === '1') {
            if ($('#game_version').val() == 'chance_systematic') {
                if ($("#card_hearts").val() !== '') {
                    cards += `${$("#card_hearts").val().length} `
                    cards += gettext('heart cards will be inserted automatically');
                    cards += '<br>';
                }
                if ($("#card_spades").val() !== '') {
                    cards += `${$("#card_spades").val().length} `
                    cards += gettext('spade cards will be inserted automatically');
                    cards += '<br>';
                }
                if ($("#card_diamonds").val() !== '') {
                    cards += `${$("#card_diamonds").val().length} `
                    cards += gettext('diamond cards will be inserted automatically');
                    cards += '<br>';
                }
                 if ($("#card_clubs").val() !== '') {
                     cards += `${$("#card_clubs").val().length} `
                     cards += gettext('club cards will be inserted automatically');
                     cards += '<br>';
             }

            } else {
                if ($("#card_hearts").val() !== '') {
                 cards += gettext('The heart card will be inserted automatically');
                 cards += '<br>';
                }
                if ($("#card_spades").val() !== '') {
                 cards += gettext('The spade card will be inserted automatically');
                 cards += '<br>';
                }
                if ($("#card_diamonds").val() !== '') {
                 cards += gettext('The diamond card will be inserted automatically');
                 cards += '<br>';
                }
                 if ($("#card_clubs").val() !== '') {
                 cards += gettext('The club card will be inserted automatically');
                 cards += '<br>';
                }
            }
        } else {
           cards = gettext('Same cards');
        }
        const text = `${gettext('Games count')}: ${games} <br>
                      ${gettext('Cards')}: ${cards}`;
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
                gameChanceSave();
            }
         });
    } else {
       gameChanceSave();
   }
}

function countSelectedCardInHiddenInputs() {
    let selected = 0;
    const cards_hidden_inputs = $('.js_card_hidden_input');
    cards_hidden_inputs.each(function(index, item) {
        if ($(item).val() !== '') {
            selected += 1;
        }
    });
    return selected;
}


function calcTotalSumChance() {
    const game_type = $('#game_version').val(),
          price = $("#price").val(),
          totalSumBlock = $('#sum_block'),
          total_sum_input = $('#total_sum');
    $.ajax({
        type: "POST",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            ticket_type: game_type,
            price: price,
            card_hearts: $("#card_hearts").val(),
            card_spades: $("#card_spades").val(),
            card_diamonds: $("#card_diamonds").val(),
            card_clubs: $("#card_clubs").val(),
            is_subscription: $('#subscription').val(),
            subscription_days: $('#subscription_day').val()
        },
        url: "/calc_game_lotto_sum/",
        success: function (res) {
            if (res.AnswerCod === '01') {
                totalSumBlock.html(res.AnswerText);
                total_sum_input.val(res.AnswerText);
            }
        },
    });
}

function sortedCards(str) {
    const cardArray = ['7', '8', '9', 'T', 'J', 'Q', 'K', 'A'];
    let result = '';
    cardArray.forEach(elem => {
        if (str.includes(elem)) {
            result += elem;
        }
    });
    return result;
}

function addCardsToBe4(str) {
    let cardArray = ['7', '8', '9', 'T', 'J', 'Q', 'K', 'A'];
    let result = str;
    for (let i=0; i< 4; i++) {
        let random = cardArray[Math.floor(Math.random() * 8)]
        while (result.includes(random)) {
            random = cardArray[Math.floor(Math.random() * 8)]
        }
        result += random;
        if (result.length === 4) {
            break;
        }
    }
    return result;
}

function turnCards(current_suit) {
    const all_4_cards = $('[data-card-suit="' + current_suit + '"]'),
          card_input = `#card_${current_suit}`;
    for (let i=0; i<4; i++) {
        let div = all_4_cards[i],
            text_val = $(card_input).val()[i];
        if (text_val === 'T') {
            text_val = '10';
        }
        if (text_val) {
            $(div).addClass('ui-game-card-suit');
            $(div).addClass(`ui-game-card-suit__${current_suit}`);
            $(div).find('.js-game-single-card_img').attr("hidden", true);
            $(div).find('.js-game-single-card_text').attr("hidden", false);
            $(div).find('.js-game-single-card_text').html(text_val);
        } else {
            $(div).removeClass('ui-game-card-suit');
            $(div).removeClass(`ui-game-card-suit__${current_suit}`);
            $(div).find('.js-game-single-card_img').attr("hidden", false);
            $(div).find('.js-game-single-card_text').attr("hidden", true);
        }
    }
}

function highlightCards(current_suit) {
    const card_input = $('#card_' + current_suit).val();
    if (card_input !== '') {
         for (let i = 0; i < card_input.length; i++) {
             $('[data-card-value="' + card_input[i] + '"]').addClass('js-single-card-selected');
        }
    }
}

function initSameTicket() {
    const game_type = $('#game_version').val(),
          cards_hidden_inputs = $('.js_card_hidden_input'),
          form_type_hidden = $('#form_type').val(),
          form_type_radios = $('.ui-game-circle-input-form-type');
    form_type_radios.each(function (index, item) {
        if ($(item).val() === form_type_hidden) {
            $(item).prop('checked', true);
        }
    });
    if (game_type === "chance_regular" || game_type === 'chance_multi') {
         cards_hidden_inputs.each(function(index, item) {
             if ($(item).val() !== '') {
                 const card_id = $(item).attr('id'),
                       current_suit = card_id.split('_')[1],
                       cardvalue = $(item).val(),
                       choosescard = $('[data-card-suit="' + current_suit + '"]');
                 choosescard.addClass('ui-game-card-suit');
                 choosescard.addClass(`ui-game-card-suit__${current_suit}`);
                 choosescard.find('.js-game-single-card_img').attr("hidden", true);
                 choosescard.find('.js-game-single-card_text').attr("hidden", false);
                 choosescard.find('.js-game-single-card_text').html(cardvalue);
             }

         });
    } else if (game_type === 'chance_systematic') {
        cards_hidden_inputs.each(function(index, item) {
            if ($(item).val() !== '') {
                if ($(item).val().includes('10')) {
                    const new_val = $(item).val().replace('10', 'T');
                    $(item).val(new_val);
                }
                const card_id = $(item).attr('id'),
                      current_suit = card_id.split('_')[1];
                turnCards(current_suit);
            }
        });
        const price_hidden = $('#price').val(),
              price_radios = $('.js-not-carousel-games-count');
        price_radios.each(function (index, item) {
            if ($(item).val() === price_hidden) {
                $(item).prop('checked', true);
            }
        });
    }
}