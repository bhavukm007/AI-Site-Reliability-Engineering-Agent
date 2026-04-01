async function analyze() {
    const logs = document.getElementById("logs").value;

    const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ logs: logs })
    });

    const data = await res.json();

    document.getElementById("output").innerText =
        "Errors:\n" + data.errors.join("\n") +
        "\n\nDecision: " + data.decision +
        "\nAction: " + data.action_result;
}