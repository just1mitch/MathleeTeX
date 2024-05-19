function getQuestion(qid) {
    // Make AJAX query for the question details
    return new Promise((resolve, reject) => {
        $.ajax({
            type: "GET",
            url: '/answer_question/' + qid,
            timeout: 30000,
            error: function (jqXHR, _, errorThrown) {
                alert('Error (' + jqXHR.status + '): ' + errorThrown);
                reject(errorThrown);
            },
            success: function (response) {
                // If not signed in, send to login page
                if(typeof response === "string"){
                    window.location.href = $("a:contains('login')").attr('href');
                    reject();
                }
                else resolve(response);
            }
        });
    });
}