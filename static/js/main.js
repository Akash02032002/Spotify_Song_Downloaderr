$(document).ready(function () {
    $('#download-form').on('submit', function (e) {
        e.preventDefault();

        const url = $('#url').val();
        $('#status').html('<p>Downloading...</p>');

        $.ajax({
            url: '/download',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ url: url }),
            success: function (response) {
                if (response.status === 'success') {
                    const downloadLink = `<a href="/download-file/${response.file_path}" class="btn btn-success mt-3">Download Song</a>`;
                    $('#status').html('<p>Download complete!</p>' + downloadLink);
                } else {
                    $('#status').html('<p>Error: ' + response.message + '</p>');
                }
            },
            error: function () {
                $('#status').html('<p>Download failed. Please try again.</p>');
            }
        });
    });
});
