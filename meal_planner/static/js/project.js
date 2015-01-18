/* Project specific Javascript goes here. */

$(document).ready(function() {
    $('a.tooltip-a').tooltip();
});

var removeDayRecipe = function(e) {
    e.preventDefault();
    var form = $(e.target);
    var postUrl = form.attr('action');
    $.post(postUrl, form.serialize()).done(function (data) {
        form.closest('li.list-group-item').remove();
    });
};

var updateRating = function(e) {
    e.preventDefault();
    var anchor = $(e.target);
    $.get(anchor.attr('href'), function (data) {
        var rating = anchor.text().trim();
        var recipeID = anchor.closest('li.list-group-item')
            .find('input:hidden').val();

        // when updating rating, make sure to update any other instances
        // of this recipe already displayed on the page
        var ratings = $('input:hidden[value=' + recipeID + ']').parent()
            .find('ul#dayrecipe-rating');
        ratings.removeClass();
        ratings.addClass('rating star' + rating);
    });
};
