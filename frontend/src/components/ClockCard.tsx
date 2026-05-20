import { useEffect, useState } from "react";

function ClockCard() {
  const [currentDate, setCurrentDate] = useState(new Date());

  useEffect(() => {
    setInterval(() => {
      setCurrentDate(new Date());
    }, 1000);
  }, []);

  return (
    <>
      <div>Current Time ={currentDate.toLocaleTimeString()}</div>
    </>
  );
}

export default ClockCard;
