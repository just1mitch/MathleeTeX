$('#code').on('keyup', function() {
    try {
        katex.render($(this).val(), document.getElementById('katexdyna'), {throwOnError: false})
        // Also render to string - if there are errors, will catch and display underneath the rendered text
        katex.renderToString($(this).val())
        $('#katexErrorCode').css('display', 'none');
    }
    catch (e) {
        if (e instanceof katex.ParseError) {
            $('#katexErrorCode').html(e.message);
            $('#katexErrorCode').css('display', 'block');
        }
    }
})

// $('#submit-question').submit(function() {
//     var $errorContainer = $(this).find(".error-section");
//     $errorContainer.empty();
//     const difficultyId = $("input[name='difficulty']:checked").attr('id');
//     let difficulty = $("label[for='" + difficultyId + "']").text();
//     const title = $("#title").val().trim();
//     const description = $("#description").val().trim();
//     const code = $("#code").val().trim();
//     let leng = title.length
//     if(title.length > 50 | description.length > 250 | code.length > 250) {
//         return false;
//     }
//     return true;
// });