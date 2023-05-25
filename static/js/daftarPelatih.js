function showError(message) {
    $('#errorMessage').html('');
    const text = `<p class="text-danger fw-bold text-center">${message}</p>`;
    $(text).appendTo('#errorMessage');
}

$(document).ready(function () {
    $('[data-submit]').submit(function (e) {
        e.preventDefault();
        var coachId = $('#coach-select').val();
        console.log(coachId)
        $.ajax({
            method: 'POST',
            url: '/manajer/tim/daftar-pelatih/',
            data: {
                coachId
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
