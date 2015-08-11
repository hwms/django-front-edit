!function(window, $) {
    // Front edit namespace
    window.djangoFrontEdit = window.djangoFrontEdit || {};

    var body = $(document.body);
    var w = $(window);
    var cookieName = 'front-edit-admin-toolbar';
    var cookieValue = '1';
    var iconOpen = '&#8677;';
    var iconClose = '&#8676;';

    // Closure variables
    var toolbarElement;
    var toggleElement;
    var linkElements;

    function editableFormSubmit(e) {
        e.preventDefault();

        var form = $(e.currentTarget);
        var loading = $('#editable-loading');

        function showError(msg) {
            if (msg) {
                msg = ': ' + msg;
            } else {
                msg = '';
            }
            alert('An error occurred' + msg);
            loading.hide();
            form.show();
        }

        form.trigger('django-front-edit-form-pre-serialize');

        form.hide();
        loading.show();

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

    function load(){
        // Add AJAX submit handler for each editable form.
        $('.editable-form').submit(editableFormSubmit);

        linkElements = $('.editable-link');

        positionEditButtons();
        body.add('.editable');
        w.on('resize', positionEditButtons);

        // Show/hide the editable area's highlight when mousing over/out the of
        // the edit link.
        $('.editable-link').on('mouseenter', function(e) {
            $(e.currentTarget).next('.editable-highlight').css('visibility', 'visible');
        });

        $('.editable-link').on('mouseleave', function(e) {
            $(e.currentTarget).next('.editable-highlight').css('visibility', 'hidden');
        });

        // Add the toolbar HTML and handlers.
        var closed = cookieToolbarClosed();
        body.append(window.djangoFrontEdit.toolbarHtml);

        toolbarElement = $('#editable-toolbar');
        toggleElement = toolbarElement.children().first();

        toggleElement.html(iconClose);
        toggleToolbar(closed);

        toggleElement.click(function(e) {
            e.preventDefault();
            toggleToolbar(toolbarElement.hasClass('toolbar-open'));
        });
    }

    function cookieToolbarClosed(){
        var at = ('; ' + document.cookie).indexOf('; ' + cookieName + '=');

        if (at > -1) {
            at += cookieName.length + 1
            return document.cookie.substr(at).split(';')[0] === cookieValue;
        }

        return false;
    }

    function toggleToolbar(opened) {
        opened ? closeToolbar() : openToolbar();
    }

    function openToolbar() {
        toggleElement.html(iconClose);
        toolbarElement.addClass('toolbar-open');
        linkElements.addClass('editable-link-show');

        document.cookie = cookieName + '=; path=/';
    }

    function closeToolbar() {
        toggleElement.html(iconOpen);
        toolbarElement.removeClass('toolbar-open');
        linkElements.removeClass('editable-link-show');

        document.cookie = cookieName + '=' + cookieValue + '; path=/';
    }

    function positionEditButtons() {
        if (typeof linkElements === 'undefined'){
            return;
        }
        linkElements.each(function(i, link) {
            var link = $(link);
            var editable = $(link.data('editable-selector'));
            var form = link.prev('form');
            var highlight = link.next('.editable-highlight');

            var expose = {
                color: '#333',
                loadSpeed: 200,
                opacity: 0.9
            };

            var overlay = {
                expose: expose,
                closeOnClick: true,
                close: ':button',
                left: 'center',
                top: 'center'
            };

            // Position the editable area's edit link.
            // Apply the editable area's overlay handler.
            link.offset({
                top: editable.offset().top + parseInt(link.css('margin-top')) - 1,
                left: editable.offset().left + parseInt(link.css('margin-left')) - link.outerWidth() - 2
            })
            
            if (!link.hasClass('editable-admin-link')) {
                link.overlay(overlay);
            }

            // Position the editable area's highlight.
            // Subtract 1 from offset to account for highlight border.
            highlight.css({
                width: editable.outerWidth(),
                height: editable.outerHeight()
            }).offset({
                top: editable.offset().top - 1,
                left: editable.offset().left - 1
            });
        });
    }

    w.on('load', load);

    window.djangoFrontEdit.refresh = positionEditButtons;
    window.djangoFrontEdit.jQuery = $;
}(this, jQuery);
