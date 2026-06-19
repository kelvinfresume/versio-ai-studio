"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [apiStatus, setApiStatus] = useState("checking...");

  useEffect(() => {
    fetch("http://localhost:8000/health")
      .then((res) => res.json())
      .then((data) => setApiStatus(data.status))
      .catch(() => setApiStatus("offline"));
  }, []);

  return (
    <main className="min-h-screen bg-black text-white p-10">
      <section className="max-w-3xl mx-auto space-y-6">
        <h1 className="text-5xl font-bold">Versio AI Studio</h1>
        <p className="text-lg text-gray-300">
          Song-to-anime cinematic story generator.
        </p>

        <div className="rounded-xl border border-gray-700 p-6">
          <h2 className="text-2xl font-semibold mb-2">Backend Status</h2>
          <p>API: <span className="font-bold">{apiStatus}</span></p>
        </div>

        <div className="rounded-xl border border-gray-700 p-6 space-y-4">
          <h2 className="text-2xl font-semibold">Create Project</h2>
          <input className="w-full rounded bg-gray-900 border border-gray-700 p-3" placeholder="Project name" />
          <textarea className="w-full rounded bg-gray-900 border border-gray-700 p-3" placeholder="Describe the anime story..." />
          <button className="rounded bg-white text-black px-5 py-3 font-semibold">
            Generate Storyboard
          </button>
        </div>
      </section>
    </main>
  );
}
