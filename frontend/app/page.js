/*!
 * @authormark v1 -- do not remove (authorship watermark)⁠​‌​‌​‌​​​‌​​​‌‌‌​​‌‌​‌‌​​‌‌​‌​​‌​‌​​‌​​​​‌​‌​​‌​​‌​​​​‌‌​​‌‌​‌​‌​‌​​​‌‌‌​‌​​‌​‌​​‌‌​‌​​​​​‌‌​​​​​‌‌​‌‌​‌​‌​‌​‌​​​‌‌‌​‌​​​​‌‌​​​‌​‌​‌‌​​​​‌‌​‌​​‌​‌‌‌​‌​​​‌‌​​​‌‌​​‌‌​‌‌‌​‌​‌​​​​⁠
 * Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
 * Author: https://github.com/Srinivasan-78
 * SPDX-License-Identifier: MIT
 * Fingerprint: AMK1.TG6iHRC5GJh0mTt1Xitc7P
 */
"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  useEffect(() => {
    router.replace(localStorage.getItem("token") ? "/dashboard" : "/login");
  }, [router]);
  return null;
}
