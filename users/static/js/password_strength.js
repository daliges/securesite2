// Runs after DOM ready (script tag has defer)
const passwordInput = document.getElementById("password") || document.getElementById("new_password");
const feedbackContainer = document.getElementById("password-feedback");
const progressEl = document.getElementById("password-strength-bar");

if (passwordInput && progressEl) {
    // Replace <progress> with a plain div bar (avoids browser pseudo-element quirks)
    const barWrapper = document.createElement("div");
    barWrapper.style.cssText = "height:6px;border-radius:99px;background:#E5E7EB;overflow:hidden;margin-top:8px;";
    const barFill = document.createElement("div");
    barFill.style.cssText = "height:100%;width:0%;border-radius:99px;transition:width 220ms ease,background-color 220ms ease;";
    barWrapper.appendChild(barFill);
    progressEl.replaceWith(barWrapper);

    fetch("/api/password-policy/")
        .then(r => r.json())
        .then(policy => attachStrengthChecker(passwordInput, feedbackContainer, barFill, policy))
        .catch(() => attachStrengthChecker(passwordInput, feedbackContainer, barFill, {
            min_length: 10,
            require_uppercase: true,
            require_lowercase: true,
            require_number: true,
            require_special_character: true
        }));
}

function attachStrengthChecker(input, feedback, fill, policy) {
    input.addEventListener("input", function () {
        const result = validatePassword(input.value, policy);
        updateBar(fill, result.score);
        updateFeedback(feedback, result.feedback);
    });
}

function validatePassword(password, policy) {
    const feedback = [];
    let score = 0;

    if (password.length >= policy.min_length) { score++; }
    else { feedback.push("At least " + policy.min_length + " characters."); }

    if (!policy.require_uppercase || /[A-Z]/.test(password)) { score++; }
    else { feedback.push("At least one uppercase letter."); }

    if (!policy.require_lowercase || /[a-z]/.test(password)) { score++; }
    else { feedback.push("At least one lowercase letter."); }

    if (!policy.require_number || /[0-9]/.test(password)) { score++; }
    else { feedback.push("At least one number."); }

    if (!policy.require_special_character || /[!@#$%^&*(),.?":{}|<>]/.test(password)) { score++; }
    else { feedback.push("At least one special character (!@#$%^&*...)."); }

    return { feedback, score };
}

function updateBar(fill, score) {
    const colors = ["#E5E7EB", "#EF4444", "#F97316", "#EAB308", "#84CC16", "#16A34A"];
    fill.style.width = (score / 5 * 100) + "%";
    fill.style.backgroundColor = colors[score];
}

function updateFeedback(container, messages) {
    if (!container) return;
    container.innerHTML = "";
    messages.forEach(function(msg) {
        const li = document.createElement("li");
        li.textContent = msg;
        container.appendChild(li);
    });
}

function togglePassword(inputId) {
    const el = document.getElementById(inputId);
    if (el) el.type = el.type === "password" ? "text" : "password";
}
