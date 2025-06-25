// Get references to HTML elements
const targetDateInput = document.getElementById("targetDate");
const eventNameInput = document.getElementById("eventName");
const addCountdownButton = document.getElementById("addCountdown");
const countdownsTable = document.getElementById("countdowns");

// Event listener for adding a countdown
addCountdownButton.addEventListener("click", () => {
    const targetDate = new Date(targetDateInput.value);
    const eventName = eventNameInput.value;

    console.log("eventName:", eventName);
    console.log("targetDate:", targetDate);

    if (!eventName || isNaN(targetDate)) {
        alert("Please enter a valid date and event name.");
        return;
    }

    // Create a new row for the countdown
    const row = countdownsTable.insertRow();
    row.classList.add("countdown-row");

    // Name of the event
    const nameCell = row.insertCell(0);
    nameCell.textContent = eventName;

    // Timer format (0 h 00 m 00s)
    const timerCell = row.insertCell(1);
    const timerText = document.createElement("div");
    timerText.classList.add("timer-text");
    timerCell.appendChild(timerText);

    // Progress bar
    const progressCell = row.insertCell(2);
    const progressBar = document.createElement("div");
    progressBar.classList.add("progress-bar");
    progressCell.appendChild(progressBar);

    // Action buttons (Pause, Resume, Clear)
    const actionsCell = row.insertCell(3);

    const pauseButton = document.createElement("button");
    pauseButton.textContent = "Pause";
    pauseButton.classList.add("action-button");
    pauseButton.classList.add("pause-button");
    pauseButton.style.backgroundColor = "blue";
    pauseButton.style.color = "white";
    actionsCell.appendChild(pauseButton);

    const resumeButton = document.createElement("button");
    resumeButton.textContent = "Resume";
    resumeButton.classList.add("action-button");
    resumeButton.classList.add("resume-button");
    resumeButton.style.backgroundColor = "blue";
    resumeButton.style.color = "white";
    actionsCell.appendChild(resumeButton);

    const clearButton = document.createElement("button");
    clearButton.textContent = "Clear";
    clearButton.classList.add("action-button");
    clearButton.classList.add("clear-button");
    clearButton.style.backgroundColor = "blue";
    clearButton.style.color = "white";
    actionsCell.appendChild(clearButton);

    // Clear input fields
    eventNameInput.value = "";
    targetDateInput.value = "";

    // Start the countdown timer
    startCountdown(targetDate, timerText, progressBar, pauseButton, resumeButton, clearButton);
});

// Function to start the countdown timer
function startCountdown(targetDate, timerText, progressBar, pauseButton, resumeButton, clearButton, row) {
    let timerInterval;
    const initialTime = targetDate - new Date();
    let remainingTime = initialTime;

    function updateTimer() {
        if (remainingTime <= 0) {
            timerText.textContent = "Expired";
            progressBar.style.width = "100%";
            clearInterval(timerInterval);
            pauseButton.disabled = true;
            resumeButton.disabled = true;

            // Show an alert message when the countdown ends
            alert("Countdown has ended!");
        } else {
            const hours = Math.floor(remainingTime / (1000 * 60 * 60));
            const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);

            timerText.textContent = `${hours} h ${minutes} m ${seconds} s`;

            const elapsedTime = initialTime - remainingTime;
            const progressPercentage = (elapsedTime / initialTime) * 100;
            progressBar.style.width = progressPercentage + "%";

            remainingTime -= 1000; // Decrease remaining time by 1 second
        }
    }

    // Update the timer every second
    updateTimer();
    timerInterval = setInterval(updateTimer, 1000);

    // Pause button click event
    pauseButton.addEventListener("click", () => {
        clearInterval(timerInterval);
        pauseButton.disabled = true;
        resumeButton.disabled = false;
    });

    // Resume button click event
    resumeButton.addEventListener("click", () => {
        timerInterval = setInterval(updateTimer, 1000);
        pauseButton.disabled = false;
        resumeButton.disabled = true;
    });

    // Clear button click event
    clearButton.addEventListener("click", () => {
        clearInterval(timerInterval);
        const row = clearButton.closest("tr"); // Find the closest table row (countdown row)
        row.parentNode.removeChild(row); // Remove the row
    });
}