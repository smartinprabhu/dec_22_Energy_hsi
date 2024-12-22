import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import { ThemeProvider } from "./components/ThemeContext"; // Adjust the path to match your project structure
import "./index.scss";
import * as serviceWorker from './serviceWorker';

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <ThemeProvider> {/* Provide the ThemeContext here */}
      <App />
    </ThemeProvider>
  </React.StrictMode>
);

serviceWorker.register();
