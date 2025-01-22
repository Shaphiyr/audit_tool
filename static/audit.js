// Dark Mode Toggle
const darkModeToggle = document.getElementById('dark-mode-toggle');
const body = document.body;

// Check and apply stored dark mode preference
if (localStorage.getItem('darkMode') === 'enabled') {
    body.classList.add('dark-mode');
}

darkModeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
        darkModeToggle.textContent = '☀️ Light Mode';
    } else {
        localStorage.setItem('darkMode', 'disabled');
        darkModeToggle.textContent = '🌙 Dark Mode';
    }
});

// Survey Navigation
let currentQuestion = 0;
const questions = document.querySelectorAll('.question');
const progressBar = document.querySelector('.progress');
const prevButton = document.getElementById('prev-button');
const nextButton = document.getElementById('next-button');

function showQuestion(index) {
    questions.forEach((question, i) => {
        question.style.display = i === index ? 'block' : 'none';
    });
    progressBar.style.width = ((index + 1) / questions.length) * 100 + '%';
    prevButton.disabled = index === 0;
    nextButton.textContent = index === questions.length - 1 ? 'Submit' : 'Next ➡️';
}

// Initialize first question
showQuestion(currentQuestion);

nextButton.addEventListener('click', () => {
    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        showQuestion(currentQuestion);
    } else {
        document.querySelector('form').submit();
    }
});

prevButton.addEventListener('click', () => {
    if (currentQuestion > 0) {
        currentQuestion--;
        showQuestion(currentQuestion);
    }
});

// "Other" Option Logic
document.querySelectorAll('select').forEach((select) => {
    select.addEventListener('change', (event) => {
        const otherInput = select.nextElementSibling;
        if (event.target.value === 'Other') {
            otherInput.style.display = 'block';
        } else {
            otherInput.style.display = 'none';
        }
    });
});
