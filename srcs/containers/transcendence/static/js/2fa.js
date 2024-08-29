console.log("2fa_script loaded");

if (document.getElementById('login')) {
    document.getElementById('login').addEventListener('click', () => {
        const url = `account/login/`;
        console.log("Navigating to:", url);
        to_unspecified_page_2fa(url);
    });
}

if (document.getElementById('two_factor')) {
    document.getElementById('two_factor').addEventListener('click', () => {
        loadTwoFactorSetup();
    });
}

async function loadTwoFactorSetup() {
    try {
        const response = await fetch('/account/two_factor/setup/');
        if (!response.ok) throw new Error('Network response was not ok');

        const html = await response.text();
        
        const contentDiv = document.getElementById('content');
        if (contentDiv) {
            contentDiv.innerHTML = html;
            // After replacing HTML, you might need to initialize or bind JavaScript functions to the new content
            initializeTwoFactorSetup();
        }
    } catch (error) {
        console.error('Error loading Two-Factor Setup:', error);
    }
}

function initializeTwoFactorSetup() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(form);
            console.log("2fa.js l95", formData);
            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    }
                });
                if (!response.ok) throw new Error('Network response was not ok');
                
                // Handle successful response
                const data = await response.json();
                console.log('Form submitted successfully:', data);
                // Update the page or notify the user
            } catch (error) {
                console.error('Error submitting form:', error);
            }
        });
    }
}

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

async function to_unspecified_page_2fa(page) {
    try {
        // navigate_to_load('/');

        let div_content = document.getElementById('content');
        await fetching_html_2fa(page, div_content);

        page = change_page_name(page);
        reset_script('/' + page);

        if (page !== 'game/') {
            if (game_socket && game_socket.readyState === WebSocket.OPEN) {
                game_socket.close();
            }
        }

        reload_scripts('/' + page, 0);
        navigate(page);
    } catch (error) {
        console.error('Error during navigation:', error);
    }
}

async function fetching_html_2fa(page, div_content) {
    try {
        const response = await fetch(page);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const html = await response.text();
        div_content.innerHTML = html;
    } catch (error) {
        console.error('Error fetching page:', error);
        div_content.innerHTML = '<p>Error loading content.</p>';
    }
}