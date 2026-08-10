"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { login, register } from "../../lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState("login");
  const [error, setError] = useState("");
  const router = useRouter();

  async function submit(e) {
    e.preventDefault();
    setError("");
    try {
      if (mode === "register") {
        await register(email, password);
      }
      await login(email, password);
      router.push("/dashboard");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ maxWidth: 360, margin: "80px auto", padding: 24 }}>
      <h1 style={{ fontSize: 20 }}>Multi-Cloud Free-Tier Platform</h1>
      <form onSubmit={submit} style={{ display: "flex", flexDirection: "column", gap: 12, marginTop: 24 }}>
        <input placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)}
          style={inputStyle} />
        <input placeholder="password" type="password" value={password}
          onChange={(e) => setPassword(e.target.value)} style={inputStyle} />
        {error && <div style={{ color: "#f85149", fontSize: 13 }}>{error}</div>}
        <button type="submit" style={buttonStyle}>{mode === "login" ? "Log in" : "Register & log in"}</button>
      </form>
      <button onClick={() => setMode(mode === "login" ? "register" : "login")}
        style={{ background: "none", border: "none", color: "#58a6ff", marginTop: 12, cursor: "pointer" }}>
        {mode === "login" ? "Need an account? Register" : "Have an account? Log in"}
      </button>
    </div>
  );
}

const inputStyle = { padding: 10, borderRadius: 6, border: "1px solid #30363d", background: "#161b22", color: "#e6edf3" };
const buttonStyle = { padding: 10, borderRadius: 6, border: "none", background: "#238636", color: "white", cursor: "pointer" };
