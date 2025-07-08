import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { AnimatePresence, motion } from "framer-motion";
import { z } from "zod";
import { toast } from "sonner";
import { useFormStore } from "../store/formStore";
import PasswordStrengthBar from "../components/StrengthBar";


const schema = z.object({
  email: z.string().email({ message: "Invalid email address" }),
  password: z
    .string()
    .min(12, "Password must be at least 12 characters")
    .regex(/[A-Z]/, "Include an uppercase letter")
    .regex(/[a-z]/, "Include a lowercase letter")
    .regex(/[0-9]/, "Include a number")
    .regex(/[^A-Za-z0-9]/, "Include a special character"),
});

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState<"login" | "register">("login");

  const { login } = useAuth();
  const navigate = useNavigate();
  const { isLoading, setLoading } = useFormStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const result = schema.safeParse({ email, password });
    if (!result.success) {
      result.error.errors.forEach((err) => toast.error(err.message));
      return;
    }

    try {
      setLoading(true);
      if (mode === "register") {
        const res = await fetch("http://localhost:8000/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });

        if (!res.ok) throw new Error("Registration failed");
      }

      await login(email, password);
      toast.success(mode === "login" ? "Welcome back!" : "Account created ✅");
      navigate("/dashboard");
    } catch (err) {
      toast.error(`${mode === "login" ? "Login" : "Registration"} failed.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4">
      <div className="bg-zinc-900 text-white p-8 rounded-xl w-full max-w-sm relative shadow-xl border border-zinc-700">
        <div className="absolute -inset-0.5 bg-gradient-to-tr blur-lg opacity-20 rounded-xl animate-pulse" />
        <div className="relative z-10">
          <AnimatePresence mode="wait">
            <motion.div
              key={mode}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <h1 className="text-2xl font-bold text-center mb-4 tracking-wide">
                {mode === "login"
                  ? "🔐 VaultGuard Login"
                  : "🧾 Register for VaultGuard"}
              </h1>
              <form onSubmit={handleSubmit} className="space-y-4">
                <input
                  className="w-full px-3 py-2 bg-zinc-800 border border-zinc-600 rounded placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
                <input
                  className="w-full px-3 py-2 bg-zinc-800 border border-zinc-600 rounded placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />

                {mode === "register" && (
                  <PasswordStrengthBar password={password} />
                )}

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-cyan-600 hover:bg-cyan-700 text-white py-2 rounded transition-colors duration-200"
                >
                  {isLoading
                    ? "Please wait..."
                    : mode === "login"
                    ? "Login"
                    : "Register"}
                </button>
              </form>
            </motion.div>
          </AnimatePresence>

          <div className="mt-4 text-sm text-center text-muted-foreground">
            {mode === "login" ? (
              <>
                Don&apos;t have an account?{" "}
                <button
                  className="text-cyan-400 hover:underline"
                  onClick={() => setMode("register")}
                >
                  Register here
                </button>
                <p className="mt-4 text-xs text-zinc-500 text-center leading-snug">
                  Password must include upper/lowercase, number, symbol, and be 12+
                  characters.
                </p>
              </>
            ) : (
              <>
                Already have an account?{" "}
                <button
                  className="text-cyan-400 hover:underline"
                  onClick={() => setMode("login")}
                >
                  Login
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
