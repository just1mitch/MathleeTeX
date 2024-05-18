$(document).on('submit', '#submit-comment', createComment);

function createComment(e) {
    e.preventDefault();
    $.ajax({
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        type: "POST",
        url: "/create_comment/" + $('#submit-answer').attr('qid'),
        data: $(this).serialize(),
        timeout: 30000,
        error: function (jqXHR, _, errorThrown) {
            alert('Error (' + jqXHR.status + '): ' + errorThrown);
            return false;
        }
    })
    $('.create-comment').val('');
}