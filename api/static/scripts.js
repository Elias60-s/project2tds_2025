document.getElementById("questionForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const response = await fetch("/api/", {
        method: "POST",
        body: formData
    });

    const result = await response.json();  // Ensure JSON parsing

    // Update UI with JSON response
    document.getElementById("answerBox").innerHTML = `<strong>Answer:</strong> ${result.answer}`;
});
