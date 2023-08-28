import React, { useContext } from "react";
import { ThemeContext } from "../App";

const ThemeToggle = () => {
  const { theme, toggleTheme } = useContext(ThemeContext);
  const iconTheme = theme === "dark-theme" ? "uil-sun" : "uil-moon";

  return (
    <i className={`uil ${iconTheme} change-theme`} onClick={toggleTheme}></i>
  );
};

export default ThemeToggle;
