$('.render-katex').each(function() {
    const element = $(this);
    element.text().split("\\").forEach(function(string) {
        debugger;
        console.log("\\" + string)
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

