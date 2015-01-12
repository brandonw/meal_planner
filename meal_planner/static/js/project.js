/* Project specific Javascript goes here. */

$(document).ready(function() {
    $('a.tooltip-a').tooltip();
});

var removeDayRecipe = function(e) {
    e.preventDefault();
    var form = $(this);
    var postUrl = form.attr('action');
    $.post(postUrl, form.serialize()).done(function (data) {
        form.closest('li.list-group-item').remove();
    });
};
