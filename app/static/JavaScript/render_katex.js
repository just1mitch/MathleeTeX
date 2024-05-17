// Function to render all KaTeX in elements of the class 'render-katex'
// Iterates over the text of the element, finds any existence of a \
// which denotes the start of KaTeX code, and tries to render it


$(document).ready(function () {
    renderKaTeX();
});

function renderKaTeX() {

    $('.render-katex').each(function () {
        const element = $(this);
        element.text().split("\\").forEach(function (string) {
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
    });

    // Use jQuery to find all elements with the class 'katex-render'
    $('.katex-render').each(function () {
        const text = $(this).text();
        try {
            katex.render(text, this, {
                throwOnError: false  // This option will render the original text if there's a parsing error
            });
        } catch (e) {
            console.error("KaTeX render error:", e);
        }
    });
}