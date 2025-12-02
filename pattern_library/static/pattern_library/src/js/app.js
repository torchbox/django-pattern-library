import '../scss/main.scss';
import persistMenu from './components/persist-menu.js';
import patternSearch from './components/pattern-search.js';
import tabbedContent from './components/tabbed-content.js';
import syntaxHighlighting from './components/syntax-highlighting.js';
import hideMenuMobile from './components/hide-menu-mobile.js';
import { setIframeSize, resizeIframe } from './components/iframe.js';
import { toggleNav, toggleNavItems } from './components/navigation.js';

document.addEventListener('DOMContentLoaded', () => {
    syntaxHighlighting();
    toggleNavItems();
    resizeIframe();
    setIframeSize();
    toggleNav();
    tabbedContent();
    persistMenu();
    patternSearch();
    hideMenuMobile();
});
