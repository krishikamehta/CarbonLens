import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-green-800 text-white p-4 flex justify-between">
      <h1 className="font-bold text-lg">CarbonLens</h1>

      <div className="space-x-6">
        <Link to="/">Home</Link>
        <Link to="/calculator">Calculator</Link>
        <Link to="/simulator">Simulator</Link>
        <Link to="/recommendations">Recommendations</Link>
      </div>
    </nav>
  );
}