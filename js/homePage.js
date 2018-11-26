function selectAllGenres() {
    $(".genre-select-item").each(function(index) {
        $(this).prop("checked", true);
    });
}

function deSelectAllGenres() {
    $(".genre-select-item").each(function(index) {
        $(this).prop("checked", false);
    });
}

$("document").ready(function() {
    let pageURL = window.location.search.substring(1);
    let URLVariables = pageURL.split('&');
    for (let i = 0; i < URLVariables.length; i++) {
        let param = URLVariables[i].split('=');
        if (param[0] === "titleSearch") {
            $("#"+param[0]).prop("value", param[1]);
        } else {
            $("#"+param[0]).prop("checked", true);
        }
    }
});