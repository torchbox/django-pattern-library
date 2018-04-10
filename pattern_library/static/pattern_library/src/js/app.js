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
        const patternIframe = document.querySelector('.js-iframe');
        const resizeButtons = document.querySelectorAll('.js-resize-iframe');
        const closeIframe = document.querySelector('.js-close-iframe');

        // Pop-out iframe
        document.querySelector('.js-resize-iframe-full').addEventListener('click', () => {
            patternIframe.style.removeProperty('width');
            patternIframe.classList.add('is-fullscreen');
        });

        // Close iframe with escape key
        document.addEventListener('keydown', e => {
            e = e || window.event;
            if (e.key === 'Escape') {
                document.querySelector('.js-iframe').classList.remove('is-fullscreen');
            }
        });

        closeIframe.addEventListener('click', e => {
            patternIframe.classList.remove('is-fullscreen');
        })

        // Resize iframe
        resizeButtons.forEach(button => {
            button.addEventListener('click', e => {
                resizeButtons.forEach(button => button.classList.remove('is-active'));
                e.target.classList.add('is-active');
                patternIframe.style.width =
                    e.target.dataset.resize == 100 ? `${e.target.dataset.resize}%` : `${e.target.dataset.resize}px`;
            });
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        highlightSyntax();
        togglePatterns();
        toggleIframe();
    });
}
