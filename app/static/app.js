const form = document.getElementById("predict-form");
const button = form.querySelector("button");
const result = document.getElementById("result");
const numericFields = ["make_year", "engine_cc", "owner_count", "accidents_reported", "mileage_kmpl"];

document.getElementById("make_year").max = new Date().getFullYear();

function showResult(label, value, isError) {
    result.className = isError ? "readout show error" : "readout show";
    result.innerHTML = "";
    const labelEl = document.createElement("span");
    labelEl.className = "readout-label";
    labelEl.textContent = label;
    const valueEl = document.createElement("span");
    valueEl.className = "readout-value";
    valueEl.textContent = value;
    result.append(labelEl, valueEl);
}

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(form));
    for (const field of numericFields) {
        data[field] = Number(data[field]);
    }

    button.disabled = true;
    button.textContent = "Predicting…";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            let message = "Request failed. Please check your inputs and try again.";
            try {
                const error = await response.json();
                if (Array.isArray(error.detail) && error.detail.length > 0) {
                    const first = error.detail[0];
                    const field = first.loc[first.loc.length - 1];
                    message = `${field}: ${first.msg}`;
                }
            } catch (_) {}
            showResult("Error", message, true);
            return;
        }

        const prediction = await response.json();
        const price = Number(prediction.predicted_price).toLocaleString("en-US", {maximumFractionDigits: 0});
        showResult("Estimated price", `$ ${price}`, false);
    } catch (_) {
        showResult("Error", "Could not reach the server. Please try again.", true);
    } finally {
        button.disabled = false;
        button.textContent = "Predict price";
    }
});
