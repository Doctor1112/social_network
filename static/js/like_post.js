$(document).ready(function() {

    $(".like").click(function(e) {
        const url = '/posts/like/';
        e.preventDefault();
        var likeButton = this;
        var likeCount = $(this).parent().find(".total");
        console.log(likeCount);
        $.ajax({
            url: url,
            type: "POST",
            data: { pk: likeButton.dataset.id , action: likeButton.dataset.action,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),},
            success: function(response) {
                    var previousAction = likeButton.dataset.action;
                    // переключить текст кнопки и атрибут data-action
                    var action = previousAction === 'like' ? 'unlike' : 'like';
                    console.log("hi");
                    likeButton.dataset.action = action;
                    likeButton.innerHTML = action;
                    // обновить количество лайков
                    var totalLikes = parseInt(likeCount.text());
                    console.log(totalLikes);
                    likeCount.html(previousAction === 'like' ? totalLikes + 1 : totalLikes - 1);
    
            },
            error: function(error) {
                console.error("Error editing comment", error);
            }
            })
    });
})