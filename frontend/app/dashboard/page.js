"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch, logout } from "../../lib/api";

export default function Dashboard() {
  const router = useRouter();
  const [catalog, setCatalog] = useState({});
  const [estimates, setEstimates] = useState([]);
  const [resources, setResources] = useState([]);
  const [provider, setProvider] = useState("aws");
  const [error, setError] = useState("");

  async function refresh() {
    const [c, e, r] = await Promise.all([
      apiFetch("/resources/catalog"),
      apiFetch("/resources/catalog/estimate"),
      apiFetch("/resources"),
    ]);
    setCatalog(c);
    setEstimates(e);
    setResources(r);
  }

  useEffect(() => {
    if (!localStorage.getItem("token")) {
      router.replace("/login");
      return;
    }
    refresh().catch((err) => setError(err.message));
  }, []);

  async function provision() {
    setError("");
    try {
      await apiFetch("/resources", {
        method: "POST",
        body: JSON.stringify({ provider, resource_type: "compute" }),
      });
      await refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  async function teardown(id) {
    await apiFetch(`/resources/${id}`, { method: "DELETE" });
    await refresh();
  }

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", padding: 24 }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h1 style={{ fontSize: 20 }}>Multi-Cloud Free-Tier Platform</h1>
        <button onClick={() => { logout(); router.push("/login"); }} style={linkBtn}>Log out</button>
      </div>

      <section style={card}>
        <h2 style={h2}>Provision (free-tier only, server-enforced)</h2>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <select value={provider} onChange={(e) => setProvider(e.target.value)} style={inputStyle}>
            {Object.keys(catalog).map((p) => <option key={p} value={p}>{p}</option>)}
          </select>
          <button onClick={provision} style={buttonStyle}>Spin up compute</button>
        </div>
        {catalog[provider]?.compute && (
          <p style={{ fontSize: 13, color: "#8b949e", marginTop: 8 }}>
            Locked spec: {JSON.stringify(catalog[provider].compute)}
          </p>
        )}
        {error && <div style={{ color: "#f85149", marginTop: 8 }}>{error}</div>}
      </section>

      <section style={card}>
        <h2 style={h2}>Theoretical cost (actual spend: $0 on free tier)</h2>
        <table style={{ width: "100%", fontSize: 13 }}>
          <thead><tr><th style={th}>Provider</th><th style={th}>Instance</th><th style={th}>$/hr</th><th style={th}>$/mo if paid</th></tr></thead>
          <tbody>
            {estimates.map((e, i) => (
              <tr key={i}>
                <td style={td}>{e.provider}</td>
                <td style={td}>{e.instance_label}</td>
                <td style={td}>${e.hourly_usd}</td>
                <td style={td}>${e.monthly_usd_if_paid}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section style={card}>
        <h2 style={h2}>Your resources</h2>
        {resources.length === 0 && <p style={{ color: "#8b949e" }}>Nothing provisioned yet.</p>}
        {resources.map((r) => (
          <div key={r.id} style={row}>
            <div>
              <strong>{r.provider}</strong> · {r.resource_type} · <span style={{ color: statusColor(r.status) }}>{r.status}</span>
              {r.outputs?.public_ip && <span> · {r.outputs.public_ip.value}</span>}
              {r.error_message && <div style={{ color: "#f85149", fontSize: 12 }}>{r.error_message}</div>}
            </div>
            {r.status === "active" && <button onClick={() => teardown(r.id)} style={destroyBtn}>Destroy</button>}
          </div>
        ))}
      </section>
    </div>
  );
}

function statusColor(s) {
  return { active: "#3fb950", error: "#f85149", provisioning: "#d29922", pending: "#8b949e" }[s] || "#8b949e";
}

const card = { border: "1px solid #30363d", borderRadius: 8, padding: 16, marginTop: 16 };
const h2 = { fontSize: 15, marginTop: 0 };
const inputStyle = { padding: 8, borderRadius: 6, border: "1px solid #30363d", background: "#161b22", color: "#e6edf3" };
const buttonStyle = { padding: 8, borderRadius: 6, border: "none", background: "#238636", color: "white", cursor: "pointer" };
const destroyBtn = { padding: "6px 10px", borderRadius: 6, border: "none", background: "#da3633", color: "white", cursor: "pointer" };
const linkBtn = { background: "none", border: "none", color: "#58a6ff", cursor: "pointer" };
const row = { display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 0", borderTop: "1px solid #21262d" };
const th = { textAlign: "left", borderBottom: "1px solid #30363d", padding: 6 };
const td = { padding: 6, borderBottom: "1px solid #21262d" };
