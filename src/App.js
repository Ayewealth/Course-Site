import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import "./App.css";
import PrivateRoutes from "./utils/PrivateRoute";
import Home from "./pages/Home";
import About from "./pages/About";
import Course from "./pages/Course";
import Blog from "./pages/Blog";
import Cart from "./pages/Cart";
import Login from "./pages/Login";
import Choice from "./pages/Choice";
import Instructor from "./pages/Registration/Instructor";
import Student from "./pages/Registration/Student";
import { createContext, useState } from "react";
import { AuthProvider } from "./context/AuthContext";

export const ThemeContext = createContext(null);
function App() {
  const [theme, setTheme] = useState("light");
  const toggleTheme = () => {
    setTheme((curr) => (curr === "light" ? "dark-theme" : "light"));
  };

  return (
    <div className={theme}>
      <Router>
        <AuthProvider>
          <ThemeContext.Provider value={{ theme, toggleTheme }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path="/courses" element={<Course />} />
              <Route path="/blog" element={<Blog />} />
              <Route path="/cart" element={<Cart />} />
              <Route path="/login" element={<Login />} />
              <Route path="/choice" element={<Choice />} />
              <Route path="/instructor" element={<Instructor />} />
              <Route path="/student" element={<Student />} />
              <Route element={<PrivateRoutes />}>
                <Route />
              </Route>
            </Routes>
          </ThemeContext.Provider>
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;
