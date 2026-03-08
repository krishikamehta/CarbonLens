import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Calculator from "./pages/Calculator";
import Simulator from "./pages/Simulator";
import Recommendations from "./pages/Recommendations";
import Footer from "./components/Footer";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/calculator" element={<Calculator />} />
        <Route path="/simulator" element={<Simulator />} />
        <Route path="/recommendations" element={<Recommendations />} />
      </Routes>

      <Footer />
    </BrowserRouter>
  );
}

export default App;