import hljs from 'highlight.js/lib/core';

export default function() {
    hljs.initHighlightingOnLoad();
    ['django', 'yaml'].forEach((langName) => {
        const langModule = require(`highlight.js/lib/languages/${langName}`);
        hljs.registerLanguage(langName, langModule);
    });
}
