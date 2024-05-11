// Function to render all KaTeX in elements of the class 'render-katex'
// Iterates over the text of the element, finds any existence of a \
// which denotes the start of KaTeX code, and tries to render it
$('.render-katex').each(function() {
    const element = $(this);
    element.text().split("\\").forEach(function(string) {
        try {
            let html = katex.renderToString("\\" + string);
            element.html(element.text().replace("\\" + string, html)); 
        }
        catch (e) {
            if (e instanceof katex.ParseError) {
                return; // Skip this string if it cannot be rendered
            }
        }

    })
})

