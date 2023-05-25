function showError(message) {
    $('#errorMessage').html('');
    const text = `<p class="text-danger fw-bold text-center">${message}</p>`;
    $(text).appendTo('#errorMessage');
}

$(document).ready(function () {
    $('[data-captain-submit]').submit(function (e) {
        e.preventDefault();
        $('[data-captain-submit]').submit(function (e) {
            e.preventDefault();
            var playerId = $(this).find('button').val();

            $.ajax({
                method: 'POST',
                url: '/manajer/change-captain/',
                data: {
                    playerId,
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

        $('[data-remove-player-submit]').click(function () {
            var playerId = $(this).val();

            $.ajax({
                method: 'POST',
                url: '/manajer/remove-player/',
                data: {
                    playerId,
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
});
