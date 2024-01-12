$(document).ready(function() {
    const responseHandlers = {
        "sended": sended,
        "accepted": accepted,
        "rejected": rejected,
        "removed": removed,
    };
    const buttonIdFunctions = {
        "add_friend": add_friend,
        "remove_friend": remove_friend,
        "reject_request": reject_request,
        "cancel_request": cancel_request,
        "accept_request": accept_request
    }

    $(".friend_button").click(function(e) {
        var button = $(this);
        var id = button.attr("id")
        var data = {};
        data = buttonIdFunctions[id](button);
        var csrf = $('input[name=csrfmiddlewaretoken]').val()
        data.data.csrfmiddlewaretoken = csrf
        $.ajax({
            url: data.url,
            type: data.method,
            data: data.data,
            headers: {'X-CSRFToken': csrf },
            success: function(response) {
                    data = responseHandlers[response.status](button)

                    button.html(data.html);
                    button.attr("data-pk", response.id);},

            error: function(error){
                console.error("Error", error);
                location.reload();
                }
            })

    })
    function add_friend(button){
        var pk = button.attr("data-pk");
        var url = '/accounts/send_friend_request/';

        return {url: url, data: {user_pk: pk}, method: "POST"};
    }
    function reject_request(button){
        var pk = button.attr("data-pk");
        var url = '/accounts/reject_friend_request/' + pk;
        return {url: url, data: {}, method: "DELETE"};
    }
    function cancel_request(button){
        var pk = button.attr("data-pk");
        var url = '/accounts/reject_friend_request/' + pk;
        return {url: url, data: {}, method: "DELETE"};
    }
    function remove_friend(button){
        var pk = button.attr("data-pk");
        var url = '/accounts/remove_from_friends/' + pk;
        return {url: url, data: {}, method: "DELETE"};
    }
    function accept_request(button){
        var pk = button.attr("data-pk");
        var url = '/accounts/accept_friend_request/';
        return {url: url, data: {pk: pk}, method: "POST"};
    }

    function sended(button){
        button.attr("id", "reject_request");
        return {html: "Отменить заявку"};
    }

    function rejected(button){
        button.attr("id", "add_friend");
        button.closest(".frnd_btns").find("#accept_request").hide();
        return {html: "Добавить в друзья"};
    }

    function accepted(button){
        button.attr("id", "remove_friend");
        button.closest(".frnd_btns").find("#reject_request").hide();
        return {html: "Удалить из друзей"};
    }

    function removed(button){
        button.attr("id", "add_friend");
        return {html: "Добавить в друзья"};
    }
})