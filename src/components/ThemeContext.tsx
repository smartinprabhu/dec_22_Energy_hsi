// ThemeContext.tsx
import React, { createContext, useContext, useState, ReactNode } from "react";

// Define the shape of the context
interface ThemeContextType {
  themes: "dark" | "light"; // Restrict theme to 'dark' or 'light'
  toggleTheme: () => void; // Function to toggle the theme
}

// Create the context with a default value of null
const ThemeContext = createContext<ThemeContextType | null>(null);

// Create a provider component
export const ThemeProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [themes, setTheme] = useState<"dark" | "light">("dark"); // Start with dark theme by default

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === "dark" ? "light" : "dark"));
  };

  return (
    <ThemeContext.Provider value={{ themes, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

// Custom hook to use the ThemeContext
export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};
