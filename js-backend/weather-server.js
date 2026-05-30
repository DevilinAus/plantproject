// small node server to serve up the weather from the database for the react app.

import express from "express";

import cors from "cors";

const app = express();
const PORT = 3001;

app.use(
  cors({
    origin: "http://localhost:5173",
  }),
);

app.get("/", (req, res) => {
  res.json({
    temp: 21,
    humidity: 78,
    condition: "cloudy",
  });
});

app.listen(PORT, () => {
  console.log(`Weather server running on http://localhost:${PORT}`);
});
