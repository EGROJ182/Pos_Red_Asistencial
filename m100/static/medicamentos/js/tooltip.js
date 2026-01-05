document.addEventListener('DOMContentLoaded', function () {
    tippy('.tooltip', {
        content(reference) {
            return reference.getAttribute('data-title');
        },
        placement: 'top',
        theme: 'light',
    });
});