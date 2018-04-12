import '../scss/main.scss';
import hljs from 'highlight.js/lib/highlight';

{
    // return an array from a given selector
    function arrayMaker(selector) {
        return Array.prototype.slice.call(document.querySelectorAll(selector));
    }

    // languages for syntax highlighting
    function addSyntaxHighlighting() {
        hljs.initHighlightingOnLoad();
        ['django', 'yaml'].forEach((langName) => {
            const langModule = require(`highlight.js/lib/languages/${langName}`);
            hljs.registerLanguage(langName, langModule);
        });
    }

    // show/hide menu items
    function toggleNavItems() {
        const headings = arrayMaker('.js-toggle-pattern');
        headings.forEach(heading => {
            heading.addEventListener('click', e => {
                e.target.classList.toggle('is-open');
                e.target.nextElementSibling.classList.toggle('is-open');
            });
        });
    }

    //  handles resizing the pattern window iframe
    function handleIframe() {
        const body = document.querySelector('body');
        const resizeButtons = arrayMaker('.js-resize-iframe');
        const patternIframe = document.querySelector('.js-iframe');
        const closeButton = document.querySelector('.js-close-iframe');

        // remove animating class to prevent delay when dragging iframe
        patternIframe.addEventListener('mousedown', function(){
            this.classList.remove('is-animatable');
        });

        patternIframe.addEventListener('mouseup', function(){
            this.classList.add('is-animatable');
        });

        // update iframe dimensions text
        patternIframe.contentWindow.addEventListener('resize', e => {
            document.querySelector('.js-iframe-size').innerHTML = `${e.target.innerWidth} x ${e.target.innerHeight}`
        });

        // pop-out iframe
        document.querySelector('.js-resize-iframe-full').addEventListener('click', () => {
            patternIframe.style.removeProperty('width');
            body.classList.add('iframe-open');
        });

        // close iframe with escape key
        document.addEventListener('keydown', e => {
            e = e || window.event;
            if (e.key === 'Escape') {
                body.classList.remove('iframe-open');
            }
        });

        // close iframe via icon
        closeButton.addEventListener('click', () => body.classList.remove('iframe-open'));

        // resize iframe via buttons
        resizeButtons.forEach(button => {
            button.addEventListener('click', e => {
                // remove active state from all buttons
                resizeButtons.forEach(button => button.classList.remove('is-active'));

                // add active state to target
                e.target.classList.add('is-active');

                // fullscreen value is a percentage, everything else is px
                patternIframe.style.width =
                    e.target.dataset.resize == 100 ? `${e.target.dataset.resize}%` : `${e.target.dataset.resize}px`;
            });
        });
    }

    // update the dimensions of the iframe on page load
    function setIframeDimensionsText() {
        const iframe = document.querySelector('.js-iframe').contentWindow;
        document.querySelector('.js-iframe-size').innerHTML = `${iframe.innerWidth} x ${iframe.innerHeight}`
    }

    // show/hide the nav
    function toggleNav() {
        document.querySelector('.js-close-menu').addEventListener('click', () => {
            document.querySelector('body').classList.toggle('nav-closed');
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        toggleNav();
        handleIframe();
        toggleNavItems();
        addSyntaxHighlighting();
        setIframeDimensionsText();
    });
}
