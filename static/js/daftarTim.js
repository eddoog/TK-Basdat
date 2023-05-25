function showError(message) {
    $('#errorMessage').html('');
    const text = `<p class="text-danger fw-bold text-center">${message}</p>`;
    $(text).appendTo('#errorMessage');
}

$(document).ready(function () {
    $('[data-submit]').submit(function (e) {
        e.preventDefault();
        var namaTim = $('#namaTim').val();
        var namaUniversitas = $('#namaUniversitas').val();
        $.ajax({
            method: 'POST',
            url: '/manajer/daftar-tim/',
            data: {
                namaTim,
                namaUniversitas,
            },
            success: function (data) {
                window.location.href = `${window.location.protocol}//${window.location.host}/manajer/tim/`;
            },
            error: function (xhr) {
                var error = xhr.responseJSON.error;
                showError(error);
            },
        });
    });
});
