function extractHeadings(htmlText) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlText, 'text/html');
    const headings = [];

    for (let i = 1; i <= 6; i++) {
        const headingTags = doc.querySelectorAll(`h${i}`);
        headingTags.forEach(tag => {
            const id = tag.getAttribute('id');
            if (id) {
                headings.push(`<a href="#${id}">${tag.textContent}</a>`);
            }
        });
    }

    return headings.join('<br>');
}

// 测试
const htmlText = `
    <h1 id="heading1">Heading 1</h1>
    <h2 id="heading2">Heading 2</h2>
    <h3 id="heading3">Heading 3</h3>
    <h4 id="heading4">Heading 4</h4>
    <h5 id="heading5">Heading 5</h5>
    <h6 id="heading6">Heading 6</h6>
`;
const extractedHeadings = extractHeadings(htmlText);
console.log(extractedHeadings);
