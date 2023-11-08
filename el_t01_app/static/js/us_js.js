var header_init, preloader;

header_init = function () {
    $('.js-header-middle__login').click(function (e) {
        console.log('js-header-middle__login');
        var t;
        e.preventDefault();
        t = $(this);
        return $('.js-modal__login').modal('show');
    });
    $('.js-header-middle__register').click(function (e) {
        console.log('js-header-middle__register');
        var t;
        e.preventDefault();
        t = $(this);
        return $('.js-modal__register').modal('show');
    });
    $('.js-stat_modal__inhour').click(function (e) {
        console.log('js-stat_modal__inhour');
        var t;
        e.preventDefault();
        t = $(this);
        var field_station;
        field_station = t.closest('.js-stat_station');

        $('#id_modal_inhour_station').html(field_station.data("station"));
        return $('.js-modal__inhour').modal('show');
    });

    // Убавляем кол-во по клику
    $('.quantity_inner .bt_minus').click(function () {
        let $input = $(this).parent().find('.quantity');
        let count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
    });
    // Прибавляем кол-во по клику
    $('.quantity_inner .bt_plus').click(function () {
        console.log("bt_plus");
        let $input = $(this).parent().find('.quantity');
        let count = parseInt($input.val()) + 1;
        count = count > parseInt($input.data('max-count')) ? parseInt($input.data('max-count')) : count;
        $input.val(parseInt(count));
    });
    // Убираем все лишнее и невозможное при изменении поля
    $('.quantity_inner .quantity').bind("change keyup input click", function () {
        if (this.value.match(/[^0-9]/g)) {
            this.value = this.value.replace(/[^0-9]/g, '');
        }
        if (this.value == "") {
            this.value = 1;
        }
        if (this.value > parseInt($(this).data('max-count'))) {
            this.value = parseInt($(this).data('max-count'));
        }
    });
};

preloader = function () {
    return $(window).load(function () {
        return $('#loading').fadeOut('slow');
    });
};

function validateEmail(email) {
    var re;
    re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return re.test(email);
}

function validatePhone(phone) {
    var re;
    re = /^[0-9\+\-]{6,18}$/;
    return re.test(phone);
}

function validatePassword(m_p1, m_p2) {
    var msg;
    console.log("m_p1, m_p2 = ", m_p1, m_p2);
    if (m_p1.length < 6) {
        msg = gettext('Password cannot be less than 6 characters.');
        return msg;
    }
    if (!(m_p1 === m_p2)) {
        msg = gettext('Password mismatch.');
        return msg;
    }
    msg = 'ok';
    return msg;
}

function input_field_not_exist(name) {
    return ($('input[name=' + name + ']')).length === 0;
}

function input_field_value(name) {
    return ($('input[name=' + name + ']')).val();
}

function input_field_value_is_empty(name) {
    return ($('input[name=' + name + ']')).val() === '';
}

function input_field_exist(name) {
    return !(($('input[name=' + name + ']')).length === 0);
}

function textarea_field_exist(name) {
    return !(($('textarea[name=' + name + ']')).length === 0);
}

function modal_get_forgot_pass() {
    $('.js-modal__login').modal('hide');
    return $('.js-modal__forgot-pass').modal('show');
}

function modal_reg_new_user() {
    $('.js-modal__login').modal('hide');
    return $('.js-modal__register').modal('show');
}
function modal_already_have_login() {
    $('.js-modal__register').modal('hide');
    return $('.js-modal__login').modal('show');
}


function btn_modal_register() {
    console.log("btn_modal_register");
    var m_url_path = input_field_value('url_path');
    var m_get_param = input_field_value('get_param');
    var m_game_gift_id = input_field_value('game_gift_id');
    var m_name = input_field_value('f_name');
    var m_email = input_field_value('f_email');
    var m_password = input_field_value('f_password');
    var m_re_password = input_field_value('f_re_password');
    var m_phone = input_field_value('f_phone');
    // var m_re_day = input_field_value('f_re_day');
    var m_re_day = $('#input-day option').filter(':selected').val();
    // var m_re_month = input_field_value('f_re_month');
    var m_re_month = $('#input-month option').filter(':selected').val();
    // var m_re_year = input_field_value('f_re_year');
    var m_re_year = $('#input-year option').filter(':selected').val();
    var m_id = input_field_value('f_id');
    var m_txt_error;
    var isValid;
    if (input_field_exist('f_name')) {
        if (input_field_value_is_empty('f_name')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter your Name"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#id_f_name');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    if (input_field_exist('f_email')) {
        if (input_field_value_is_empty('f_email')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter your Email/Login"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#id_f_email');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
        isValid = validateEmail(input_field_value('f_email'));
        if (!isValid) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Invalid email format"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#id_f_email');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    if (input_field_exist('f_password')) {
        m_txt_error = validatePassword(m_password, m_re_password);
        if (!(m_txt_error === "ok")) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: m_txt_error,
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#id_f_password');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    if (input_field_exist('f_phone')) {
        if (input_field_value_is_empty('f_phone')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter your phone number"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#input-phone');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    if (input_field_exist('f_re_day')) {
        if (input_field_value_is_empty('f_re_day')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter Day"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#input-day');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    if (input_field_exist('f_re_month')) {
        if (input_field_value_is_empty('f_re_month')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter Month"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#input-month');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    if (input_field_exist('f_re_year')) {
        if (input_field_value_is_empty('f_re_year')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter Year"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#input-year');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    if (input_field_exist('f_id')) {
        if (input_field_value_is_empty('f_id')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter your Id"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#input-id');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    //
    var m_city = '';
    if (input_field_exist('f_city')) {
        m_city = input_field_value('f_city');
        if (input_field_value_is_empty('f_city')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter your City"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#input-city');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    var m_street = '';
    if (input_field_exist('f_street')) {
        m_street = input_field_value('f_street');
        if (input_field_value_is_empty('f_street')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter your Street"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#input-street');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    var m_building = '';
    if (input_field_exist('f_building')) {
        m_building = input_field_value('f_building');
        if (input_field_value_is_empty('f_building')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter your Building"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#input-building');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    var m_apartments = '';
    if (input_field_exist('f_apartments')) {
        m_apartments = input_field_value('f_apartments');
        if (input_field_value_is_empty('f_apartments')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter your Apartments"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#input-apartments');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    //
    if (input_field_exist('f_terms')) {
        if (!$('input[name=f_terms]').is(':checked')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please confirm your agreement with the Rules"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    }
    // console.log("input_field_exist('f_yearsold') = ", input_field_exist('f_yearsold'));
    // console.log("checked = ", $('input[name=f_yearsold]').is(':checked'));
    if (input_field_exist('f_yearsold')) {
        if (!$('input[name=f_yearsold]').is(':checked')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please confirm that you are over 18 years old"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    }
    let m_reklama = "1";
    if (input_field_exist('f_reklama')) {
        if ($('input[name=f_reklama]').is(':checked')) {
            m_reklama = "1"
        }
    }
    $.ajax({
        type: "GET",
        async: false,
        data: {
            u_name: m_name
        },
        url: "/check-username/",
        success: function (res) {
            console.log("check-username success");
            if (res.AnswerCod === "00") {
                console.log("check-username ok");
            } else {
                Swal.fire({
                    icon: 'error',
                    title: gettext('ERROR'),
                    background: '#cacaca',
                    html: gettext("User with this login already exists"),
                    confirmButtonText: gettext('Back to form'),
                    confirmButtonColor: '#d33',
                });
                return false;
            }
        },
        error: function (res) {
            console.log("check-username error");
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occurred during user verification, please try again later"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    });
    $.ajax({
        type: "POST",
        async: false,
        data: {
            f_name: m_name,
            f_email: m_email,
            f_password: m_password,
            f_re_password: m_re_password,
            f_phone: m_phone,
            f_day: m_re_day,
            f_month: m_re_month,
            f_year: m_re_year,
            f_id: m_id,
            f_city: m_city,
            f_street: m_street,
            f_building: m_building,
            f_apartments: m_apartments,
            f_reklama: m_reklama,
            f_url_path: m_url_path,
            f_get_param: m_get_param,
            f_game_gift_id: m_game_gift_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/register-user/",
        success: function (res) {
            if (res.AnswerCod === "00") {
                $('.js-modal__register').modal('hide');
                location.href = "/registration-ok/";
                // Swal.fire({
                //     type: "success",
                //     icon: 'success',
                //     title: gettext('Registration completed'),
                //     background: '#ffffff',
                //     html: gettext("Registration completed successfully, follow the instructions in the mail"),
                //     confirmButtonText: gettext('OK'),
                //     confirmButtonColor: '#33c833',
                //     });
                // return true;
            }
            else if (res.AnswerCod === "00gift") {
                $('.js-modal__register').modal('hide');
                location.href = res.RedirectUrl;
            }
            else {
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
                html: gettext("An error occurred while creating the user profile, please try again later"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#dd3333',
            });
            return false;
        }
    });
}


function btn_modal_login() {
    console.log("btn_modal_login");
    var m_email = "";
    if (input_field_exist('fl_email')) {
        m_email = input_field_value('fl_email');
    }
    var m_password = "";
    if (input_field_exist('fl_password')) {
        m_password = input_field_value('fl_password');
    }
    var isValid;
    if (input_field_exist('fl_email')) {
        if (input_field_value_is_empty('fl_email')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter your Email/Login"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#id_fl_email');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
        isValid = validateEmail(input_field_value('fl_email'));
        if (!isValid) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Invalid email format"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#id_fl_email');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    if (input_field_exist('fl_password')) {
        if (m_password.length < 6) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext('Password cannot be less than 6 characters.'),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#id_fl_password');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    $.ajax({
        type: "GET",
        data: {
            fl_email: m_email,
            fl_password: m_password
        },
        url: "/check-userlogin/",
        success: function (res) {
            console.log("res = ", res)
            if (res.AnswerCod === "00") {
                console.log("check-userlogin ok");
                $("#id_form_login").submit();
            } else {
                Swal.fire({
                    icon: 'error',
                    title: gettext('ERROR'),
                    background: '#cacaca',
                    html: res.AnswerText,
                    confirmButtonText: gettext('Back to form'),
                    confirmButtonColor: '#d33',
                });
                return false;
            }
        },
        error: function () {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occurred during user verification, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    });
}


function btn_modal_recovery() {
    console.log("btn_modal_recovery");
    var m_email_recovery = "";
    if (input_field_exist('fl_email_recovery')) {
        m_email_recovery = input_field_value('fl_email_recovery');
    }
    var isValid;
    if (input_field_exist('fl_email_recovery')) {
        if (input_field_value_is_empty('fl_email_recovery')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter your Email/Login"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#id_fl_email_recovery');
            // if (mLine_wrong.length) {
            //     $('html,body').stop().animate({scrollTop: mLine_wrong.offset().top - 20}, '3000', 'swing');
            // }
            return false;
        }
        isValid = validateEmail(input_field_value('fl_email_recovery'));
        if (!isValid) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Invalid email format"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#id_fl_email_recovery');
            // if (mLine_wrong.length) {
            //     $('html,body').stop().animate({scrollTop: mLine_wrong.offset().top - 20}, '3000', 'swing');
            // }
            return false;
        }
    }
    $.ajax({
        type: "GET",
        data: {
            fl_email: m_email_recovery
        },
        url: "/check-loginrecovery/",
        success: function (res) {
            console.log("res = ", res)
            if (res.AnswerCod === "00") {
                console.log("check-userlogin ok");
                $("#id_form_recovery").submit();
            } else {
                Swal.fire({
                    icon: 'error',
                    title: gettext('ERROR'),
                    background: '#cacaca',
                    html: res.AnswerText,
                    confirmButtonText: gettext('Back to form'),
                    confirmButtonColor: '#d33',
                });
                return false;
            }
        },
        error: function () {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occurred during user verification, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    });
}


function btn_set_pass() {
    console.log("btn_set_pass");
    var m_password_1 = "";
    var m_password_2 = "";
    if (input_field_exist('fl_set_password1')) {
        m_password_1 = input_field_value('fl_set_password1');
    }
    if (input_field_exist('fl_set_password2')) {
        m_password_2 = input_field_value('fl_set_password2');
    }
    if (m_password_1 != m_password_2) {
        Swal.fire({
            icon: 'error',
            title: gettext('ERROR'),
            background: '#cacaca',
            html: gettext('Password mismatch.'),
            confirmButtonText: gettext('Back to form'),
            confirmButtonColor: '#d33',
        });
        mLine_wrong = $('#id_set_password1');
        if (mLine_wrong.length) {
            $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
        }
        return false;
    }

    if (input_field_exist('fl_set_password1')) {
        if (m_password_1.length < 6) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext('Password cannot be less than 6 characters.'),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#id_set_password1');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    $("#id_form_set_pass").submit();
}


function btn_cab_pass() {
    console.log("btn_cab_pass");
    var m_password_1 = "";
    var m_password_2 = "";
    if (input_field_exist('f_u_password1')) {
        m_password_1 = input_field_value('f_u_password1');
    }
    if (input_field_exist('f_u_password2')) {
        m_password_2 = input_field_value('f_u_password2');
    }
    if (m_password_1 != m_password_2) {
        Swal.fire({
            icon: 'error',
            title: gettext('ERROR'),
            background: '#cacaca',
            html: gettext('Password mismatch.'),
            confirmButtonText: gettext('Back to form'),
            confirmButtonColor: '#d33',
        });
        mLine_wrong = $('#f_u_password1');
        if (mLine_wrong.length) {
            $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
        }
        return false;
    }

    if (input_field_exist('f_u_password1')) {
        if (m_password_1.length < 6) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext('Password cannot be less than 6 characters.'),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#f_u_password1');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    $("#id_form_cab_pass").submit();
}


function btn_payment_method() {
    console.log("btn_game_pay");
    let t = $(event.currentTarget);
    t.closest('.payment-method').find('.single-method').removeClass('active');
    t.addClass('active');
    let m_popup = t.data('popup');
    let m_paymethod = t.data('paymethod');
    let m_href = t.data('href');
    let m_text = $('#id_ItemPayment_' + m_paymethod).val();
    if (m_popup == "11") {
        Swal.fire({
            icon: 'warning',
            title: m_text,
            showCancelButton: true,
            // reverseButtons: true,
            confirmButtonText: gettext("Yes"),
            cancelButtonText: gettext("No")
        }).then((result) => {
            if (result.isConfirmed) {
                location.href = m_href;
            }
        })
    } else {
        mLine_wrong = $('#pay_checkbox_1');
        if (mLine_wrong.length) {
            var w_height = $(window).height();
            var top_items = 0;
            top_items = mLine_wrong.offset().top;
            console.log(" w_height = ", w_height, top_items);
            if (top_items >= w_height) {
                $('html,body').stop().animate({ scrollTop: top_items - 20 }, '3000', 'swing');
            }
        }
        return false;
    }
}


function btn_game_pay() {
    console.log("btn_game_pay");
    // Swal.fire({
    //     icon: 'warning',
    //     title: gettext("Are you sure?"),
    //     showCancelButton: true,
    //     confirmButtonColor: "#15b284",
    //     cancelButtonColor: "#DD6B55",
    //     confirmButtonText: gettext("Yes"),
    //     cancelButtonText: gettext("No"),
    //     reverseButtons: true
    // }).then((result) => {
    //     if (result.isConfirmed) {
    let m_pay_ticket_type = $('#id_pay_ticket_type').val();
    let m_pay_ticket_col = $('#id_pay_ticket_col').val();
    let m_pay_method = "";
    let m_pay_game_id = $('#id_pay_game_id').val();
    let m_pay_ads = "0";

    if ($('#pay_checkbox_ads').length) {
        if ($('#pay_checkbox_ads').is(":checked")) {
            m_pay_ads = "1";
        }
    }

    m_mm = $('.payment-method').find('.single-method.active');
    if (m_mm) {
        m_pay_method = m_mm.data('paymethod');
    }
    $.ajax({
        type: "POST",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            pay_ticket_type: m_pay_ticket_type,
            pay_ticket_col: m_pay_ticket_col,
            pay_method: m_pay_method,
            pay_game_id: m_pay_game_id,
            pay_ads: m_pay_ads,
        },
        url: "/cab-game-paybtn/",
        success: function (res) {
            console.log("success");
            console.log(res);
            if (res.AnswerCod == "01") {
                console.log("AnswerCod: 01");
                window.location.href = res.AnswerHref;
            }
            if (res.AnswerCod == "00") {
                return Swal.fire({
                    icon: 'error',
                    title: gettext("Error"),
                    text: res.AnswerText,
                    confirmButtonColor: "#15b284",
                    confirmButtonText: gettext("Ok"),
                });
            }
        },
        error: function (res) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occured, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            console.log("error");
            return false;
        }
    });
    //     } else {
    //         // 'OK my boss, I didn\'t think you were so greedy'
    //         Swal.fire(gettext('Thank you and goodbye'), '', 'info');
    //         return false;
    //     }
    // });
}


function btn_ticket_check_send() {
    console.log('btn_ticket_check_send');
    let m_ticket_id = $('#id_ticket_active').val();
    let m_ticket_id_status = $('#id_ticket_active_status').val();
    console.log('m_ticket_id = ', m_ticket_id);
    $.ajax({
        async: false,
        type: "POST",
        data: {
            ticket_id: m_ticket_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cab-game-play-ticket-send-status/",
        success: function (res) {
            if (res.AnswerCod === '01') {
                if (res.game_finish) {
                    $('#id_btn_ap').addClass('disabled');
                    $('#id_btn_ng').removeClass('disabled');
                    $('#id_btn_rg').removeClass('disabled');
                }
            }
            if (res.AnswerCod === "00") {
                return Swal.fire({
                    icon: 'error',
                    title: gettext("Error"),
                    text: res.AnswerText,
                    confirmButtonColor: "#15b284",
                    confirmButtonText: gettext('Back to form'),
                });
            }
        },
        error: function (res) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occured, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            console.log("error");
            return false;
        }
    });
}


function btn_ticket_result(ticket_id) {
    console.log('btn_ticket_result');
    $("#ResTicketAjax").html("");
    $.ajax({
        type: "POST",
        data: {
            ticket_id: ticket_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/ticket_result/",
        success: function (res) {
            console.log("success");
            $("#ResTicketAjax").html(res);
            if (res != 'error' && res != 'ok') {
                return swal({
                    title: gettext("Ошибка"),
                    text: res,
                    type: "warning",
                    animation: false,
                    showCancelButton: false,
                    confirmButtonColor: "#15b284",
                    confirmButtonText: gettext("Ок"),
                    closeOnConfirm: true
                }).then(function (isConfirm) {
                    if (isConfirm === true) {
                        $('.modal-content').removeClass('modal-content-error');
                        return false;
                    } else {
                        $('.modal-content').removeClass('modal-content-error');
                        return false;
                    }
                });
            }
        },
        error: function (res) {
            console.log("error");
        }
    });


    //    var t;
    //    e.preventDefault();
    //    t = $(this);
    //    var field_station;
    //    field_station = t.closest('.js-stat_station');

    //    $('#id_modal_inhour_station').html(field_station.data("station"));
    return $('.js-modal__ticket_rezult').modal('show');

    // //            m_res = simple_get('/delete_ad_from_favorite', {ad_id: ad_id});
    // //            console.log("m_res = ", m_res);
    // //            $('#id_my_favorites_ads').html(m_res.my_favorites_ads)
    // //            console.log("m_res = ", m_res.my_drafts_tender);
    // //            $('#id_my_favorites_tender').html(m_res.my_favorites_tender)
    // //            $('#tender-' + ad_id).hide();
    //        }
    //    })
}


function btn_ticket_result_send() {
    console.log('btn_ticket_result_send');
    let m_ticket_id = $('#id_ticket_active').val();
    let m_ticket_id_status = $('#id_ticket_active_status').val();
    console.log('m_ticket_id = ', m_ticket_id);
    $.ajax({
        async: false,
        type: "POST",
        data: {
            ticket_id: m_ticket_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cab-game-play-ticket-send-status/",
        success: function (res) {
            if (res.AnswerCod === '01') {
                if (res.game_finish) {
                    $('#id_btn_ap').addClass('disabled');
                    $('#id_btn_ng').removeClass('disabled');
                    $('#id_btn_rg').removeClass('disabled');
                }
            }
            if (res.AnswerCod === "00") {
                return Swal.fire({
                    icon: 'error',
                    title: gettext("Error"),
                    text: res.AnswerText,
                    confirmButtonColor: "#15b284",
                    confirmButtonText: gettext('Back to form'),
                });
            }
        },
        error: function (res) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occured, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            console.log("error");
            return false;
        }
    });
}

$('#pay_checkbox_1').change(function () {
    if ($('#pay_checkbox_2').length) {
        if ($('#pay_checkbox_1').is(":checked") && $('#pay_checkbox_2').is(":checked")) {
            $('#id_btn_pur').removeClass('disabled');
        } else {
            $('#id_btn_pur').addClass('disabled');
        }
    } else {
        if ($('#pay_checkbox_1').is(":checked")) {
            $('#id_btn_pur').removeClass('disabled');
        } else {
            $('#id_btn_pur').addClass('disabled');
        }
    }
});

$('#pay_checkbox_2').change(function () {
    if ($('#pay_checkbox_1').length) {
        if ($('#pay_checkbox_1').is(":checked") && $('#pay_checkbox_2').is(":checked")) {
            $('#id_btn_pur').removeClass('disabled');
        } else {
            $('#id_btn_pur').addClass('disabled');
        }
    } else {
        if ($('#pay_checkbox_2').is(":checked")) {
            $('#id_btn_pur').removeClass('disabled');
        } else {
            $('#id_btn_pur').addClass('disabled');
        }
    }
});


function startCanvas(l_pic_canvas) {
    console.log("startCanvas");
    'use strict';
    var isDrawing, lastPoint;
    var container = document.getElementById('js-container'),
        pic_img = document.querySelector('.js-pic_result'),
        pic_result_width = pic_img.width,
        pic_result_height = pic_img.height,
        canvas = document.getElementById('js-canvas'),
        canvasWidth = canvas.width,
        canvasHeight = canvas.height,
        ctx = canvas.getContext('2d'),
        image = new Image(),
        brush = new Image();
    // base64 Workaround because Same-Origin-Policy
    image.src = l_pic_canvas;
    image.onload = function () {
        // var width = Math.min(500, image.width);
        // var height = image.height * (width / image.width);
        var width = pic_result_width;
        var height = pic_result_height;
        canvas.width = width;
        canvas.height = height;
        canvasWidth = width;
        canvasHeight = height;
        ctx.drawImage(image, 0, 0, width, height);
        var m_pixels_0 = ctx.getImageData(0, 0, canvasWidth, canvasHeight);
        let m_scratch_box = $('.js-scratch_box');
        m_scratch_box.css('opacity', '1');
    };

    brush.src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFAAAAAxCAYAAABNuS5SAAAKFklEQVR42u2aCXCcdRnG997NJtlkk83VJE3apEma9CQlNAR60UqrGSqW4PQSO9iiTkE8BxWtlGMqYCtYrLRQtfVGMoJaGRFliijaViwiWgQpyCEdraI1QLXG52V+n/5nzd3ENnX/M8/sJvvt933/533e81ufL7MyK7NOzuXPUDD0FQCZlVn/+xUUQhkXHny8M2TxGsq48MBjXdAhL9/7YN26dd5nI5aVRrvEc0GFEBNKhbDjwsHh3qP/FJK1EdYIedOFlFAOgREhPlICifZDYoBjTna3LYe4xcI4oSpNcf6RvHjuAJRoVszD0qFBGmgMChipZGFxbqzQkJWVZUSOF7JRX3S4LtLTeyMtkkqljMBkPzHRs2aYY5PcZH/qLY1EIo18byQ6hBytIr3WCAXcV4tQHYvFxg3w3N6+Bh3OQolEoqCoqCinlw16JzTFJSE6PYuZKqvztbC2ex7bzGxhKu+rerjJrEEq+r9ieElJSXFDQ0Mh9zYzOzu7FBUWcO4Q9xbD6HYvhXhGLccVD5ZAPyfMqaioyOrBUgEv8FZXV8caGxtz8vLykhCWTnZIKmsKhUJnEYeKcKk2YYERH41G7UYnck1/WvAPOxsdLJm2+bEY0Ay0RNeqkytXQkoBZM4U5oOaoYSUkBGRtvnesrBZK4e4F6ypqSkuLy+v4KI99ZQxkfc6vZ4jNAl1wkbhG8LrhfNBCdkxmhYacvj/GOce+3K9MHHbDHUmicOufREELRIWch/DljzMsglutr+VIJO5KjGrVfZAnpF8mnCd8G5hrnC60Cl8T/iw8C1hKd9P9eDCMcgo5HwBx8BB/g7xeRPkrBbeJ3xTeAxjvRGVV3NcshfPG1JX4tVDQae47GuVOknCi23xHr5nyrxe2C1sFlYJ7xe+Jlwm7BRulItP0ms957RzTMK1ws41jMS8eDxehopaOCYfxc3AIHcIX+K6nxW+ImyVF1i8PQ8DTuwtdC1atCja3NwcHkq5EuXmo85G+jq+yMm28V4q/zcIPxV+K9zPxnbgTi0ocybu6wX66fx/vfAB4T1gHt8xI1wlXMF5zEXnQKC56ruEjwhvEa4WrrXvK/Yt5Pt5I1UveeVKyKmT+lpG2gQ2npMmez8ZzFT3e+HXwj7hKXNf6rFZbDpJUjESLdFsFX4mfFv4Fd/7qPBm4UPCJ4RNwncwym4UfYVUtiAcDk/T+3NRmylwWzAY7BCBCwYYogZPnrJoRNm2IDc3tw4FVKXFm95UmGLzkTTFpog524WnhQPCQeGvwiPCCuFCYmk5GbEJt3tOeF54HPVeLLyXxHOv8BPhYaFLeFU4gsI7OWeZk3g+hpJNvVMGIIqhdRvy+biVISouq2TBqWxoIL1wgBhU5AR1SzJvFR4UnhX+Bl4RfsFGP0npUkTymIQ7fh8Cf4l6F0LgXkj6o3O+buGfwj+ElzGQETaNeJqPhxiahckYq8KJ9V6mP+4pTIATjsGCA8lCQVy9VbhB2CM8itu9IBxlkx6O4nbmmpcSi0KUExa3Psfn23DZC4lhlhRuIWs/R1Y9BrpR4WHcfiOq34bLl5DJm1B7BANPGO4+2OJfDcVwX+RZkL5d+DRqeRJ360IJx1CFp4w/8/lhVGXxay1xKp8asQ31rSbgz2az1aBBWCZsgKTfEFe7uM4xYus9KHWXcBv3eolwJe67hJLIN6yubMVpW1tbbllZWVxtzjRquvQe9981IG3RZHUQttH7hB8IP0cdLwp/YnNHcdsjEP1xsEruO56i2Fy3UWXMskAgYAH/EjOiCD6NDc/XZ4v12RqSy3WQ9rJD3jPClwkZz2Aoy8JnUEjPcwYWfgfHvcIW84h308mABQP4Xp02OY44M4tSZSfx7UXIewU3NpXuxw0vJzauYDP1XM8y8Ttx67fhylYrdlAMW1x7h/BF3NWI+4PwFwjbSha26/xQuBmib6HDqeI+m4m5wzrj9A/xO+O5qbm4yizcbDOKfAjVWeC/WzAFLSeI+4hN9WzQ65EvED7D8Tt4vwE33O64rIfD1JW3k6xeQoX3UN6chyG8In4tcbHuRAyKw2ktVIIM2U5XcA7t2FKy5vWQeBexbbrTpvmZiJwN6e3EwKspW/ajqBuAKfKQk8m7KIce5bgnMNQDkLWPUmkj511DSVV5HJOd417FzrDAK7RjZLMZiURigmLVFCYs5tI2PFhpcUj/n6z6sp72LwJKiU2rUdp62rA7IX4XytpJ3Weh4XfE1/0kk/uoFX8kbCHudZLld5E8vJIs2+mbT8iznaR60DHMBt0EE1DySVlSsOBvyrL6zkZG5qI2T/QSBYTHMYAlq2tw1+0MFO4kVj5GSbSbgvkA8fQQr1uIdfdD5mZ1GhZbP0XfuwlPmOp0SNkYbkQV2JdlEsq69VJS+rTER+NtZVC+TX+NRFq1XGeiHXbGUHMg6lk2/DiZ+mHU8wTueoTXLtS3F5e9l2PNZW9lyrOB5LGSmJokzMQ6OjqCA3wsMXLLhqrWoZgKe3lyZ5YtLiwsLLfMLhJL0ibW3rKa7oMQ+Ajq6gKHcMeHeP8qZcpRMvyt1J97SRabcNP1ZGsbKhSb6lF+5GR6shUnlqTSyPM7LZxV/PUqjOfTH6cvqx+XyN3aCfBPUWh3UZIcxC2/jgu/BJ7Eve/G1R/EXS9gaLCc0dgySqIm7jV4MhEYdAaN4R4eRHkBusJp3GNp56iSOscyYN0DaUch8Ai13X6yrg0PvotCO8nme0geKymBaulc1qO+NbxOOpHZtrcHR+nT6+wePvcnk8k8qv6iNBdyH4/OoGR5gXbv75D4NIX3NoruLSjtKmLlbTwCKER1NmV+QIqfS13aai0izUHsRKksAQE5g0w4fuehj9f+xb25Ym1tbcIhuw2COmkBn2cAcQAFbsclV1BTns49JZio3EQWPkgCySJpFIu8aor0UfeLigDTlUTa/8eimhRGuUiKOZPYtYNabh9EGik3Mkk+A9I8JTWoAiik/LEpzY8tY4uwWc4AJMjxQd8oXRHU8JqbW32orNyAiubZo0WR5wX9KyHrLpLD52nrxhFHa1CVV5w3081cRu/7BYichpEqfafA7/sCzhT7tVkhLZvhTeB8Gv1r6U+ty/gqtWHQCSNTcPOl9NmXM1S4hgRjBjjL1MdUJ8cx3uhe3d3dfh5Meb8qyKWsuJRidwtN/h20XEtxvTwya7tKncU8ACqmXVwLict5fy6TnFhra2uW7xT8dWk2BHptVBOx8GLKjo3g7bhrBQq1sdVsCvEkhLZIac1y/zmUSO0oO8fX/0P2Ub3cwaWpZSITnLnOpDlBWTIfMleJqFb10jXCBJUlMyORSIP14LhqNef6v/05bpZTdHulUyXKsufDNdRxZ4vIhSKwhQFG5vfLfcwZsx2X92Jhje8/P8OI+TK/oO+zeA84WTzkvI/6RuB3y6f68qf11xnyMiuzMms4178AwArmZmkkdGcAAAAASUVORK5CYII=';
    canvas.addEventListener('mousedown', handleMouseDown, false);
    canvas.addEventListener('touchstart', handleMouseDown, false);
    canvas.addEventListener('mousemove', handleMouseMove, false);
    canvas.addEventListener('touchmove', handleMouseMove, false);
    canvas.addEventListener('mouseup', handleMouseUp, false);
    canvas.addEventListener('touchend', handleMouseUp, false);

    $(window).resize(respondCanvas);
    function respondCanvas() {
        console.log("resize");
        pic_img = document.querySelector('.js-pic_result');
        // pic_result_width = pic_img.width;
        // pic_result_height = pic_img.height;
        // console.log("pic_result_width  = ", pic_result_width);
        // console.log("pic_result_height = ", pic_result_height);
        // let n_width = pic_result_width;
        // let n_height = pic_result_height;
        // console.log("n_width  = ", n_width);
        // console.log("n_height = ", n_height);
        //
        // console.log("n_width old  = ", canvas.width);
        // console.log("n_height old = ", canvas.height);

        let n_width_old = canvas.width;
        let n_height_old = canvas.height;
        let n_width_new = pic_img.width;
        let n_height_new = pic_img.height;

        // console.log("n_width_old  = ", n_width_old);
        // console.log("n_height_old = ", n_height_old);
        // console.log("n_width_new  = ", n_width_new);
        // console.log("n_height_new = ", n_height_new);

        if (n_width_old != n_width_new || n_height_old != n_height_new) {
            canvas.width = n_width_new;
            canvas.height = n_height_new;
            ctx.drawImage(image, 0, 0, n_width_new, n_height_new);
            // var m_pixels_0 = ctx.getImageData(0, 0, canvasWidth, canvasHeight);
        }
    }

    function distanceBetween(point1, point2) {
        return Math.sqrt(Math.pow(point2.x - point1.x, 2) + Math.pow(point2.y - point1.y, 2));
    }

    function angleBetween(point1, point2) {
        return Math.atan2(point2.x - point1.x, point2.y - point1.y);
    }
    // Only test every `stride` pixel. `stride`x faster,
    // but might lead to inaccuracy
    function getFilledInPixels(stride) {
        if (!stride || stride < 1) {
            stride = 1;
        }
        var pixels = ctx.getImageData(0, 0, canvasWidth, canvasHeight),
            pdata = pixels.data,
            l = pdata.length,
            total = (l / stride),
            count = 0;
        for (var i = count = 0; i < l; i += stride) {
            if (parseInt(pdata[i]) === 0) {
                count++;
            }
        }
        return Math.round((count / total) * 100);
    }

    function getMouse(e, canvas) {
        var offsetX = 0, offsetY = 0, mx, my;

        var div = document.getElementById('id-scratch_box');
        var divRect = div.getBoundingClientRect();
        var m_divRect_y = divRect.y;

        if (canvas.offsetParent !== undefined) {
            do {
                offsetX += canvas.offsetLeft;
                offsetY += canvas.offsetTop;
            } while ((canvas = canvas.offsetParent));
        }
        // mx = (e.pageX || e.touches[0].clientX) - offsetX;
        // my = (e.pageY || e.touches[0].clientY) - offsetY;
        mx = (e.pageX || e.touches[0].clientX) - offsetX;

        var offsetTop = offsetY;
        if (isMobile.Android()) {
            offsetTop = m_divRect_y;
        }
        my = (e.pageY || e.touches[0].clientY) - offsetTop;
        // my = (e.pageY || e.touches[0].clientY) - offsetY;
        // my = (e.pageY || e.touches[0].clientY) - m_divRect_y;
        return { x: mx, y: my };
    }

    function handlePercentage(filledInPixels) {
        filledInPixels = filledInPixels || 0;
        if (filledInPixels > 98) {
            canvas.parentNode.removeChild(canvas);
            btn_ticket_result_send();
            PollingTicketInfo();
        }
    }

    function handleMouseDown(e) {
        isDrawing = true;
        lastPoint = getMouse(e, canvas);
    }

    function handleMouseMove(e) {
        if (!isDrawing) {
            return;
        }
        e.preventDefault();
        var currentPoint = getMouse(e, canvas),
            dist = distanceBetween(lastPoint, currentPoint),
            angle = angleBetween(lastPoint, currentPoint),
            x, y;

        for (var i = 0; i < dist; i++) {
            // x = lastPoint.x + (Math.sin(angle) * i) - 25;
            x = lastPoint.x + (Math.sin(angle) * i) - 30;
            y = lastPoint.y + (Math.cos(angle) * i) - 30;

            ctx.globalCompositeOperation = 'destination-out';
            ctx.drawImage(brush, x, y);
        }
        lastPoint = currentPoint;
        // handlePercentage(getFilledInPixels(32));
        handlePercentage(getFilledInPixels(25));
    }

    function handleMouseUp(e) {
        isDrawing = false;
    }
}

function ClearCanvas() {
    var canvas = document.getElementById("js-canvas");
    if (!canvas) return;
    canvas.parentNode.removeChild(canvas);
    btn_ticket_result_send();
    PollingTicketInfo();
}


$('.js-btn_ticket_info').click(function () {
    // console.log("js-btn_ticket_info");
    let t = $(this);
    let m_ticket_id = t.data("id");
    $.ajax({
        async: false,
        type: "POST",
        data: {
            ticket_id: m_ticket_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cab-game-play-ticket-info/",
        success: function (res) {
            console.log("res = ", res);
            if (res.AnswerCod === '01') {
                let m_scratch_box = $('.js-scratch_box');
                $('#id_ticket_active').val(t.data('id'));
                t.closest('.ui-table_tickets').find('.ui-btn_ticket_info').removeClass('active');
                $('#id_ticket_' + $('#id_ticket_active').val()).addClass('active');
                let m_status_new = res.t_status;
                if (m_status_new == "01") {
                    $('#id_btn_ap').removeClass('disabled');
                    if ($('.cab-play-info-text').length) {
                        $('.cab-play-info-text').hide();
                    }
                } else {
                    $('#id_btn_ap').addClass('disabled');
                    if ($('.cab-play-info-text').length) {
                        $('.cab-play-info-text').show();
                    }
                }
                if (res.s_canvas === '01') {
                    m_scratch_box.css('opacity', '0');
                    m_scratch_box.html(res.s_box_html);
                    //если картинка в кэше
                    if ($('.js-pic_result').complete || $('.myimg').readyState === 4) {
                        startCanvas(res.pic_canvas64);
                    }
                    //если картинка загружается в первый раз
                    else {
                        $('.js-pic_result').on('load', function () {
                            startCanvas(res.pic_canvas64);
                        });
                    }
                } else {
                    m_scratch_box.html(res.s_box_html);
                }
                var w_height = $(window).height();
                var w_width = $(window).width();
                var top_items = 0;
                top_items = m_scratch_box.offset().top;
                if (top_items >= w_height) {
                    $('html,body').stop().animate({ scrollTop: top_items - 60 }, '3000', 'swing');
                }
            }
            if (res.AnswerCod === "00") {
                return Swal.fire({
                    icon: 'error',
                    title: gettext("Error"),
                    text: res.AnswerText,
                    confirmButtonColor: "#15b284",
                    confirmButtonText: gettext('Back to form'),
                });
            }
        },
        error: function (res) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occured, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            console.log("error");
            return false;
        }
    });
});

function PollingTicketInfo() {
    console.log("PollingTicketInfo");
    let m_item_game_id = $('#id_item_game').val();
    let m_gift = $('#id_item_gift').val();
    console.log('GIFT?', m_gift)
    $.ajax({
        type: "POST",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            game_id: m_item_game_id,
        },
        url: "/cab-game-play-info/",
        success: function (res) {
            console.log(res);
            if (res.AnswerCod == "01") {
                let m_list_t = res.TicketInfo;
                $.each(m_list_t, function (index, value) {
                    $('#id_ticket_' + value.id).html(value.html);
                    $('#id_ticket_' + value.id).removeClass();
                    $('#id_ticket_' + value.id).addClass(value.class);
                });
                if (res.NextTimeout > 0) {
                    setTimeout(PollingTicketInfo, res.NextTimeout);
                }
                $('#id_ticket_' + $('#id_ticket_active').val()).addClass('active');
                let m_status_old = $('#id_ticket_active_status').val();
                let m_status_new = res.TicketDict["k" + $('#id_ticket_active').val()].status;
                let m_ticket_id = $('#id_ticket_active').val()
                let m_ticket_first = $('#id_ticket_' + m_ticket_id);
                // console.log("res.TicketDict = ", res.TicketDict);
                // console.log("ticket_active  = ", m_ticket_id);
                // console.log("status_old     = ", m_status_old);
                // console.log("status_new     = ", m_status_new);
                if (m_status_old != m_status_new) {
                    console.log("status ---------- ");
                    $('#id_ticket_active_status').val(m_status_new);
                    if (m_status_new == "01") {
                        $('#id_btn_ap').removeClass('disabled');
                        if ($('.cab-play-info-text').length) {
                            $('.cab-play-info-text').hide();
                        }
                    } else {
                        $('#id_btn_ap').addClass('disabled');
                        if ($('.cab-play-info-text').length) {
                            $('.cab-play-info-text').show();
                        }
                    }
                    m_ticket_first.click();
                } else {
                    // console.log("status ++++++++++ ");
                }
                console.log(res.WinSum)
                if (m_gift === "True" && res.GameFinish === true) {
                    $('.js-btn_autoplay').attr("hidden", true);
                    if (Number(res.WinSum) > 0) {
                        $('.js-btn_getwin').attr("hidden", false);
                        Swal.fire({
                            title: gettext('Result'),
                            background: '#cacaca',
                            html: gettext("Congratulations! you won ") + res.WinSum,
                            confirmButtonText: gettext('Back'),
                            confirmButtonColor: '#42f587',
                        });

                    } else {
                        Swal.fire({
                            title: gettext('Result'),
                            background: '#cacaca',
                            html: gettext("Unfortunately today you lost"),
                            confirmButtonText: gettext('Back'),
                            confirmButtonColor: '#d33',
                        });
                    }

                }
            }
            if (res.AnswerCod == "00") {
            }
        },
        error: function (res) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occurred, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    });
}


function btn_mob_code() {
    var m_item_game_id = $('#id_item_game').val();
    $.ajax({
        type: "POST",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            user_id: m_item_game_id,
        },
        url: "/cab-game-play-info/",
        success: function (res) {
            console.log(res);
            if (res.AnswerCod == "01") {
                let m_list_t = res.TicketInfo;
                $.each(m_list_t, function (index, value) {
                    $('#id_ticket_' + value.id).html(value.html);
                    $('#id_ticket_' + value.id).removeClass();
                    $('#id_ticket_' + value.id).addClass(value.class);
                });
                if (res.NextTimeout > 0) {
                    setTimeout(PollingTicketInfo, res.NextTimeout);
                }
                $('#id_ticket_' + $('#id_ticket_active').val()).addClass('active');
                let m_status_old = $('#id_ticket_active_status').val();
                let m_status_new = res.TicketDict["k" + $('#id_ticket_active').val()].status;
                let m_ticket_id = $('#id_ticket_active').val()
                let m_ticket_first = $('#id_ticket_' + m_ticket_id);
                // console.log("res.TicketDict = ", res.TicketDict);
                // console.log("ticket_active  = ", m_ticket_id);
                // console.log("status_old     = ", m_status_old);
                // console.log("status_new     = ", m_status_new);
                if (m_status_old != m_status_new) {
                    console.log("status ---------- ");
                    $('#id_ticket_active_status').val(m_status_new);
                    if (m_status_new == "01") {
                        $('#id_btn_ap').removeClass('disabled');
                        if ($('.cab-play-info-text').length) {
                            $('.cab-play-info-text').hide();
                        }
                    } else {
                        $('#id_btn_ap').addClass('disabled');
                        if ($('.cab-play-info-text').length) {
                            $('.cab-play-info-text').show();
                        }
                    }
                    m_ticket_first.click();
                } else {
                    // console.log("status ++++++++++ ");
                }
            }
            if (res.AnswerCod == "00") {
            }
        },
        error: function (res) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occured, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    });
}

function btn_mob_confirm() {

}


function btn_mob_code() {
    var m_item_game_id = $('#id_item_game').val();
    $.ajax({
        type: "POST",
        async: false,
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            user_id: m_item_game_id,
        },
        url: "/cab-game-play-info/",
        success: function (res) {
            console.log(res);
            if (res.AnswerCod == "01") {
                let m_list_t = res.TicketInfo;
                $.each(m_list_t, function (index, value) {
                    $('#id_ticket_' + value.id).html(value.html);
                    $('#id_ticket_' + value.id).removeClass();
                    $('#id_ticket_' + value.id).addClass(value.class);
                });
                if (res.NextTimeout > 0) {
                    setTimeout(PollingTicketInfo, res.NextTimeout);
                }
                $('#id_ticket_' + $('#id_ticket_active').val()).addClass('active');
                let m_status_old = $('#id_ticket_active_status').val();
                let m_status_new = res.TicketDict["k" + $('#id_ticket_active').val()].status;
                let m_ticket_id = $('#id_ticket_active').val()
                let m_ticket_first = $('#id_ticket_' + m_ticket_id);
                // console.log("res.TicketDict = ", res.TicketDict);
                // console.log("ticket_active  = ", m_ticket_id);
                // console.log("status_old     = ", m_status_old);
                // console.log("status_new     = ", m_status_new);
                if (m_status_old != m_status_new) {
                    console.log("status ---------- ");
                    $('#id_ticket_active_status').val(m_status_new);
                    if (m_status_new == "01") {
                        $('#id_btn_ap').removeClass('disabled');
                        if ($('.cab-play-info-text').length) {
                            $('.cab-play-info-text').hide();
                        }
                    } else {
                        $('#id_btn_ap').addClass('disabled');
                        if ($('.cab-play-info-text').length) {
                            $('.cab-play-info-text').show();
                        }
                    }
                    m_ticket_first.click();
                } else {
                    // console.log("status ++++++++++ ");
                }
            }
            if (res.AnswerCod == "00") {
            }
        },
        error: function (res) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occured, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    });
}

function btn_user_balance_edit(l_user_id, l_user, l_name, l_tel, l_balance) {
    console.log("btn_user_balance_edit");
    $('#id_balance_item').val(l_user_id);
    $('#id_balance_s01').html(l_user);
    $('#id_balance_s02').html(l_name);
    $('#id_balance_s03').html(l_tel);
    $('#id_balance_s04').html(l_balance);

    $('.js__modal_editbalance').modal('show');
}


function btn_user_profile_edit() {

}

function btn_user_profile_edit(l_user_id) {

    $("#id_UserProfileEdit").html("");
    $.ajax({
        type: "POST",
        data: {
            user_id: l_user_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cabb_user_profile_edit/",
        success: function (res) {
            $("#id_ResAjax").html(res);
            if (res != 'error' && res != 'ok') {
                return swal({
                    title: gettext("Ошибка"),
                    text: res,
                    type: "warning",
                    animation: false,
                    showCancelButton: false,
                    confirmButtonColor: "#15b284",
                    confirmButtonText: gettext("Ок"),
                    closeOnConfirm: true
                }).then(function (isConfirm) {
                    if (isConfirm === true) {
                        $('.modal-content').removeClass('modal-content-error');
                        return false;
                    } else {
                        $('.modal-content').removeClass('modal-content-error');
                        return false;
                    }
                });
            }
        },
        error: function (res) {
            console.log("error");
            return swal({
                title: gettext("Ошибка"),
                text: res,
                type: "warning",
                animation: false,
                showCancelButton: false,
                confirmButtonColor: "#15b284",
                confirmButtonText: gettext("Ок"),
                closeOnConfirm: true
            })
        }
    });
    return $('.js-modal__cabb_userprofileedit').modal('show');
}

function btn_user_balance_oparation(l_user_id) {
    console.log("btn_user_balance_oparation");
    $("#id_ResAjax_cabb_form").html("");
    $.ajax({
        type: "POST",
        async: false,
        data: {
            f_user_id: l_user_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cabb_user_balance_oparation/",
        success: function (res) {
            $("#id_ResAjax_cabb_form").html(res);
            return $('.js-modal__cabb_form').modal('show');
        },
        error: function (res) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occurred while creating the user profile, please try again later"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#dd3333',
            });
            return false;
        }
    });
}

//
// function btn_feedback_send(l_btn) {
//     $.ajax({
//         type: "POST",
//         data: {
//             feedback_id: $('#id_feedback_id').val(),
//             feedback_btn: l_btn,
//             feedback_text: $('#id_feedback_text').val(),
//             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
//         },
//         url: "/cabb_feedback_btn_save/",
//         success: function (res) {
//             if (res.AnswerCod == '01') {
//                 $('.js__modal_feedback_replay').modal('hide');
//                 location.reload();
//             } else {
//                 return Swal.fire({
//                     icon: 'error',
//                     title: gettext('ERROR'),
//                     background: '#cacaca',
//                     html: gettext("An error occured, please try again later."),
//                     confirmButtonText: gettext('Back to form'),
//                     confirmButtonColor: '#d33',
//                 });
//             }
//         },
//         error: function (res) {
//             return Swal.fire({
//                 icon: 'error',
//                 title: gettext('ERROR'),
//                 background: '#cacaca',
//                 html: gettext("An error occured, please try again later."),
//                 confirmButtonText: gettext('Back to form'),
//                 confirmButtonColor: '#d33',
//             });
//         }
//     })
// }


// function btn_ticketcheck_conf(l_param) {
//     m_payadd_id = $("#id_payadd_id").val();
//     $.ajax({
//         type: "POST",
//         data: {
//             f_id: m_payadd_id,
//             f_param: l_param,
//             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
//         },
//         url: "/cabb_ticketcheck_conf/",
//         success: function (res) {
//             location.reload();
//             return ;
//         },
//         error: function () {
//             Swal.fire({
//                 icon: 'error',
//                 title: gettext('ERROR'),
//                 background: '#cacaca',
//                 html: gettext("An error occurred during user verification, please try again later."),
//                 confirmButtonText: gettext('Back to form'),
//                 confirmButtonColor: '#d33',
//             });
//             return false;
//         }
//     });
// }
///////




function balance_set() {
    console.log("id  = ", $('#id_balance_item').val());
    console.log("bal = ", $('#id_balance_new').val());
    $.ajax({
        type: "POST",
        data: {
            balance_id: $('#id_balance_item').val(),
            balance_num: $('#id_balance_new').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cabb_balance_save/",
        success: function (res) {
            console.log(res);
            console.log(res.answer);
            if (res.AnswerCod == '01') {
                $('.js__modal_editbalance').modal('hide');
                location.reload();
            } else {
                return Swal.fire({
                    icon: 'error',
                    title: gettext('ERROR'),
                    background: '#cacaca',
                    html: gettext("An error occured, please try again later."),
                    confirmButtonText: gettext('Back to form'),
                    confirmButtonColor: '#d33',
                });
            }
        },
        error: function (res) {
            return Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occured, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
        }
    })
    // }
}

function feedback_replay(l_id) {
    console.log('feedback_replay');
    $("#id_ResAjax").html("");
    $.ajax({
        type: "POST",
        data: {
            f_feedback_id: l_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cabb_feedback_btn_info/",
        success: function (res) {
            console.log("success");
            $("#id_ResAjax").html(res);
            if (res != 'error' && res != 'ok') {
                return swal({
                    title: gettext("Ошибка"),
                    text: res,
                    type: "warning",
                    animation: false,
                    showCancelButton: false,
                    confirmButtonColor: "#15b284",
                    confirmButtonText: gettext("Ок"),
                    closeOnConfirm: true
                }).then(function (isConfirm) {
                    if (isConfirm === true) {
                        $('.modal-content').removeClass('modal-content-error');
                        return false;
                    } else {
                        $('.modal-content').removeClass('modal-content-error');
                        return false;
                    }
                });
            }
        },
        error: function (res) {
            console.log("error");
        }
    });
    return $('.js-modal__cabb_feedback').modal('show');
}


function btn_feedback_send(l_btn) {
    $.ajax({
        type: "POST",
        data: {
            feedback_id: $('#id_feedback_id').val(),
            feedback_btn: l_btn,
            feedback_text: $('#id_feedback_text').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cabb_feedback_btn_save/",
        success: function (res) {
            if (res.AnswerCod == '01') {
                $('.js__modal_feedback_replay').modal('hide');
                location.reload();
            } else {
                return Swal.fire({
                    icon: 'error',
                    title: gettext('ERROR'),
                    background: '#cacaca',
                    html: gettext("An error occured, please try again later."),
                    confirmButtonText: gettext('Back to form'),
                    confirmButtonColor: '#d33',
                });
            }
        },
        error: function (res) {
            return Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occured, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
        }
    })
}


function btn_payout_save() {
    if (input_field_exist('f_acc_name')) {
        if (input_field_value_is_empty('f_acc_name')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter your Account Name"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#id_acc_name');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            $('#id_acc_name').focus();
            return false;
        }
    }
    if (input_field_exist('f_name_bank')) {
        if (input_field_value_is_empty('f_name_bank')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter Name of the Bank"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            mLine_wrong = $('#id_name_bank');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            $('#id_name_bank').focus();
            return false;
        }
    }
    if (input_field_exist('f_branch')) {
        if (input_field_value_is_empty('f_branch')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter Branch number"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            $('#id_branch').focus();
            mLine_wrong = $('#id_branch');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    if (input_field_exist('f_acc_num')) {
        if (input_field_value_is_empty('f_acc_num')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter Account number"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            $('#id_acc_num').focus();
            mLine_wrong = $('#id_acc_num');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    if (input_field_exist('f_amount')) {
        if (input_field_value_is_empty('f_amount')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter Amount"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            $('#id_amount').focus();
            mLine_wrong = $('#id_amount');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    let m_balance = $('#id_balance').val();
    let m_amount = $('#id_amount').val();
    if (+m_amount <= 0 || +m_amount > +m_balance) {
        Swal.fire({
            icon: 'error',
            title: gettext('ERROR'),
            background: '#cacaca',
            html: gettext("Please enter correct Amount"),
            confirmButtonText: gettext('Back to form'),
            confirmButtonColor: '#d33',
        });
        $('#id_amount').focus();
        mLine_wrong = $('#id_amount');
        if (mLine_wrong.length) {
            $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
        }
        return false;
    }

    $("#id_form_payout").submit();

    // $.ajax({
    //     type: "POST",
    //     data: {
    //         m_acc_name: $('#id_acc_name').val(),
    //         m_name_bank: $('#id_name_bank').val(),
    //         m_branch: $('#id_branch').val(),
    //         m_acc_num: $('#id_acc_num').val(),
    //         m_amount: $('#id_amount').val(),
    //         csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    //     },
    //     url: "/payout_save/",
    //     success: function (res) {
    //         console.log("res = ", res)
    //         if (res.AnswerCod === "00") {
    //             console.log("check-userlogin ok");
    //             // $("#id_form_login").submit();
    //         } else {
    //             Swal.fire({
    //                 icon: 'error',
    //                 title: gettext('ERROR'),
    //                 background: '#cacaca',
    //                 html: res.AnswerText,
    //                 confirmButtonText: gettext('Back to form'),
    //                 confirmButtonColor: '#d33',
    //             });
    //             return false;
    //         }
    //     },
    //     error: function () {
    //         Swal.fire({
    //             icon: 'error',
    //             title: gettext('ERROR'),
    //             background: '#cacaca',
    //             html: gettext("An error occurred during user verification, please try again later."),
    //             confirmButtonText: gettext('Back to form'),
    //             confirmButtonColor: '#d33',
    //         });
    //         return false;
    //     }
    // });
}

function btn_payout_ok(l_pay_out_id) {
    $.ajax({
        type: "POST",
        data: {
            f_pay_out_id: l_pay_out_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cab_payout_ok/",
        success: function (res) {
            console.log("res = ", res)
            if (res.AnswerCod === "00") {
                location.reload();
            } else {
                Swal.fire({
                    icon: 'error',
                    title: gettext('ERROR'),
                    background: '#cacaca',
                    html: res.AnswerText,
                    confirmButtonText: gettext('Back to form'),
                    confirmButtonColor: '#d33',
                });
                return false;
            }
        },
        error: function () {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occurred during user verification, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    });
}


function btn_payout_block(l_pay_out_id) {
    console.log();
    $.ajax({
        type: "POST",
        data: {
            f_pay_out_id: l_pay_out_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cab_payout_block/",
        success: function (res) {
            console.log("res = ", res)
            if (res.AnswerCod === "00") {
                location.reload();
            } else {
                Swal.fire({
                    icon: 'error',
                    title: gettext('ERROR'),
                    background: '#cacaca',
                    html: res.AnswerText,
                    confirmButtonText: gettext('Back to form'),
                    confirmButtonColor: '#d33',
                });
                return false;
            }
        },
        error: function () {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occurred during user verification, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    });
}

function btn_payadd_save() {
    if (input_field_exist('f_add_file')) {
        if (input_field_value_is_empty('f_add_file')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please Select File"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            $('#id_add_file').focus();
            mLine_wrong = $('#id_add_file');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    if (input_field_exist('f_add_amount')) {
        if (input_field_value_is_empty('f_add_amount')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter Amount"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            $('#id_amount').focus();
            mLine_wrong = $('#id_add_amount');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    let m_amount = $('#id_add_amount').val();
    if (0 >= m_amount || m_amount > 500000) {
        Swal.fire({
            icon: 'error',
            title: gettext('ERROR'),
            background: '#cacaca',
            html: gettext("Please enter correct Amount"),
            confirmButtonText: gettext('Back to form'),
            confirmButtonColor: '#d33',
        });
        $('#id_amount').focus();
        mLine_wrong = $('#id_amount');
        if (mLine_wrong.length) {
            $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
        }
        return false;
    }

    $("#id_form_payadd").submit();
}


function btn_payadd_ok(l_payadd_id) {
    console.log('btn_payadd_ok');
    console.log('l_payadd_id = ', l_payadd_id);
    $("#id_ResPayAdd").html("");
    $.ajax({
        type: "POST",
        data: {
            f_payadd_id: l_payadd_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cabb_payadd_info/",
        success: function (res) {
            console.log("success");
            console.log(res);
            console.log($('#ResTicketAjax').length);
            $("#id_ResPayAdd").html(res);
            return $('.js-modal__cabb_payadd').modal('show');
        },
        error: function () {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occurred during user verification, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    });
}

function btn_payadd_conf(l_payadd_conf) {
    m_payadd_id = $("#id_payadd_id").val();
    $.ajax({
        type: "POST",
        data: {
            f_payadd_id: m_payadd_id,
            f_payadd_conf: l_payadd_conf,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cabb_payadd_conf/",
        success: function (res) {
            location.reload();
            return;
        },
        error: function () {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occurred during user verification, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    });
}

function btn_cabbpayout_edit(l_payout_id) {
    console.log('btn_cabbpayout_edit');
    console.log('l_payout_id = ', l_payout_id);
    $("#id_ResPayOut").html("");
    $.ajax({
        type: "POST",
        data: {
            f_payout_id: l_payout_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cabb_payout_info/",
        success: function (res) {
            console.log("res = ", res);
            $("#id_ResPayOut").html(res);
            return $('.js-modal__cabb_payout').modal('show');
        },
        error: function () {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occurred. Please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    });
}

function btn_form_find(is_export = false) {
    var _location = location.href;
    var _location_main = _location.split('?')[0];
    var _location_add = '';
    if ($('#id_find_date').length) {
        var m_date = $('#id_find_date').val();
        if (m_date !== '') {
            _location_add = _location_add + 'date=' + m_date;
        }
    }
    if ($('#id_find_date_range').length) {
        var m_date_range = $('#id_find_date_range').val();
        if (m_date_range != '') {
            _location_add = _location_add + 'daterange=' + m_date_range;
        }
    }

    if ($('#id_find_date_range_2').length) {
        var m_date_range_2 = $('#id_find_date_range_2').val();
        if (m_date_range_2 != '') {
            if (_location_add != '') {
                _location_add = _location_add + '&';
            }
            _location_add = _location_add + 'daterange_2=' + m_date_range_2;
        }
    }
    if ($('#id_find_date_range_empty').length) {
        var m_date_range = $('#id_find_date_range_empty').val();
        if (m_date_range != '') {
            if (_location_add != '') {
                _location_add = _location_add + '&';
            }
            _location_add = _location_add + 'daterange=' + m_date_range;
        }
    }
    if ($('#id_find_date_range_2_empty').length) {
        var m_date_range_2 = $('#id_find_date_range_2_empty').val();
        if (m_date_range_2 != '') {
            if (_location_add != '') {
                _location_add = _location_add + '&';
            }
            _location_add = _location_add + 'daterange_2=' + m_date_range_2;
        }
    }
    if ($('#id_find_datetime_range').length) {
        var m_datetime_range = $('#id_find_datetime_range').val();
        if (m_datetime_range != '') {
            if (_location_add != '') {
                _location_add = _location_add + '&';
            }
            _location_add = _location_add + 'datetimerange=' + m_datetime_range;
        }
    }

    if ($('#id_find_uname').length) {
        var m_uName = $('#id_find_uname').val();
        if (m_uName != '') {
            if (_location_add != '') {
                _location_add = _location_add + '&';
            }
            _location_add = _location_add + 'uName=' + m_uName;
        }
    }
    if ($('#id_find_uemail').length) {
        var m_uEmail = $('#id_find_uemail').val();
        if (m_uEmail != '') {
            if (_location_add != '') {
                _location_add = _location_add + '&';
            }
            _location_add = _location_add + 'uEmail=' + m_uEmail;
        }
    }
    if ($('#id_find_uphone').length) {
        var m_uPhone = $('#id_find_uphone').val();
        if (m_uPhone != '') {
            if (_location_add != '') {
                _location_add = _location_add + '&';
            }
            _location_add = _location_add + 'uPhone=' + m_uPhone;
        }
    }
    if ($('#id_find_uticket').length) {
        var m_uTicket = $('#id_find_uticket').val();
        if (m_uTicket != '') {
            if (_location_add != '') {
                _location_add = _location_add + '&';
            }
            _location_add = _location_add + 'uTicket=' + m_uTicket;
        }
    }
    if ($('#id_find_active').is(':checked')) {
        let m_active = 1;
        if (m_active == 1) {
            if (_location_add != '') {
                _location_add = _location_add + '&';
            }
            _location_add = _location_add + 'active=' + m_active;
        }
    }
    let weekdays = ''
    if ($('#id_day_1').is(':checked')) {
        weekdays += 1
    }
    if ($('#id_day_2').is(':checked')) {
        weekdays += 2
    }
    if ($('#id_day_3').is(':checked')) {
        weekdays += 3
    }
    if ($('#id_day_4').is(':checked')) {
        weekdays += 4
    }
    if ($('#id_day_5').is(':checked')) {
        weekdays += 5
    }
    if ($('#id_day_6').is(':checked')) {
        weekdays += 6
    }
    if ($('#id_day_7').is(':checked')) {
        weekdays += 7
    }
    if ($('#id_weekdays').length) {
        if (_location_add != '') {
            _location_add = _location_add + '&';
        }
        _location_add = _location_add + 'weekdays=' + weekdays;
    }
    if ($('#id_find_idcard').length) {
        let m_idcard = $('#id_find_idcard').val().trim();
        if (m_idcard != '') {
            if (_location_add != '') {
                _location_add = _location_add + '&';
            }
            _location_add = _location_add + 'uIdcard=' + m_idcard;
        }
    }
    let status = ''
    if ($('#id_conf_status_wait').is(':checked')) {
        status += 'wait-'
    }
    if ($('#id_conf_status_success').is(':checked')) {
        status += 'ok-'
    }
    if ($('#id_conf_status_reject').is(':checked')) {
        status += 'reject-'
    }
    if ($('#id_conf_status_repeat').is(':checked')) {
        status += 'repeat-'
    }
    if ($('#id_conf_statuses').length) {
        if (_location_add != '') {
            _location_add = _location_add + '&';
        }
        _location_add = _location_add + 'status=' + status;
    }
    if ($('#id_conf_only_paid').length) {
        if ($('#id_conf_only_paid').is(':checked')) {
            if (_location_add != '') {
                _location_add = _location_add + '&';
            }
            _location_add = _location_add + 'onlypaid=' + '1';
        }
    }
    let payout_status = ''
    if ($('#payout_status_new').is(':checked')) {
        payout_status += '00-'
    }
    if ($('#payout_status_ok').is(':checked')) {
        payout_status += '01-'
    }
    if ($('#payout_status_reject').is(':checked')) {
        payout_status += '02-'
    }

    if ($('#payout_statuses').length) {
        if (_location_add != '') {
            _location_add = _location_add + '&';
        }
        _location_add = _location_add + 'status=' + payout_status;
    }

    if (is_export) {
        if (_location_add != '') {
            _location_add = _location_add + '&';
        }
        _location_add = _location_add + 'is_export=' + 'true';
    }
    if (_location_add != '') {
        _location = _location_main + '?' + _location_add;
        location.href = _location;
    } else {
        location.href = _location_main;
    }

}

function btn_reports_export(l_verbal_exp) {
    console.log("btn_reports_load");
    var m_game_list = "";
    $('#bootstrap-duallistbox-selected-list_ option').each(function () {
        console.log("item = ", $(this).data('code'));
        if (m_game_list == '') {
            m_game_list = $(this).data('code');
        } else {
            m_game_list += ':' + $(this).data('code');
        }
    });

    console.log("m_game_list = ", m_game_list);
    var m_date_range = "";
    m_date_range = $('#reservation').val();
    var m_find_report_verbal = "";
    m_find_report_verbal = $('#id_find_report_verbal').val();
    console.log("m_find_report_verbal = ", m_find_report_verbal);
    var m_url = '/cab_reports_load/' + m_find_report_verbal + '/?date_range=' + m_date_range + '&game_list=' + m_game_list;
    console.log("m_url = ", m_url);
    window.open(m_url);
}



function StartTicketFirst() {
    var m_ticket_first = $('.ui-table_tickets').find('.js-btn_ticket_info').first();
    m_ticket_first.click();
}

function change_lang(lang_code) {
    console.log("change_lang = ", lang_code);
    $('input[name=language]').val(lang_code);
    $("#lang_form").submit();
}

$(function () {
    console.log('document load');
    header_init();
    return preloader();
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

$(document).ready(function () {
    $('#loading').hide();
});

var isMobile = {
    Android: function () {
        return navigator.userAgent.match(/Android/i);
    },
    BlackBerry: function () {
        return navigator.userAgent.match(/BlackBerry/i);
    },
    iOS: function () {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
    },
    Opera: function () {
        return navigator.userAgent.match(/Opera Mini/i);
    },
    Windows: function () {
        return navigator.userAgent.match(/IEMobile/i) || navigator.userAgent.match(/WPDesktop/i);
    },
    any: function () {
        return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
    }
};
//
//Date range picker
$('#id_find_date_range').daterangepicker({
    locale: {
        format: 'DD.MM.YYYY'
    }
});
$('#id_find_date_range_2').daterangepicker({
    locale: {
        format: 'DD.MM.YYYY'
    }
});
// Date picker
$('#id_find_date').daterangepicker({
    singleDatePicker: true,
    locale: {
        format: 'DD.MM.YYYY'
    }
});

//Date and time picker
// $('#id_find_datetime_range').datetimepicker({ icons: { time: 'far fa-clock' } });

// //Date range picker with time picker
$('#id_find_datetime_range').daterangepicker({
    timePicker: true,
    timePickerIncrement: 30,
    locale: {
        format: 'MM/DD/YYYY hh:mm A'
    }
});

// daterange picker with empty default value
$('#id_find_date_range_empty').daterangepicker({
    autoUpdateInput: false,
    locale: {
        cancelLabel: 'Clear',
        format: 'DD.MM.YYYY'
    }
});
$('#id_find_date_range_empty').on('apply.daterangepicker', function (ev, picker) {
    $(this).val(picker.startDate.format('DD.MM.YYYY') + ' - ' + picker.endDate.format('DD.MM.YYYY'));
});

$('#id_find_date_range_empty').on('cancel.daterangepicker', function (ev, picker) {
    $(this).val('');
});

// daterange picker 2 with empty default value
$('#id_find_date_range_2_empty').daterangepicker({
    autoUpdateInput: false,
    locale: {
        cancelLabel: 'Clear',
        format: 'DD.MM.YYYY'
    }
});
$('#id_find_date_range_2_empty').on('apply.daterangepicker', function (ev, picker) {
    $(this).val(picker.startDate.format('DD.MM.YYYY') + ' - ' + picker.endDate.format('DD.MM.YYYY'));
});

$('#id_find_date_range_2_empty').on('cancel.daterangepicker', function (ev, picker) {
    $(this).val('');
});


function btn_cashadd_save() {
    if (input_field_exist('f_cashadd_city')) {
        if (input_field_value_is_empty('f_cashadd_city')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter City"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            $('#id_cashadd_city').focus();
            mLine_wrong = $('#id_cashadd_city');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    if (input_field_exist('f_cashadd_street')) {
        if (input_field_value_is_empty('f_cashadd_street')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter Street"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            $('#id_cashadd_street').focus();
            mLine_wrong = $('#id_cashadd_street');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    if (input_field_exist('f_cashadd_building')) {
        if (input_field_value_is_empty('f_cashadd_building')) {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("Please enter Building"),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            $('#id_cashadd_building').focus();
            mLine_wrong = $('#id_cashadd_building');
            if (mLine_wrong.length) {
                $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
            }
            return false;
        }
    }
    let m_amount = $('#id_cashadd_amount').val();
    if (1000 > m_amount || m_amount > 11000) {
        Swal.fire({
            icon: 'error',
            title: gettext('ERROR'),
            background: '#cacaca',
            html: gettext("Please enter correct Amount"),
            confirmButtonText: gettext('Back to form'),
            confirmButtonColor: '#d33',
        });
        $('#id_cashadd_amount').focus();
        mLine_wrong = $('#id_cashadd_amount');
        if (mLine_wrong.length) {
            $('html,body').stop().animate({ scrollTop: mLine_wrong.offset().top - 20 }, '3000', 'swing');
        }
        return false;
    }
    $("#id_form_cashadd").submit();
}

function btn_payadd_ok(l_payadd_id) {
    console.log('btn_payadd_ok');
    console.log('l_payadd_id = ', l_payadd_id);
    $("#id_ResPayAdd").html("");
    $.ajax({
        type: "POST",
        data: {
            f_payadd_id: l_payadd_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: "/cabb_payadd_info/",
        success: function (res) {
            console.log("success");
            console.log(res);
            console.log($('#ResTicketAjax').length);
            $("#id_ResPayAdd").html(res);
            return $('.js-modal__cabb_payadd').modal('show');
        },
        error: function () {
            Swal.fire({
                icon: 'error',
                title: gettext('ERROR'),
                background: '#cacaca',
                html: gettext("An error occurred during user verification, please try again later."),
                confirmButtonText: gettext('Back to form'),
                confirmButtonColor: '#d33',
            });
            return false;
        }
    });
}

function btn_cabbcash_actiom(cash_id, l_action) {
    // BLOCK OK
    console.log("btn_cabbcash_ok");
    let m_title = "";
    if (l_action == "01") {
        m_title = gettext("CONFIRMATION");
    }
    if (l_action == "02") {
        m_title = gettext("BLOCK");
    }
    Swal.fire({
        icon: 'warning',
        title: m_title,
        html: gettext("Are you sure?"),
        showCancelButton: true,
        confirmButtonText: gettext("Yes"),
        cancelButtonText: gettext("No")
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                type: "POST",
                async: false,
                data: {
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    f_cash_id: cash_id,
                    f_cash_action: l_action,
                },
                url: "/cabb_cashadd_btn/",
                success: function (res) {
                    if (res.AnswerCod == "01") {
                        console.log("AnswerCod: 01");
                        location.reload();
                        return false;
                    }
                    if (res.AnswerCod == "00") {
                        return Swal.fire({
                            icon: 'error',
                            title: gettext("Error"),
                            text: res.AnswerText,
                            confirmButtonColor: "#15b284",
                            confirmButtonText: gettext("Yes"),
                        });
                    }
                },
                error: function (res) {
                    Swal.fire({
                        icon: 'error',
                        title: gettext('ERROR'),
                        background: '#cacaca',
                        html: gettext("An error occured, please try again later."),
                        confirmButtonText: gettext('Back to form'),
                        confirmButtonColor: '#d33',
                    });
                    console.log("error");
                    return false;
                }
            });
        }
    })
}

function btn_partner_action() {
    let t = $(event.currentTarget);
    let m_url = t.data('url');
    Swal.fire({
        icon: 'warning',
        title: gettext("Are you sure?"),
        html: gettext("You are transferred to an external site, all responsibility for your activity on the site is that of a direct fool, the responsibility and conduct of the site is your responsibility."),
        showCancelButton: true,
        confirmButtonText: gettext("Yes"),
        cancelButtonText: gettext("No")
    }).then((result) => {
        if (result.isConfirmed) {
            window.open(m_url, '_blank');
        }
    })
}


// function btn_task_user_select() {
//     // let t = $(event.currentTarget);
//     // let m_url = t.data('url');
//     let m_user_list = $(".js-task_user");
//     // m_user_list.find('.js-task_user_checkbox').each(function () {
//     //     mm_ = $.trim( $(this).html() )
//     // });
//     m_user_list.find('.js-task_user_checkbox').prop('checked', true);
// }
//
//
function btn_task_user_select() {
    let m_user_list = $(".js-task_user");
    m_user_list.find('.js-task_user_checkbox').prop('checked', true);
}

function btn_task_user_unselect() {
    let m_user_list = $(".js-task_user");
    m_user_list.find('.js-task_user_checkbox').prop('checked', false);
}
