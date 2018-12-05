$("document").ready(function() {
    $(document).on('click', '.btn-add', function(e) {
        e.preventDefault();

        let currentEntry = $(this).parents('.entry:first'),
            newEntry = $(currentEntry.clone()).insertAfter(currentEntry);

        currentEntry.find('.btn-add').removeClass('btn-add btn-success').addClass('btn-remove btn-danger').html('Delete');
        newEntry.find('input').val('');
    }).on('click', '.btn-remove', function(e) {
        e.preventDefault();
        $(this).parents('.entry:first').remove();
    });
});
