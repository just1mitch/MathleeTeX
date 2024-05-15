function timeSince(_, dateposted) {
    let date = new Date(dateposted.getAttribute('dateposted'));
    let seconds = Math.floor((new Date() - date) / 1000) + date.getTimezoneOffset() * 60;
    let interval = seconds / 31536000;
    if (interval > 1) {
        dateposted.innerText = Math.floor(interval) + " years ago";
        return;
    }
    interval = seconds / 2592000;
    if (interval > 1) {
        dateposted.innerText = Math.floor(interval) + " months ago";
        return;
    }
    interval = seconds / 86400;
    if (interval > 1) {
        dateposted.innerText = Math.floor(interval) + " days ago";
        return;
    }
    interval = seconds / 3600;
    if (interval > 1) {
        dateposted.innerText = Math.floor(interval) + " hours ago";
        return;
    }
    interval = seconds / 60;
    if (interval > 1) {
        dateposted.innerText = Math.floor(interval) + " minutes ago";
        return;
    }
    dateposted.innerText = Math.floor(interval) + " seconds ago";
}

function setTimes() {
    $('.dateposted').each(timeSince)
}

$(document).ready(function () {
    setTimes();
    setInterval(setTimes, 5000)
})

$('#answer').on('input', function () {
    $('#katexdyna').prop('hidden', false);
    try {
        katex.render($(this).val(), document.getElementById('katexdyna'), { throwOnError: false })
        // Also render to string - if there are errors, will catch and display underneath the rendered text
        katex.renderToString($(this).val())
        if ($(this).val().length === 0) $('#katexdyna').prop('hidden', true);
        $('#answerSubmit').prop('disabled', false);
        $('#katexErrorCode').prop('hidden', true);
        if (code.length > 50) {
            $('#codeError').html("Error: Code length must be less than 50 characters (currently " + code.length + ")")
            $('#codeError').parent().show();
            $('#answerSubmit').prop('disabled', true);
        }
        else {
            $('#codeError').parent().hide();
            $('#answerSubmit').prop('disabled', false);
        }

    }
    catch (e) {
        if (e instanceof katex.ParseError) {
            $('#katexErrorCode').html(e.message);
            $('#katexErrorCode').prop('hidden', false);
            // Prevent submitting form if katex is invalid
            $('#answerSubmit').prop('disabled', true);
        }
    }
})

function showModal(qid, code, title, difficulty, description, username, date_posted) {
    // setting individually as Safari doesn't support createElement 'options' feature
    // https://developer.mozilla.org/en-US/docs/Web/API/Document/createElement
    let btn = document.createElement("button");
    btn.setAttribute("type", "button");
    btn.setAttribute("id", "modalToggle");
    btn.setAttribute("class", "btn")
    btn.style.display = "none";
    btn.setAttribute("data-bs-toggle", "modal");
    btn.setAttribute("data-bs-target", "#answerModal");

    // render question
    try {
        katex.render(code, document.getElementsByClassName('modal-code')[0], { throwOnError: false });
    } catch (e) {
        console.error("KaTeX render error:", e);
    }

    // Add data to modal
    $('.modal-title').html(title);
    $('.modal-description').html(description);
    $('.modal-byline').html("Posted by " + username + " " + date_posted);
    $('#answer').val('');
    katex.render('', document.getElementById('katexdyna'), { throwOnError: false })
    if (difficulty == 'Easy') {
        $('.modal-difficulty').html("<span class='easy'>Easy</span>");
        $('.modal-difficulty').addClass('ps-4');
        $('.modal-difficulty').removeClass('ps-0');
    }
    else if (difficulty == 'Medium') {
        $('.modal-difficulty').html("<span class='medium'>Medium</span>");
        $('.modal-difficulty').addClass('ps-0');
        $('.modal-difficulty').removeClass('ps-4');
    }
    else if (difficulty == 'Hard') {
        $('.modal-difficulty').html("<span class='hard'>Hard</span>");
        $('.modal-difficulty').addClass('ps-4');
        $('.modal-difficulty').removeClass('ps-0');
    }


    document.body.appendChild(btn);
    $('#modalToggle').click();
}

function showQuestion(qid, title, difficulty, description, username, date_posted) {
    // Make AJAX query for the code
    $.ajax({
        url: '/answer_question/' + qid,
        timeout: 30000,
        error: function () {
            return false;
        },
        success: function (code) {
            showModal(qid, code, title, difficulty, description, username, date_posted)
        }
    })
}

