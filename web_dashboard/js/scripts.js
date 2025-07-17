function showChartsBasedOnTime() {
    const now = new Date();
    const hours = now.getHours();
    // console.log("Current Hour:", hours);

    // Task 2: Show only between 1 PM to 2 PM
    if (hours === 13) {
        document.getElementById("task2").style.display = "block";
    }

    // Task 3: Show only between 5 PM to 7 PM
    if (hours >= 17 && hours < 19) {
        document.getElementById("task3").style.display = "block";
    }
}

// Call this function when the page loads
window.onload = showChartsBasedOnTime;
