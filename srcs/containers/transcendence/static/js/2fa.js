console.log("2fa_script loaded...");

if (document.getElementById('otp-form')) {

    if (document.getElementById('error-message'))
        errorDiv = document.getElementById('error-message')
    document.getElementById('otp-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting normally
        isFormSubmitted = true;
        form = document.getElementById('otp-form');
        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                to_unspecified_page(data.redirect_url);
            } else {
                if (errorDiv) {
                    errorDiv.innerHTML = `<p>${data.error}</p>`; // Display error message
                }
            }
        })
        .catch(error => console.error('Error:', error));
    })
}
