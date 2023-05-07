function show() {
    var why = document.getElementById('work');
    if (why.style.display === 'flex') {
        why.style.display = 'none';
    } else {
        why.style.display = 'flex';
    }
}

window.addEventListener('resize', function () {
    var why = document.getElementById('work');
    var width = window.innerWidth;
    if (width > 900 && why.style.display === 'none') {
        why.style.display = 'flex';
    }

    if (width <= 900 && why.style.display === 'flex') {
        why.style.display = 'none';
    }
});
