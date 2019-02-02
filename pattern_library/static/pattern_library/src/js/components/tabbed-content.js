export default function() {
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
