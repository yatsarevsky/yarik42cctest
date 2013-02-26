$(function(){
    $.datepicker.setDefaults(
        $.extend($.datepicker.regional["ru"])
    );
    $("#id_birth_date").datepicker({
        changeYear: "True",
        minDate: "-40y",
        dateFormat: "yy-mm-dd"
    });
});
