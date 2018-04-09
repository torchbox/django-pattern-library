import '../css/main.scss';
import hljs from 'highlight.js';

{
    document.addEventListener('DOMContentLoaded', () => hljs.initHighlightingOnLoad());

        function highlightSyntax(){
            hljs.initHighlightingOnLoad();
        }

        function togglePatterns(){
            const headings = document.querySelectorAll('.js-toggle-pattern');

            headings.forEach(function(heading){
                heading.addEventListener('click', function(e){
                    event.target.classList.toggle('is-open');
                    event.target.nextElementSibling.classList.toggle('is-open');
                })
            })
        }

    document.addEventListener('DOMContentLoaded', () => {
        highlightSyntax();
        togglePatterns();
    });
}
