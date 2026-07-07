const form = document.getElementById("predict-form");

form.addEventListener("submit" , async function (e) {
    e.preventDefault();


const data = {
    make_year : Number(document.getElementById("make_year").value),
    engine_cc : Number(document.getElementById("engine_cc").value),
    owner_count : Number(document.getElementById("owner_count").value),
    accidents_reported : Number(document.getElementById("accidents_reported").value),
    mileage_kmpl : Number(document.getElementById("mileage_kmpl").value),
    fuel_type : document.getElementById("fuel_type").value ,
    brand : document.getElementById("brand").value ,
    transmission : document.getElementById("transmission").value ,
    color : document.getElementById("color").value ,
    service_history : document.getElementById("service_history").value ,
    insurance_valid : document.getElementById("insurance_valid").value
}

const response = await fetch("/predict", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
});

if (!response.ok) {
    let message = "Ошибка запроса";
    try {
        const error = await response.json();
        if (Array.isArray(error.detail) && error.detail.length > 0) {
            const first = error.detail[0];
            const field = first.loc[first.loc.length - 1];
            message = `${field}: ${first.msg}`;
        }
    } catch (_) { /* тело не JSON — оставляем общее сообщение */ }
    document.getElementById("result").textContent = message;
    return ;
}

const result = await response.json()
document.getElementById("result").textContent = result.predicted_price.toFixed(2) + " $";
})
