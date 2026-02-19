const searchBox = document.querySelector(".search input");
const searchBtn = document.querySelector(".search button");
const weatherIcon = document.querySelector(".weather-icon");

async function checkWeather(city) {

    if (!city) return;

    try {
        // Call Flask backend instead of OpenWeather directly
        const response = await fetch(`/weather?city=${city}`);
        const data = await response.json();

        if (!response.ok) {
            document.querySelector(".error").style.display = "block";
            document.querySelector(".weather").style.display = "none";
            document.querySelector(".card-button").style.display = "none";
            return;
        }

        document.querySelector(".city").innerHTML = data.city;
        document.querySelector(".temp").innerHTML = Math.round(data.temp) + "°C";
        document.querySelector(".humidity").innerHTML = data.humidity + "%";
        document.querySelector(".wind").innerHTML = data.wind + " km/h";

        // Use OpenWeather dynamic icon
        weatherIcon.src =
            `https://openweathermap.org/img/wn/${data.icon}@2x.png`;

        document.querySelector(".weather").style.display = "block";
        document.querySelector(".card-button").style.display = "block";
        document.querySelector(".error").style.display = "none";

    } catch (error) {
        console.log("Error:", error);
        document.querySelector(".error").style.display = "block";
        document.querySelector(".weather").style.display = "none";
    }
}

searchBtn.addEventListener("click", () => {
    checkWeather(searchBox.value.trim());
});

// Allow Enter key search
searchBox.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        checkWeather(searchBox.value.trim());
    }
});
