import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {

  const { user, logout } = useAuth();

  return (
    <nav className="bg-green-800 text-white p-4 flex justify-between">

      <h1 className="font-bold text-lg">CarbonLens</h1>

      <div className="space-x-6 flex items-center">

        <Link to="/">Home</Link>

        {user && (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/calculator">Calculator</Link>
            <Link to="/simulator">Simulator</Link>
            <Link to="/recommendations">Recommendations</Link>
          </>
        )}

        {!user && (
          <>
            <Link to="/login">Login</Link>
            <Link
              to="/signup"
              className="bg-white text-green-800 px-3 py-1 rounded"
            >
              Signup
            </Link>
          </>
        )}

        {user && (
          <button
            onClick={logout}
            className="bg-white text-green-800 px-3 py-1 rounded"
          >
            Logout
          </button>
        )}

      </div>

    </nav>
  );
}