// General AJAX function
function ajaxRequest(url, method, data, callback) {
    const spinner = document.getElementById('spinner'); // Ensure spinner is in the DOM
    spinner.classList.remove('hidden'); // Show the spinner

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for POST requests
        },
        body: method === 'POST' ? JSON.stringify(data) : null, // Only include body for POST requests
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Parse JSON response
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        callback(data); // Call the provided callback with the data
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    })
    .finally(() => {
        spinner.classList.add('hidden'); // Hide the spinner
    });
}

// Utility function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
