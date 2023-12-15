export function toggleNavItems() {
    const categoryButtons = document.querySelectorAll('.js-toggle-pattern');

    categoryButtons.forEach((button) => {
        button.addEventListener('click', (e) => {
            e.target.classList.toggle('is-open');
            for (const element of e.target.closest('.js-list-item').childNodes) {
                if (element.nodeName === 'UL') {
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
