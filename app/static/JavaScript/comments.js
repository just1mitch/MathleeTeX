$(document).on('submit', '#submit-comment', createComment);

$(document).on('input', '#comment', function() {
    $('#commentSubmit').prop('disabled', false);
    if ($(this).val().length > 250) {
        $('#commentError').html("Error: Comment length must be less than 250 characters (currently " + $(this).val().length + ")")
        $('#commentError').parent().show();
        $('#commentSubmit').prop('disabled', true);
    }
    else {
        $('#commentError').parent().hide();
        $('#commentSubmit').prop('disabled', false);
    }
})

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
            return null;
        }
    })
    $('.create-comment').val('');
    getComments($('#submit-answer').attr('qid')).then(comments => {
        $('#commentSection').prop('hidden', false);
        $('#commentSection').html(comments);
        $('.dateposted').each(timeSince);
    }).catch();
}

function getComments(qid) {
    return new Promise((resolve, reject) => {
        // load comment section
        $.ajax({
            type: 'GET',
            url: '/get_comments/' + qid,
            timeout: 30000,
            error: function (jqXHR, _, errorThrown) {
                alert('Error (' + jqXHR.status + '): ' + errorThrown);
                reject(errorThrown);
            },
            success: function(comments) {
                resolve(comments);
            }
        }); 
    });
}
