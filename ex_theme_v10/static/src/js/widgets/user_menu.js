odoo.define('ex_theme_v10.UserMenu', function (require) {
"use strict";

var core = require('web.core');
var Dialog = require('web.Dialog');
var UserMenu = require('web.UserMenu');

var _t = core._t;
var QWeb = core.qweb;

UserMenu.include({
    on_menu_support: function () {
        window.location.href = 'https://www.odoo.com/help';
    },
    on_menu_shortcuts: function() {
        new Dialog(this, {
            size: 'large',
            dialogClass: 'o_act_window',
            title: _t("Keyboard Shortcuts"),
            $content: $(QWeb.render("UserMenu.shortcuts"))
        }).open();
    },
});

});
