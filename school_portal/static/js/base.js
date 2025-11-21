
document.querySelectorAll('.navbar .dropdown').forEach((drop) => {
    let timeout;
    const menu = drop.querySelector('.dropdown-menu');

    drop.addEventListener('mouseenter', () => {
        clearTimeout(timeout);
        menu.classList.add('show', 'animate-dropdown');
    });

    drop.addEventListener('mouseleave', () => {
        timeout = setTimeout(() => {
            menu.classList.remove('show', 'animate-dropdown');
        }, 300);
    });
});