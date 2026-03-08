import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Calculator from "./pages/Calculator";
import History from "./pages/History";
import Recommendations from "./pages/Recommendations";
import Simulator from "./pages/Simulator";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import ProtectedRoute from "./components/ProtectedRoute";

import { AuthProvider } from "./context/AuthContext";

function App() {
  return (
    <AuthProvider>

      <BrowserRouter>

        <Navbar />

        <Routes>

          {/* Landing page */}
          <Route path="/" element={<Home />} />

          {/* Auth */}
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          {/* Protected routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/calculator"
            element={
              <ProtectedRoute>
                <Calculator />
              </ProtectedRoute>
            }
          />

          <Route
            path="/history"
            element={
              <ProtectedRoute>
                <History />
              </ProtectedRoute>
            }
          />

          <Route
            path="/recommendations"
            element={
              <ProtectedRoute>
                <Recommendations />
              </ProtectedRoute>
            }
          />

          <Route
            path="/simulator"
            element={
              <ProtectedRoute>
                <Simulator />
              </ProtectedRoute>
            }
          />

        </Routes>

        <Footer />

      </BrowserRouter>

    </AuthProvider>
  );
}

export default App;