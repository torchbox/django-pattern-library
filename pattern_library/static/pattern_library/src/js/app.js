import '../scss/main.scss';
import hljs from 'highlight.js/lib/highlight';

{
    function addSyntaxHighlighting() {
        hljs.initHighlightingOnLoad();
        ['django', 'yaml'].forEach((langName) => {
            const langModule = require(`highlight.js/lib/languages/${langName}`);
            hljs.registerLanguage(langName, langModule);
        });
    }

    function toggleNavItems() {
        const headings = document.querySelectorAll('.js-toggle-pattern');
        headings.forEach(heading => {
            heading.addEventListener('click', e => {
                e.target.classList.toggle('is-open');
                e.target.nextElementSibling.classList.toggle('is-open');
            });
        });
    }

    function resizeIframe() {
        const body = document.querySelector('body');
        const patternIframe = document.querySelector('.js-iframe');
        const resizeButtons = document.querySelectorAll('.js-resize-iframe');
        const closeButton = document.querySelector('.js-close-iframe');

        // remove animating class to prevent delay when dragging iframe
        patternIframe.addEventListener('mousedown', function(){
            this.classList.remove('is-animatable');
        });

        patternIframe.addEventListener('mouseup', function(){
            this.classList.add('is-animatable');
        });

        patternIframe.contentWindow.addEventListener('resize', (e) => {
            document.querySelector('.js-iframe-size').innerHTML = `${e.target.innerWidth} x ${e.target.innerHeight}`
        });

        // Close iframe with escape key
        document.addEventListener('keydown', e => {
            e = e || window.event;
            if (e.key === 'Escape') {
                body.classList.remove('iframe-open');
            }
        });

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

    function setIframeSize() {
        const iframe = document.querySelector('.js-iframe').contentWindow;
        document.querySelector('.js-iframe-size').innerHTML = `${iframe.innerWidth} x ${iframe.innerHeight}`
    }

    function toggleNav() {
        document.querySelector('.js-close-menu').addEventListener('click', (e) => {
            document.querySelector('body').classList.toggle('nav-closed');
        });
    }

    function tabbedContent() {
        let i;
        let tabItem = document.querySelectorAll('.tabbed-content__heading');

        function tabs(tabClickEvent) {
            for (let i = 0; i < tabItem.length; i++) {
                tabItem[i].classList.remove('tabbed-content__heading--active');
            }

            let clickedTab = tabClickEvent.currentTarget;

            clickedTab.classList.add('tabbed-content__heading--active');
            tabClickEvent.preventDefault();

            let contentPanes = document.querySelectorAll('.tabbed-content__item');

            for (i = 0; i < contentPanes.length; i++) {
                contentPanes[i].classList.remove('tabbed-content__item--active');
            }

            let anchorReference = tabClickEvent.target;
            let activePaneId = anchorReference.getAttribute('href');
            let activePane = document.querySelector(activePaneId);

            activePane.classList.add('tabbed-content__item--active');
        }

        for (i = 0; i < tabItem.length; i++) {
            tabItem[i].addEventListener('click', tabs)
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        addSyntaxHighlighting();
        toggleNavItems();
        resizeIframe();
        setIframeSize();
        toggleNav();
        tabbedContent();
    });
}
