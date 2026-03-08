import { createContext, useState, useContext } from "react";

export const AuthContext = createContext();

export function AuthProvider({ children }) {

  let storedUser = null;

  try {
    storedUser = JSON.parse(localStorage.getItem("user"));
  } catch {
    storedUser = null;
  }

  const [user, setUser] = useState(storedUser);

  const login = (userData) => {
    localStorage.setItem("user", JSON.stringify(userData));
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem("user");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);