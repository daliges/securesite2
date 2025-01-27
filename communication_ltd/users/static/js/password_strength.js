document.addEventListener("DOMContentLoaded", function () {
    // Fetch the config JSON file
    fetch('/static/config.json')  // הנתיב לתיקייה הסטטית
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
            const passwordInput = document.getElementById("password") || document.getElementById("new_password");;
            const feedbackContainer = document.getElementById("password-feedback");
            const strengthBar = document.getElementById("password-strength-bar");

            passwordInput.addEventListener("input", function () {
                const password = passwordInput.value;
                const feedback = validatePassword(password, policy);
                displayFeedback(feedback, feedbackContainer, strengthBar);
            });
        })
        .catch(error => console.error("Error loading config.json:", error));
});

// Function to validate the password based on policy
function validatePassword(password, policy) {
    const feedback = [];
    let score = 0;

    if (password.length < policy.min_length) {
        feedback.push(`Password must be at least ${policy.min_length} characters.`);
    } else {
        score += 1;
    }

    if (policy.require_uppercase && !/[A-Z]/.test(password)) {
        feedback.push("Password must include at least one uppercase letter.");
    } else {
        score += 1;
    }

    if (policy.require_lowercase && !/[a-z]/.test(password)) {
        feedback.push("Password must include at least one lowercase letter.");
    } else {
        score += 1;
    }

    if (policy.require_number && !/[0-9]/.test(password)) {
        feedback.push("Password must include at least one number.");
    } else {
        score += 1;
    }

    if (policy.require_special_character && !/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        feedback.push("Password must include at least one special character.");
    } else {
        score += 1;
    }

    return { feedback, score };
}

function updateBarColor(bar, score) {
    bar.value = score;
    if (score === 0) {
        bar.style.backgroundColor = "#808080"; // Gray (nothing)
    }else if (score === 1) {
            bar.style.backgroundColor = "#ff4d4d"; // Red (Very Weak)
    } else if (score === 2) {
        bar.style.backgroundColor = "#ffcc00"; // Yellow (Weak)
    } else if (score === 3) {
        bar.style.backgroundColor = "#ffcc00"; // Yellow (Fair)
    } else if (score === 4) {
        bar.style.backgroundColor = "#66cc00"; // Green (Good)
    } else {
        bar.style.backgroundColor = "#00b300"; // Dark Green (Strong)
    }
}


// Function to display feedback and update the strength bar
function displayFeedback(result, container, bar) {
    container.innerHTML = ""; // Clear previous feedback
    result.feedback.forEach(msg => {
        const li = document.createElement("li");
        li.textContent = msg;
        container.appendChild(li);
    });

    bar.value = result.score;

    updateBarColor(bar, result.score);
}



function togglePassword(inputId) {
    const passwordInput = document.getElementById(inputId);
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;
}