;!function(window, document, $, _$) {
    var body = $(document.body),
        w = $(window),
        cookie = 'admin-toolbar';

    function editableFormSubmit(e) {
        e.preventDefault();
        var form = $(this),
            loading = $('#editable-loading'),
            showError = function(msg) {
                if (msg) {
                    msg = ': ' + msg;
                } else {
                    msg = '';
                }
                alert('An error occurred' + msg);
                loading.hide();
                form.show();
            };
        form.hide();
        loading.show();

        if (window.__loader_presubmit) {
            window.__loader_presubmit(e, form, loading);
        }

        $.ajax(form.attr('action'), {
            type: form.attr('method'),
            data: form.serialize(),
            dataType: 'json',
            success: function(/*PlainObject*/data, /*String*/textStatus, /*jqXHR*/jqXHR){
                if (data.valid){
                    location.reload();
                } else {
                    form.html($(data.form).html());
                }
            },
            error: function(/*jqXHR*/jqXHR, /*String*/textStatus, /*String*/errorThrown){
                showError(errorThrown);
            },
        });
    }

    var editable = function(commands){
        commands["refresh"] = this.positionEditButtons;
    }

    editable.prototype.load = function(){
        // Add AJAX submit handler for each editable form.
        $('.editable-form').submit(editableFormSubmit);

        this.positionEditButtons();
        body.add('.editable');
        w.resize($.proxy(function(e) {
            this.positionEditButtons();
        }, this));

        // Show/hide the editable area's highlight when mousing over/out the of
        // the edit link.
        $('.editable-link').on('mouseenter', function(e) {
            $(this).next('.editable-highlight').css('visibility', 'visible');
        });

        $('.editable-link').on('mouseleave', function(e) {
            $(this).next('.editable-highlight').css('visibility', 'hidden');
        });

        // Add the toolbar HTML and handlers.
        var closed = this.getCookie(true);
        body.append(window.__toolbar_html);

        this.toolbar = $('#editable-toolbar');
        this.toggle = this.toolbar.children().first();
        this.links = $('.editable-link');

        this.toggle.text('<<');
        this.toggleToolbar(closed);

        this.toggle.click($.proxy(function(e) {
            e.preventDefault();
            this.toggleToolbar(this.toolbar.hasClass('toolbar-open'));
        }, this));
    }

    editable.prototype.getCookie = function(default_val){
        var at = ('; ' + document.cookie).indexOf('; ' + cookie + '=');
        if (at > -1) {
            return document.cookie.substr(at + cookie.length + 1).split(';')[0];
        }
        return default_val
    }

    editable.prototype.toggleToolbar = function(opened){
        opened?this.closeToolbar():this.openToolbar();
    }

    editable.prototype.openToolbar= function() {
        this.toggle.text('<<');
        this.toolbar.addClass('toolbar-open');
        this.links.addClass('editable-link-show');

        document.cookie = cookie + '=; path=/';
    }

    editable.prototype.closeToolbar = function() {
        this.toggle.text('>>');
        this.toolbar.removeClass('toolbar-open');
        this.links.removeClass('editable-link-show');

        document.cookie = cookie + '=1; path=/';
    }

    editable.prototype.positionEditButtons = function() {
        $('.editable-link').each(function() {
            var link = $(this),
                editable = $(link.attr('href')),
                form = link.prev('form'),
                highlight = link.next('.editable-highlight'),
                expose = {
                    color: '#333',
                    loadSpeed: 200,
                    opacity: 0.9
                },
                overlay = {
                    expose: expose,
                    closeOnClick: true,
                    close: ':button',
                    left: 'center',
                    top: 'center'
                };

            // Position the editable area's edit link.
            // Apply the editable area's overlay handler.
            link.offset({
                top: editable.offset().top + parseInt(link.css('margin-top')),
                left: editable.offset().left + parseInt(link.css('margin-left')) - link.outerWidth() - 1
            }).overlay(overlay);

            // Position the editable area's highlight.
            highlight.css({
                width: editable.width(),
                height: editable.height()
            }).offset({
                top: editable.offset().top,
                left: editable.offset().left
            });
        });
    }

    var commands = {},
        edit = new editable(commands);
    w.load($.proxy(edit.load, edit));
    _$['front_edit'] = function() {
        var method = arguments[0],
            args = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
        if (commands[method]) {
            return commands[method].apply(null, args);
        }
    };
}(this, document, window.__loader_jquery, jQuery);
