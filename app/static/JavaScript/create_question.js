// Validate Title and Description Inputs of create question form
function validateInput() {
    const title = $("#title").val().trim();
    const description = $("#description").val().trim();
    const code = $("#code").val().trim();
    let valid = true;

    // Check if Title and Description lengths are valid
    if(title.length > 50) {
        $('#titleError').html("Error: Title length must be less than 50 characters (currently " + title.length + ")")
        $('#titleError').parent().show();
        valid = false;
    }
    else $('#titleError').parent().hide();
    if(description.length > 250) {
        $('#descriptionError').html("Error: Description length must be less than 250 characters (currently " + description.length + ")")
        $('#descriptionError').parent().show();
        valid = false;
    }
    else $('#descriptionError').parent().hide()
    if(code.length > 50) {
        $('#codeError').html("Error: Code length must be less than 50 characters (currently " + code.length + ")")
        $('#codeError').parent().show();
        valid = false;
    }
    else $('#codeError').parent().hide()

    // Disable submit button if inputs are invalid
    if(valid) $('#questionSubmit').prop('disabled', false);
    else $('#questionSubmit').prop('disabled', true);
};

$(document).ready(validateInput);
$('#title').on('input', validateInput);
$('#description').on('input', validateInput);

$('#code').on('input', function() {
    $('#katexdyna').prop('hidden', false);
    try {
        katex.render($(this).val(), document.getElementById('katexdyna'), {throwOnError: false})
        // Also render to string - if there are errors, will catch and display underneath the rendered text
        katex.renderToString($(this).val())
        if($(this).val().length === 0) $('#katexdyna').prop('hidden', true);
        $('#questionSubmit').prop('disabled', false);
        $('#katexErrorCode').prop('hidden', true);
        validateInput();

    }
    catch (e) {
        if (e instanceof katex.ParseError) {
            $('#katexErrorCode').html(e.message);
            $('#katexErrorCode').prop('hidden', false);
            // Prevent submitting form if katex is invalid
            $('#questionSubmit').prop('disabled', true);
        }
    }
})