$(document).ready(function() {
    $('#edit_form').submit(function() {
        var $progress = $('#progress').show();
        var $form = $(this);
        var $inputs = $form.find(':input').prop('readonly', true);
        $form.addClass('loading_form');
        $form.ajaxSubmit({
            success: function(response) {
                $form.html($(response).find('#edit_form').html());
                $progress.hide();
                $inputs.prop('readonly', false);
                $form.removeClass('loading_form');
            }
        });
        return false;
    });
})
