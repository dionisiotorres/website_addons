// # -*- coding: utf-8 -*-
// #################################################################################
// # Author      : Kelvzxu (<https://kltech-intl.odoo.com/>)
// # Copyright(c): 2015-kltech-intl.
// # All Rights Reserved.
// #
// #
// # This program is copyright property of the author mentioned above.
// # You can`t redistribute it and/or modify it.
// #################################################################################

$(document).ready(function() {
    $('.oe_website_login_container').each(function(ev) {
        var elements = this;
        $(elements).on('click', 'div.input-group-append button.btn.btn-primary', function() {
            var icon = $(this).find('i.fa.fa-eye').length
            if (icon == 1) {
                $(this).find('i.fa.fa-eye').removeClass('fa-eye').addClass('fa-eye-slash');
                $(this).parent().prev('input[type="password"]').prop('type', 'text');
            } else {
                $(this).find('i.fa.fa-eye-slash').removeClass('fa-eye-slash').addClass('fa-eye');
                $(this).parent().prev('input[type="text"]').prop('type', 'password');
            }
        });
    });
});