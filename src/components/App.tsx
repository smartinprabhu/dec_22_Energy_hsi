import React from "react";
import { ThemeProvider } from "./ThemeContext";
import MainPage from "../pages/MainPage/MainPage";

function App() {
  return (
    <ThemeProvider>
      <MainPage />
    </ThemeProvider>
  );
}

export default App;
