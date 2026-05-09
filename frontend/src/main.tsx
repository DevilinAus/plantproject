import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import ClockCard from "./components/ClockCard.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ClockCard />

    <App />
  </StrictMode>,
);
