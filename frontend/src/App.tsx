import { useEffect, useState } from "react";
import ClockCard from "./components/ClockCard.tsx";
import "./App.css";
import WeatherCard from "./components/WeatherCard.tsx";

type Weather = {
  temp: number;
  humidity: number;
  condition: string;
};
type WeatherLoaded = { type: "loaded"; weather: Weather }; // new this
type WeatherError = { type: "error"; error: Error };
type WeatherLoading = { type: "loading" };

type WeatherStatus = WeatherLoaded | WeatherError | WeatherLoading;

function App() {
  const [weatherStatus, setWeatherStatus] = useState<WeatherStatus>({
    type: "loading",
  });

  useEffect(() => {
    async function getWeather() {
      try {
        const weatherReq = await fetch("http://localhost:3001/");
        const weatherObj = await weatherReq.json();
        setWeatherStatus({ type: "loaded", weather: weatherObj });
      } catch (e) {
        setWeatherStatus({ type: "error", error: e as Error });
      }
    }

    getWeather();
  }, []);

  if (weatherStatus.type === "loading") {
    return <>Loading</>;
  }

  if (weatherStatus.type === "error") {
    return <>{weatherStatus.error.message}</>;
  }

  const weather = weatherStatus.weather;

  return (
    <>
      <ClockCard />
      <WeatherCard
        temp={weather.temp}
        humidity={weather.humidity}
        condition={weather.condition}
      />
    </>
  );
}

export default App;
