$(document).ready(function () {
    $('.logout-button').click(function (e) {
        e.preventDefault();
        $.ajax({
            method: 'POST',
            url: '/logout/',
            success: function (data) {
                window.location.href = `${window.location.protocol}//${window.location.host}`;
            },
            error: function (error) {
                showError('Cannot logout');
            },
        });
    });
});
