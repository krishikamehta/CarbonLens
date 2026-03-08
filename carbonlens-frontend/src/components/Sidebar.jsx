import { Link } from "react-router-dom";

export default function Sidebar(){

  return(
    <div className="w-64 bg-green-800 text-white min-h-screen p-6">

      <h1 className="text-xl font-bold mb-8">
        CarbonLens
      </h1>

      <div className="space-y-4">

        <Link to="/dashboard">Dashboard</Link>
        <Link to="/calculator">Calculator</Link>
        <Link to="/simulator">Simulator</Link>
        <Link to="/recommendations">Recommendations</Link>

      </div>

    </div>
  );
}