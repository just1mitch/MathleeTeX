function deleteQuestion(questionId) {
    if (confirm("Are you sure you want to delete this question?")) {
        fetch(`/delete_question/${questionId}`, {
            method: 'POST'
        })
        .then(response => {
            if (response.ok) {
                //Might aswell use existing code to animate the deletion of the question
                document.getElementById(`question-${questionId}`).classList.add('content-animation');
                document.getElementById(`question-${questionId}`).remove();
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