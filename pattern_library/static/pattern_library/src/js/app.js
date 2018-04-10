import '../css/main.scss';
import hljs from 'highlight.js';

{
    function addSyntaxHighlighting() {
        hljs.initHighlightingOnLoad();
    }

    function toggleNavItems() {
        const headings = document.querySelectorAll('.js-toggle-pattern');
        headings.forEach(heading => {
            heading.addEventListener('click', e => {
                event.target.classList.toggle('is-open');
                event.target.nextElementSibling.classList.toggle('is-open');
            });
        });
    }

    function resizeIframe() {
        const body = document.querySelector('body');
        const patternIframe = document.querySelector('.js-iframe');
        const resizeButtons = document.querySelectorAll('.js-resize-iframe');
        const closeButton = document.querySelector('.js-close-iframe');

        patternIframe.contentWindow.addEventListener('resize', function(e){
            document.querySelector('.js-iframe-size').innerHTML = `${e.target.innerWidth} x ${e.target.innerHeight}`
        });

        // Pop-out iframe
        document.querySelector('.js-resize-iframe-full').addEventListener('click', () => {
            body.classList.add('iframe-open');
            patternIframe.style.removeProperty('width');
        });

        // Close iframe with escape key
        document.addEventListener('keydown', e => {
            e = e || window.event;
            if (e.key === 'Escape') {
                body.classList.remove('iframe-open');
            }
        });

        // Close iframe via icon
        closeButton.addEventListener('click', e => {
            body.classList.remove('iframe-open');
        })

        // Resize iframe via buttons
        resizeButtons.forEach(button => {
            button.addEventListener('click', e => {
                resizeButtons.forEach(button => button.classList.remove('is-active'));
                e.target.classList.add('is-active');
                patternIframe.style.width =
                    e.target.dataset.resize == 100 ? `${e.target.dataset.resize}%` : `${e.target.dataset.resize}px`;
            });
        });
    }

    function setIframeSize(){
        const iframe = document.querySelector('.js-iframe').contentWindow;
        document.querySelector('.js-iframe-size').innerHTML = `${iframe.innerWidth} x ${iframe.innerHeight}`
    }

    function toggleNav() {
        document.querySelector('.js-close-menu').addEventListener('click', function(e){
            document.querySelector('body').classList.toggle('nav-open');
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        addSyntaxHighlighting();
        toggleNavItems();
        resizeIframe();
        setIframeSize();
        toggleNav();
    });
}
