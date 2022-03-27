import hljs from 'highlight.js/lib/core';
import django from 'highlight.js/lib/languages/django';
import yaml from 'highlight.js/lib/languages/yaml';

export default function() {
    hljs.registerLanguage('django', django);
    hljs.registerLanguage('yaml', yaml);
    hljs.highlightAll();
}
