// src/components/Navbar.tsx
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../src/context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav className="flex justify-between items-center px-4 py-2 bg-gray-100 shadow">
      <Link to="/" className="text-lg font-bold">
        VaultGuard
      </Link>

      <div className="space-x-4">
        {user ? (
          <>
            <span className="text-sm">Logged in as {user.email}</span>
            <Link to="/dashboard" className="text-blue-500 hover:underline">
              Dashboard
            </Link>
            <button
              onClick={handleLogout}
              className="bg-black text-white px-3 py-1 rounded hover:bg-opacity-80"
            >
              Logout
            </button>
          </>
        ) : (
          <Link
            to="/login"
            className="bg-black text-white px-4 py-1 rounded hover:bg-opacity-80"
          >
            Login
          </Link>
        )}
      </div>
    </nav>
  );
}
