export default function() {
    const searchBox = document.getElementById('js-pattern-search-input');
    const patternList = [...document.querySelectorAll('.list__item-link')];
    const patternListContainer = document.getElementById('sidebar-nav');
    const searchResultsContainer = document.getElementById('js-pattern-search-results-container')

    searchBox.addEventListener('keyup', e => {
        let searchValue = e.target.value.toLowerCase();

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
                return item.textContent.toLowerCase().includes(searchValue);
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
