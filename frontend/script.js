const form = document.querySelector('#registration-form');
const statusBox = document.querySelector('#form-status');
const submitButton = form.querySelector('button[type="submit"]');
const apiBaseUrl = (window.APP_CONFIG?.API_BASE_URL || '').replace(/\/$/, '');

const fields = ['full_name', 'email', 'age', 'password'];

function setStatus(message, type) {
    statusBox.textContent = message;
    statusBox.className = `status is-visible is-${type}`;
}

function clearStatus() {
    statusBox.textContent = '';
    statusBox.className = 'status';
}

function clearErrors() {
    fields.forEach((field) => {
        document.querySelector(`[data-error-for="${field}"]`).textContent = '';
    });
}

function showErrors(errors) {
    Object.entries(errors).forEach(([field, messages]) => {
        const errorTarget = document.querySelector(`[data-error-for="${field}"]`);

        if (errorTarget) {
            errorTarget.textContent = messages.join(' ');
        }
    });
}

function getPayload() {
    const data = new FormData(form);

    return {
        full_name: data.get('full_name').trim(),
        email: data.get('email').trim(),
        age: Number(data.get('age')),
        password: data.get('password'),
    };
}

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearStatus();
    clearErrors();
    submitButton.disabled = true;
    submitButton.textContent = 'Submitting...';

    try {
        const response = await fetch(`${apiBaseUrl}/api/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(getPayload()),
        });
        const result = await response.json();

        if (!response.ok) {
            showErrors(result.errors || {});
            setStatus('Please check the highlighted fields.', 'error');
            return;
        }

        form.reset();
        setStatus(result.message || 'Registration submitted successfully.', 'success');
    } catch (error) {
        setStatus('Could not connect to the registration server.', 'error');
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Submit Registration';
    }
});
