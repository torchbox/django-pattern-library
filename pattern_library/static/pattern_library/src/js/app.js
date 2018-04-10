import '../css/main.scss';
import hljs from 'highlight.js';

{
    function highlightSyntax() {
        hljs.initHighlightingOnLoad();
    }

    function togglePatterns() {
        const headings = document.querySelectorAll('.js-toggle-pattern');
        headings.forEach(heading => {
            heading.addEventListener('click', e => {
                event.target.classList.toggle('is-open');
                event.target.nextElementSibling.classList.toggle('is-open');
            });
        });
    }

    function toggleIframe() {
        const buttons = document.querySelectorAll('.js-resize-iframe');
        buttons.forEach(button => {
            button.addEventListener('click', e => {
                buttons.forEach(button => button.classList.remove('is-active'));
                e.target.classList.add('is-active');
                document.querySelector('.js-iframe').style.width =
                    e.target.dataset.resize == 100
                        ? `${e.target.dataset.resize}%`
                        : `${e.target.dataset.resize}px`;
            });
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        highlightSyntax();
        togglePatterns();
        toggleIframe();
    });
}
