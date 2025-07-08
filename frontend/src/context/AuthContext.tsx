// src/context/AuthContext.tsx
import React, { createContext, useContext, useEffect, useState } from "react";
import { fetchWithAuth } from "../lib/fetchWithAuth";

type User = {
  email: string;
};

type AuthContextType = {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  // ✅ Attempt to fetch current user or refresh access token on mount
  useEffect(() => {
    const fetchUser = async () => {
      let token = localStorage.getItem("accessToken");

      // Try /auth/me with current token if present
      if (token) {
        const res = await fetchWithAuth("http://localhost:8000/auth/me");
        if (res.ok) {
          const data = await res.json();
          setUser(data);
          return;
        }
      }

      // 🚨 Attempt to refresh access token using secure cookie
      try {
        const refreshRes = await fetch("http://localhost:8000/auth/refresh", {
          method: "POST",
          credentials: "include", // Important for sending HTTP-only cookie
        });

        if (!refreshRes.ok) {
          localStorage.removeItem("accessToken");
          setUser(null);
          return;
        }

        const { access_token } = await refreshRes.json();
        localStorage.setItem("accessToken", access_token);

        // Fetch user with new token
        const userRes = await fetch("http://localhost:8000/auth/me", {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });

        if (userRes.ok) {
          const userData = await userRes.json();
          setUser(userData);
        } else {
          localStorage.removeItem("accessToken");
        }
      } catch (err) {
        console.error("Token refresh failed:", err);
        localStorage.removeItem("accessToken");
      }
    };

    fetchUser();
  }, []);

  // 🔐 Login + user fetch
  const login = async (email: string, password: string) => {
    const res = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
      credentials: "include",
    });

    if (!res.ok) throw new Error("Login failed");

    const data = await res.json();
    localStorage.setItem("accessToken", data.access_token);

    const meRes = await fetch("http://localhost:8000/auth/me", {
      headers: { Authorization: `Bearer ${data.access_token}` },
    });

    if (!meRes.ok) throw new Error("Failed to fetch user after login");

    const userData = await meRes.json();
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem("accessToken");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
