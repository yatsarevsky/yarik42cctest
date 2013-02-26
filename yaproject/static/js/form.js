$(document).ready(function() {
    $('#edit_form').submit(function() {
        $('#progress').show();
        var $inputs = $(this).find(':input');
        $inputs.prop('readonly', true);
        $(this).addClass('loading_form');
        $(this).ajaxSubmit({
            success: function(response) {
                if (response['ok']) {
                    $('#progress').hide();
                    $inputs.prop('readonly', false);
                    $('#edit_form').removeClass('loading_form');
                } else {
                    alert('somethig is wrong');
                    $inputs.prop('readonly', false);
                    $('#edit_form').removeClass('loading_form');
                    $('#progress').hide();
                }
            }
        });
        return false;
    });
})