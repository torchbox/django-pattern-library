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
        const patternIframe = document.querySelector('.js-iframe');
        const resizeButtons = document.querySelectorAll('.js-resize-iframe');

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

    function patternSearch() {
        const searchBox = document.getElementById('js-pattern-search-input');
        const patternList = [...document.querySelectorAll('.list__item-link')];
        const patternListContainer = document.getElementById('sidebar-nav');
        const searchResultsContainer = document.getElementById('js-pattern-search-results-container')

        searchBox.addEventListener('keyup', e => {
            let searchValue = e.target.value;

            // Clear if input value is empty
            if (searchValue === '') {
                searchResultsContainer.innerHTML = '';
                patternListContainer.classList.remove('sidebar__nav--inactive');
            }

            // On enter key
            if (e.keyCode == 13 && searchValue != '') {

                // Clear results list and hide pattern list
                searchResultsContainer.innerHTML = '';
                patternListContainer.classList.add('sidebar__nav--inactive');

                // Match search query
                let matchedValues = patternList.filter(function (item) {
                    return item.textContent.includes(searchValue);
                });

                // Populate search results
                if (matchedValues.length) {
                    matchedValues.forEach(item => {
                        searchResultsContainer.innerHTML += '<a href="' + item.getAttribute("href") +'">' + item.textContent + '</a>';
                    });
                } else {
                    searchResultsContainer.innerHTML = 'No results found.';
                }
            }
        });
    }

    function persistMenu() {
        // split url to match {{ template.origin.template_name }}
        const id = location.pathname.split('/pattern/')[1];

        // find the matching pattern
        const currentPattern = document.getElementById(id);

        // grab the parent lists and headings
        const parentCategory = currentPattern.closest('ul');
        const parentCategoryHeading = parentCategory.previousElementSibling;
        const grandParentCategory = parentCategoryHeading.closest('ul');
        const grandParentCategoryHeading = grandParentCategory.previousElementSibling;

        parentCategory.classList.add('is-open');
        parentCategoryHeading.classList.add('is-open');
        grandParentCategory.classList.add('is-open');
        grandParentCategoryHeading.classList.add('is-open');
    }

    function hideMenuOnMobile() {
        // hide the sidebar if coming from a mobile device
        if (window.matchMedia('(max-width: 600px)').matches) {
            document.querySelector('body').classList.add('nav-closed')
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        addSyntaxHighlighting();
        toggleNavItems();
        resizeIframe();
        setIframeSize();
        toggleNav();
        tabbedContent();
        patternSearch();
        persistMenu();
        hideMenuOnMobile();
    });
}
