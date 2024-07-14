$(document).ready(function () {
    $('#download-form').on('submit', function (e) {
        e.preventDefault();

        const url = $('#url').val();
        $('#status').html('<p>Downloading...</p>');
        $('#progress-bar').css('width', '0%').text('0%').parent().show();
        $('#progress-text').text('0%').show();

        $.ajax({
            url: '/download',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ url: url }),
            xhr: function() {
                const xhr = new window.XMLHttpRequest();
                xhr.onprogress = function(event) {
                    if (event.lengthComputable) {
                        const percentComplete = (event.loaded / event.total) * 100;
                        $('#progress-bar').css('width', percentComplete + '%').text(Math.round(percentComplete) + '%');
                        $('#progress-text').text(Math.round(percentComplete) + '%');
                    }
                };
                return xhr;
            },
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
