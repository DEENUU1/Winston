document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(event) {
        if (event.target && event.target.classList.contains('copy-button')) {
            const textToCopy = event.target.getAttribute('data-result');
            const textArea = document.createElement('textarea');

            textArea.value = textToCopy;
            document.body.appendChild(textArea);

            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        }
    });
});