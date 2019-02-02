export function toggleNavItems() {
    const headings = document.querySelectorAll('.js-toggle-pattern');
    headings.forEach(heading => {
        heading.addEventListener('click', e => {
            e.target.classList.toggle('is-open');
            for ( const element of e.target.parentNode.childNodes ) {
                if ( element.nodeName === "UL" ){
                    element.classList.toggle('is-open');
                }
            }
        });
    });
}

export function toggleNav() {
    document.querySelector('.js-close-menu').addEventListener('click', (e) => {
        document.querySelector('body').classList.toggle('nav-closed');
    });
}
