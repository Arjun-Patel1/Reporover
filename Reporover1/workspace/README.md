# Super Weather App
It is an Weather Dashboard with attractive UI/UX, languages used are html, css, and js
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #1a1a2e;
            --secondary: #16213e;
            --accent: #0f3460;
            --background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }

        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            margin: 0;
            min-height: 100vh;
            background: var(--background);
            color: #e6e6e6;
            line-height: 1.6;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        header {
            padding: 2rem 1rem;
            background: rgba(0, 0, 0, 0.3);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(8px);
            border-radius: 20px;
            margin-bottom: 2rem;
        }

        .weather-container {
            max-width: 800px;
            width: 90%;
            padding: 2rem;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .input-box {
            width: 100%;
            padding: 1rem;
            border: none;
            border-radius: 15px;
            background: rgba(0, 0, 0, 0.3);
            color: white;
            font-size: 1.1rem;
            transition: all 0.3s ease;
        }

        .input-box:focus {
            outline: none;
            background: rgba(0, 0, 0, 0.4);
            box-shadow: 0 0 0 2px var(--accent);
        }

        .btn {
            background: linear-gradient(45deg, var(--accent), #1a1a2e);
            border: none;
            padding: 0.8rem 1.5rem;
            margin: 0.5rem;
            border-radius: 15px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(15, 52, 96, 0.4);
        }

        .weather-summary {
            background: rgba(0, 0, 0, 0.3);
            padding: 2rem;
            border-radius: 25px;
            margin: 1rem 0;
            text-align: center;
            backdrop-filter: blur(5px);
        }

        .weather-icon {
            font-size: 4rem;
            margin: 1rem 0;
            color: #4fc3f7;
            filter: drop-shadow(0 2px 4px rgba(79, 195, 247, 0.3));
        }

        .weather-icon .fa-sun,
        .weather-icon .fa-cloud-sun {
            color: #FFD700;
        }

        .weather-icon .fa-cloud-rain,
        .weather-icon .fa-cloud-showers-heavy {
            color: #4fc3f7;
        }

        #temperature {
            font-size: 4rem;
            font-weight: 300;
            margin: 1rem 0;
            background: linear-gradient(45deg, #4fc3f7, #e6e6e6);
            -webkit-text-fill-color: transparent;
            -webkit-background-clip: text;
            background-clip: text;
            cursor: pointer;
            transition: transform 0.3s ease;
        }

        #temperature:hover {
            transform: scale(1.05);
        }

        .loading {
            display: none;
            text-align: center;
            padding: 2rem;
        }

        .loading-spinner {
            display: inline-block;
            width: 50px;
            height: 50px;
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #4fc3f7;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .hourly-forecast {
            display: flex;
            overflow-x: auto;
            padding: 1rem 0;
            gap: 1rem;
            scrollbar-width: thin;
            scrollbar-color: var(--accent) transparent;
        }

        .hourly-item {
            flex: 0 0 120px;
            padding: 1.5rem;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 20px;
            text-align: center;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
            position: relative;
            overflow: hidden;
        }

        .hourly-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s ease;
        }

        .hourly-item:hover::before {
            left: 100%;
        }

        .hourly-item:hover {
            transform: translateY(-5px);
            background: rgba(0, 0, 0, 0.4);
        }

        .hourly-item .time {
            font-size: 1rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }

        .hourly-item .temp {
            font-size: 1.5rem;
            font-weight: 600;
            margin: 0.5rem 0;
        }

        .hourly-item .icon {
            font-size: 2rem;
            margin: 0.5rem 0;
        }

        .weather-metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }

        .metric-item {
            background: rgba(0, 0, 0, 0.3);
            padding: 1.5rem;
            border-radius: 20px;
            text-align: center;
            backdrop-filter: blur(5px);
            transition: transform 0.3s ease;
        }

        .metric-item:hover {
            transform: translateY(-5px);
        }

        .metric-item i {
            font-size: 2rem;
            color: #4fc3f7;
            margin-bottom: 0.5rem;
        }

        .alert-box {
            background: rgba(255, 50, 50, 0.3);
            border-left: 4px solid #ff3265;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 15px;
            animation: slideIn 0.3s ease;
            display: none;
        }

        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    </style>
</head>
<body>
    <header>
        <h1 style="text-align: center; margin: 0;">Weather Dashboard</h1>
    </header>
    <main>
        <div class="weather-container">
            <div style="display: flex; gap: 0.5rem; margin-bottom: 2rem;">
                <input type="text" id="cityInput" placeholder="Enter city name" class="input-box">
                <button id="getWeatherBtn" class="btn"><i class="fas fa-search"></i> Search</button>
                <button id="geoLocationBtn" class="btn"><i class="fas fa-location-crosshairs"></i> Locate</button>
            </div>

            <div class="loading" id="loading">
                <div class="loading-spinner"></div>
                <div style="margin-top: 1rem;">Fetching weather data...</div>
            </div>

            <div class="weather-summary">
                <h2 id="locationName" style="margin: 0 0 1rem 0; font-weight: 500;"></h2>
                <div id="currentWeather">
                    <div id="weatherIcon" class="weather-icon"></div>
                    <div id="temperature"></div>
                    <div id="weatherDescription" style="font-size: 1.2rem;"></div>
                </div>
            </div>

            <div class="weather-metrics">
                <div class="metric-item">
                    <i class="fas fa-wind"></i>
                    <div>Wind</div>
                    <span id="windSpeed"></span>
                </div>
                <div class="metric-item">
                    <i class="fas fa-droplet"></i>
                    <div>Humidity</div>
                    <span id="humidity"></span>
                </div>
                <div class="metric-item">
                    <i class="fas fa-sun"></i>
                    <div>UV Index</div>
                    <span id="uvIndex"></span>
                </div>
                <div class="metric-item">
                    <i class="fas fa-cloud-rain"></i>
                    <div>Precipitation</div>
                    <span id="precipitation"></span>
                </div>
            </div>

            <div class="hourly-forecast" id="hourlyList"></div>

            <div id="alerts" class="alert-box"></div>
        </div>
    </main>

    <script>
        document.addEventListener("DOMContentLoaded", function () {
            const getWeatherBtn = document.getElementById("getWeatherBtn");
            const cityInput = document.getElementById("cityInput");
            const geoLocationBtn = document.getElementById("geoLocationBtn");
            const loading = document.getElementById("loading");
            const temperature = document.getElementById("temperature");
            let isCelsius = true;

            async function fetchCoordinates(city) {
                try {
                    const response = await fetch(
                        `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(city)}&count=1`
                    );
                    const data = await response.json();
                    
                    if (!data.results || data.results.length === 0) {
                        throw new Error('No city found');
                    }
                    
                    return {
                        name: data.results[0].name,
                        country: data.results[0].country,
                        latitude: data.results[0].latitude,
                        longitude: data.results[0].longitude
                    };
                } catch (error) {
                    showError(error.message);
                    return null;
                }
            }

            async function fetchWeather(lat, lon) {
                try {
                    loading.style.display = 'block';
                    const unit = isCelsius ? 'celsius' : 'fahrenheit';
                    const response = await fetch(
                        `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&hourly=temperature_2m,weathercode&current=temperature_2m,weathercode,windspeed_10m,relativehumidity_2m,uv_index,precipitation&temperature_unit=${unit}&windspeed_unit=ms&timezone=auto`
                    );
                    const data = await response.json();
                    
                    if (!data.current) {
                        throw new Error('Weather data not available');
                    }
                    
                    updateDisplay(data);
                    updateHourlyForecast(data.hourly);
                } catch (error) {
                    showError(error.message);
                } finally {
                    loading.style.display = 'none';
                }
            }

            function updateDisplay(data) {
                const current = data.current;
                temperature.textContent = `${current.temperature_2m}°${isCelsius ? 'C' : 'F'}`;
                document.getElementById('weatherDescription').textContent = getWeatherDescription(current.weathercode);
                document.getElementById('windSpeed').textContent = `${current.windspeed_10m} m/s`;
                document.getElementById('humidity').textContent = `${current.relativehumidity_2m}%`;
                document.getElementById('uvIndex').textContent = current.uv_index;
                document.getElementById('precipitation').textContent = `${current.precipitation}mm`;
                document.getElementById('weatherIcon').innerHTML = getWeatherIcon(current.weathercode);
            }

            function updateHourlyForecast(hourly) {
                const hourlyList = document.getElementById('hourlyList');
                hourlyList.innerHTML = '';
                
                for (let i = 0; i < 24; i++) {
                    const div = document.createElement('div');
                    div.className = 'hourly-item';
                    div.innerHTML = `
                        <div class="time">${new Date(hourly.time[i]).getHours()}:00</div>
                        <div class="temp">${hourly.temperature_2m[i]}°</div>
                        <div class="icon">${getWeatherIcon(hourly.weathercode[i])}</div>
                    `;
                    hourlyList.appendChild(div);
                }
            }

            function getWeatherDescription(code) {
                const weatherCodes = {
                    0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy',
                    3: 'Overcast', 45: 'Fog', 48: 'Fog',
                    51: 'Light drizzle', 53: 'Moderate drizzle', 55: 'Dense drizzle',
                    56: 'Freezing drizzle', 57: 'Dense freezing drizzle',
                    61: 'Slight rain', 63: 'Moderate rain', 65: 'Heavy rain',
                    66: 'Freezing rain', 67: 'Heavy freezing rain',
                    71: 'Slight snow', 73: 'Moderate snow', 75: 'Heavy snow',
                    77: 'Snow grains', 80: 'Slight showers', 81: 'Moderate showers',
                    82: 'Violent showers', 85: 'Snow showers', 86: 'Heavy snow showers',
                    95: 'Thunderstorm', 96: 'Thunderstorm with hail',
                    99: 'Heavy thunderstorm with hail'
                };
                return weatherCodes[code] || 'Unknown weather';
            }

            function getWeatherIcon(code) {
                const icons = {
                    0: 'fa-sun', 1: 'fa-cloud-sun', 2: 'fa-cloud-sun',
                    3: 'fa-cloud', 45: 'fa-smog', 48: 'fa-smog',
                    51: 'fa-cloud-rain', 53: 'fa-cloud-rain', 55: 'fa-cloud-showers-heavy',
                    56: 'fa-cloud-meatball', 57: 'fa-cloud-meatball',
                    61: 'fa-cloud-rain', 63: 'fa-cloud-showers-heavy', 65: 'fa-cloud-showers-water',
                    66: 'fa-icicles', 67: 'fa-icicles',
                    71: 'fa-snowflake', 73: 'fa-snowflake', 75: 'fa-snowflake',
                    77: 'fa-snowflake', 80: 'fa-cloud-showers-heavy', 81: 'fa-cloud-showers-heavy',
                    82: 'fa-cloud-showers-water', 85: 'fa-snowflake', 86: 'fa-snowflake',
                    95: 'fa-bolt', 96: 'fa-bolt-lightning', 99: 'fa-bolt-lightning'
                };
                return `<i class="fas ${icons[code] || 'fa-question'}"></i>`;
            }

            function showError(message) {
                const alerts = document.getElementById('alerts');
                alerts.style.display = 'block';
                alerts.textContent = message;
                setTimeout(() => alerts.style.display = 'none', 3000);
            }

            temperature.addEventListener('click', () => {
                isCelsius = !isCelsius;
                const location = document.getElementById('locationName').textContent;
                if (location) {
                    if (location === 'Your Location') {
                        navigator.geolocation.getCurrentPosition(async position => {
                            await fetchWeather(position.coords.latitude, position.coords.longitude);
                        });
                    } else {
                        const currentCity = cityInput.value.trim();
                        if (currentCity) {
                            fetchCoordinates(currentCity).then(location => {
                                if (location) {
                                    fetchWeather(location.latitude, location.longitude);
                                }
                            });
                        }
                    }
                }
            });

            getWeatherBtn.addEventListener('click', async () => {
                try {
                    if (!cityInput.value.trim()) {
                        throw new Error('Please enter a city name');
                    }
                    
                    const location = await fetchCoordinates(cityInput.value.trim());
                    if (location) {
                        document.getElementById('locationName').textContent = `${location.name}, ${location.country}`;
                        await fetchWeather(location.latitude, location.longitude);
                    }
                } catch (error) {
                    showError(error.message);
                }
            });

            geoLocationBtn.addEventListener('click', () => {
                if (!navigator.geolocation) return showError('Geolocation not supported');
                navigator.geolocation.getCurrentPosition(async position => {
                    document.getElementById('locationName').textContent = 'Your Location';
                    await fetchWeather(position.coords.latitude, position.coords.longitude);
                }, () => showError('Unable to get your location'));
            });
        });
    </script>
</body>
</html>
