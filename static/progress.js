// Questions Data
const questions = [
    "How often do you reach out to past clients?",
    "How frequently do you review your CRM analytics?",
    "How personalized are your client follow-ups?",
    "Do you use automation tools for client engagement?",
    "How often do you update your client database?",
    "Do you track referral opportunities actively?",
    "How consistent are your marketing efforts?",
    "Do you segment your clients for tailored communication?",
    "How frequently do you follow up with prospects?",
    "Do you use client feedback to refine your processes?",
];

// DOM Elements
const questionContainer = document.getElementById('questions');
const nextBtn = document.getElementById('nextBtn');
let currentQuestion = 0;

// Functions
function loadQuestion(index) {
    questionContainer.innerHTML = `
        <label for="q${index}">${questions[index]}</label><br>
        <select name="q${index}" id="q${index}">
            <option value="" disabled selected>Choose an option</option>
            <option value="Always">Always</option>
            <option value="Often">Often</option>
            <option value="Sometimes">Sometimes</option>
            <option value="Rarely">Rarely</option>
            <option value="Never">Never</option>
        </select>
    `;
    nextBtn.disabled = true; // Disable button until answer is selected
}

function updateProgress() {
    const progress = ((currentQuestion + 1) / questions.length) * 100;
    document.querySelector('.progress').style.width = progress + '%';
}

// Event Listeners
document.addEventListener('change', (event) => {
    if (event.target.tagName === 'SELECT') {
        nextBtn.disabled = false;
    }
});

nextBtn.addEventListener('click', () => {
    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        loadQuestion(currentQuestion);
        updateProgress();
    } else {
        alert("You've completed the audit! 🎉");
        document.querySelector('form').submit();
    }
});

// Initialize
loadQuestion(currentQuestion);
updateProgress();
