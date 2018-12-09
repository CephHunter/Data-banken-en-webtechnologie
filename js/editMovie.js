$("document").ready(function() {
    $(document).on('click', '.btn-add', function(e) {
        e.preventDefault();

        let currentEntry = $(this).parents('.entry:first'),
            newEntry = $(currentEntry.clone()).insertAfter(currentEntry);

        currentEntry.find('.btn-add').prop('hidden', true);
        newEntry.find('input').val('');
    })
    .on('click', '.btn-remove', function(e) {
        e.preventDefault();
        if ($(this).parents('.entry:first').siblings().length > 0) {
            if ($(this).parents('.entry:first').next().length === 0) {
                $(this).parents('.entry:first').prev().find('.btn-add').prop('hidden', false);
            }
            $(this).parents('.entry:first').remove();
        } else {
            $(this).parents('.entry:first').find('input').val('');
        }
    });

    let checkboxes = $('#genres-container input');
    function checkCheckboxes(e) {
        if (checkboxes.is(':checked')) {
            checkboxes.prop('required', false);
        } else {
            checkboxes.prop('required', true);
        }
    }
    checkboxes.on('change', checkCheckboxes);
    checkCheckboxes();
});
