const toggleBtn = document.getElementById('toggle-theme');
const savedTheme = localStorage.getItem('theme') || 'light';
if (savedTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    toggleBtn.innerText = '☀️';
}

toggleBtn.onclick = () => {
    const theme =
        document.documentElement.getAttribute('data-theme') === 'dark'
            ? 'light'
            : 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    toggleBtn.innerText = theme === 'dark' ? '☀️' : '🌙';
};

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
