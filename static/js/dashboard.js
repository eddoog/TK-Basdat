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

function showError(message) {
    $('#errorMessage').html('');
    const text = `<p class="text-danger font-bold text-center">${message}</p>`;
    $(text).appendTo('#errorMessage');
}

$(document).ready(function () {
    $('#logoutButton').click(function (e) {
        console.log('logouting');
        e.preventDefault();
        $.ajax({
            method: 'POST',
            url: '/dashboard/logout/',
            success: function (data) {
                window.location.href = `${window.location.protocol}//${window.location.host}`;
            },
            error: function (error) {
                showError('Cannot logout');
            },
        });
    });
});
