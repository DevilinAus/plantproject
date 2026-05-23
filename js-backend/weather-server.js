// small node server to serve up the weather from the database for the react app.

import express from "express";

const app = express();
const PORT = 3001;

app.listen(PORT, () => {
  console.log(`Weather server running on http://localhost:${PORT}`);
});
