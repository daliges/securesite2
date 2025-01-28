document.addEventListener("DOMContentLoaded", function () {
    // Fetch the config JSON file
    fetch('/static/config.json')  // Path to the static directory
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to load config.json: ${response.status}`);
            }
            return response.json();
        })
        .then(config => {
            const policy = config.password_policy;
            console.log("Password policy loaded:", policy);

            // Add event listener to check password strength
            const passwordInput = document.getElementById("password") || document.getElementById("new_password");
            const feedbackContainer = document.getElementById("password-feedback");
            const strengthBar = document.getElementById("password-strength-bar");

            if (passwordInput) {
                passwordInput.addEventListener("input", function () {
                    const password = passwordInput.value;
                    const feedback = validatePassword(password, policy);
                    displayFeedback(feedback, feedbackContainer, strengthBar);
                });
            } else {
                console.error("Password input field not found.");
            }
        })
        .catch(error => console.error("Error loading config.json:", error));
});

// Function to validate the password based on policy
function validatePassword(password, policy) {
    const feedback = [];
    let score = 0;

    // Check password length
    if (password.length < policy.min_length) {
        feedback.push(`Password must be at least ${policy.min_length} characters.`);
    } else {
        score++;
    }

    // Check for uppercase letters
    if (policy.require_uppercase && !/[A-Z]/.test(password)) {
        feedback.push("Password must include at least one uppercase letter.");
    } else {
        score++;
    }

    // Check for lowercase letters
    if (policy.require_lowercase && !/[a-z]/.test(password)) {
        feedback.push("Password must include at least one lowercase letter.");
    } else {
        score++;
    }

    // Check for numbers
    if (policy.require_number && !/[0-9]/.test(password)) {
        feedback.push("Password must include at least one number.");
    } else {
        score++;
    }

    // Check for special characters
    if (policy.require_special_character && !/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        feedback.push("Password must include at least one special character.");
    } else {
        score++;
    }

    return { feedback, score };
}

// Function to update the color of the progress bar based on score
function updateBarColor(bar, score) {
    let color;

    switch (score) {
        case 1:
            color = "#c7340c"; // Very Weak (Dark Red)
            break;
        case 2:
            color = "#ce7a0c"; // Weak (Orange)
            break;
        case 3:
            color = "#e2e619"; // Fair (Yellow)
            break;
        case 4:
            color = "#49d508"; // Good (Light Green)
            break;
        case 5:
            color = "green"; // Strong (Green)
            break;
        default:
            color = "#c7340c"; // Default (Weakest Red)
            break;
    }

    // Apply the color to the progress bar
    bar.style.backgroundColor = color;
}

// Function to display feedback and update the strength bar
function displayFeedback(result, container, bar) {
    // Clear previous feedback
    container.innerHTML = "";

    // Add feedback messages
    result.feedback.forEach(msg => {
        const li = document.createElement("li");
        li.textContent = msg;
        container.appendChild(li);
    });

    // Update progress bar value and color
    bar.value = result.score;
    updateBarColor(bar, result.score);
}

// Function to toggle password visibility
function togglePassword(inputId) {
    const passwordInput = document.getElementById(inputId);
    if (passwordInput) {
        passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
    } else {
        console.error(`Input field with ID "${inputId}" not found.`);
    }
}
