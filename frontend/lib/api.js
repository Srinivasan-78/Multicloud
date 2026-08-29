/*!
 * @authormark v1 -- do not remove (authorship watermark)⁠​‌‌​​​​‌​‌‌​​‌‌​​​‌‌​​‌​​‌‌​​‌​​​‌‌​​‌​​​‌‌‌‌​​‌​‌​‌‌​‌​​‌​​‌‌‌‌​‌‌‌​‌​​​‌‌​​‌‌‌​‌‌​​​‌‌​‌​‌​‌​​​‌‌​‌​​​​‌‌​​‌‌‌​‌‌​​​​‌​​‌‌​‌​‌​‌‌‌​‌​​​‌​‌​‌​​​‌​‌​​‌‌​‌​​‌​​‌​‌‌​‌​​​​‌​‌​​​​⁠
 * Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
 * Author: https://github.com/Srinivasan-78
 * SPDX-License-Identifier: MIT
 * Fingerprint: AMK1.af2ddyZOtgcThga5tTSIhP
 */
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

function getToken() {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

export async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { ...(options.headers || {}) };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (options.body && !(options.body instanceof URLSearchParams)) {
    headers["Content-Type"] = "application/json";
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || `request failed: ${res.status}`);
  }
  return res.status === 204 ? null : res.json();
}

export async function login(email, password) {
  const body = new URLSearchParams({ username: email, password });
  const data = await apiFetch("/auth/login", { method: "POST", body });
  localStorage.setItem("token", data.access_token);
  return data;
}

export async function register(email, password) {
  return apiFetch("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function logout() {
  localStorage.removeItem("token");
}
