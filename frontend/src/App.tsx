import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "./assets/vite.svg";
import heroImg from "./assets/hero.png";
import ClockCard from "./components/ClockCard.tsx";
import "./App.css";
import WeatherCard from "./components/WeatherCard.tsx";

function App() {
  const [weather, setWeather] = useState(null);

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
