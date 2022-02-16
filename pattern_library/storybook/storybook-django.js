/**
 * Inserts HTML into an element, executing embedded script tags.
 * @param {Element} element
 * @param {string} html
 */
 export const insertHTMLWithScripts = (element, html) => {
    element.innerHTML = html;

    Array.from(element.querySelectorAll('script')).forEach((script) => {
        const newScript = document.createElement('script');
        Array.from(script.attributes).forEach((attr) =>
            newScript.setAttribute(attr.name, attr.value),
        );

        newScript.appendChild(document.createTextNode(script.innerHTML));
        script.parentNode.replaceChild(newScript, script);
    });
};

/**
 * Inserts HTML into an element, executing embedded script tags,
 * firing a DOMContentLoaded event.
 * @param {Element} element
 * @param {string} html
 */
export const simulateLoading = (element, html) => {
    if (!element) {
        return;
    }

    insertHTMLWithScripts(element, html);

    window.document.dispatchEvent(
        new Event('DOMContentLoaded', {
            bubbles: true,
            cancelable: true,
        }),
    );
};

export const renderPattern = (endpoint) => {
    return window.fetch(endpoint, {
        method: 'GET',
        mode: 'same-origin',
        cache: 'no-cache',
        credentials: 'omit',
    });
};
