import { useState } from "react";

function ClockCard() {
  const [currentDate, setCurrentDate] = useState(new Date());

  return (
    <>
      <button onClick={() => setCurrentDate(new Date())}>update time</button>
      <div>
        Current Time ={" "}
        {currentDate.getHours() +
          ":" +
          currentDate.getMinutes() +
          ":" +
          currentDate.getSeconds()}
      </div>
    </>
  );
}

export default ClockCard;
