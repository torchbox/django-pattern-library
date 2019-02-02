export default function() {
    // hide the sidebar if coming from a mobile device
    if (window.matchMedia('(max-width: 600px)').matches) {
        document.querySelector('body').classList.add('nav-closed')
    }
}
