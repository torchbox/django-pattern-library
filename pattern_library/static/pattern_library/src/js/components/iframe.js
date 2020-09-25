export function resizeIframe() {
    const body = document.querySelector('body');
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

export function setIframeSize() {
    const iframe = document.querySelector('.js-iframe').contentWindow;
    document.querySelector('.js-iframe-size').innerHTML = `${iframe.innerWidth} x ${iframe.innerHeight}`
}
