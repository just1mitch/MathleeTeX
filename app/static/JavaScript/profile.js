function deleteQuestion(questionId) {
    if (confirm("Are you sure you want to delete this question?")) {
        fetch(`/delete_question/${questionId}`, {
            method: 'POST'
        })
        .then(response => {
            if (response.ok) {
                //Might aswell use existing code to animate the deletion of the question
                document.getElementById(`question-${questionId}`).classList.add('content-animation');
                setTimeout(() => { document.getElementById(`question-${questionId}`).remove(); }, 500);
                console.log('Question deleted successfully.');
            } else {
                console.error('Failed to delete question.');
            }
        })
        .catch(error => {
            console.error('An error occurred:', error);
        });
    }
}

function showPreview(qid, title, description, date_posted, difficulty) {
    getQuestion(qid).then(response => {
        // Create Modal button
        let btn = document.createElement("button");
        btn.setAttribute("type", "button");
        btn.setAttribute("id", "modalToggle");
        btn.setAttribute("class", "btn")
        btn.style.display = "none";
        btn.setAttribute("data-bs-toggle", "modal");
        btn.setAttribute("data-bs-target", "#answerModal");

        // render question - should never fail if server validation worked
        try {
            katex.render(response.code, document.getElementsByClassName('modal-code')[0], { throwOnError: false });
        } catch (e) {
            console.error("KaTeX render error:", e);
        }
        $('.modal-title').html(title);
        $('.modal-description').html(description);
        $('#byline').html("Posted " + date_posted);

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
        // Click invisible button to trigger Bootstrap Modal
        document.body.appendChild(btn);
        $('#modalToggle').click();

        // Load Comments
        getComments($('#submit-answer').attr('qid')).then(comments => {
            $('#commentSection').prop('hidden', false);
            $('#commentSection').html(comments);
            $('.dateposted').each(timeSince);
        }).catch();
    }).catch();
    return;
}