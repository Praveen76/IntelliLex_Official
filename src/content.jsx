import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import "./tailwind.css";
import { MainApp } from "./pages/MainApp/MainApp.jsx";

const root = document.createElement("div");
root.id = "intellilex-root";
root.style.position = "absolute";
root.style.zIndex = "2147483647";
document.body.appendChild(root);

createRoot(root).render(
  <StrictMode>
    <MainApp />
  </StrictMode>
);
