$(document).ready(function() {
    renderKaTeX();
  });
  
  function renderKaTeX() {
    // Use jQuery to find all elements with the class 'katex-render'
    $('.katex-render').each(function() {
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