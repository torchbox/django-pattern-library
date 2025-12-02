import '../scss/main.scss';
import persistMenu from './components/persist-menu';
import patternSearch from './components/pattern-search';
import tabbedContent from './components/tabbed-content';
import syntaxHighlighting from './components/syntax-highlighting';
import hideMenuMobile from './components/hide-menu-mobile';
import { setIframeSize, resizeIframe } from './components/iframe';
import { toggleNav, toggleNavItems } from './components/navigation';

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
