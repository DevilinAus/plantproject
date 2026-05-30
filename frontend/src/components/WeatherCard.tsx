type WeatherCardProps = { temp: number; humidity: number; condition: string };

function WeatherCard({ temp, humidity, condition }: WeatherCardProps) {
  return (
    <section>
      <h2>Current Weather</h2>
      <p>Temp: {temp}</p>
      <p>humidity: {humidity}</p>
      <p>condition: {condition}</p>
    </section>
  );
}

export default WeatherCard;
