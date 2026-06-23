"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";

const API_BASE_URL = "http://localhost:8000";

type Project = {
  project_id: string;
  project_name: string;
  story_prompt: string;
  bucket: string;
  object_key: string;
  filename: string;
  content_type: string;
  status: string;
  created_at: string;
};

export default function Home() {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [apiStatus, setApiStatus] = useState("checking...");
  const [projectName, setProjectName] = useState("");
  const [storyPrompt, setStoryPrompt] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [lastResponse, setLastResponse] = useState("");
  const [projects, setProjects] = useState<Project[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  async function fetchProjects() {
    try {
      const res = await fetch(`${API_BASE_URL}/projects`);
      const data = await res.json();
      setProjects(Array.isArray(data) ? data : []);
    } catch {
      setProjects([]);
    }
  }

  useEffect(() => {
    fetch(`${API_BASE_URL}/health`)
      .then((res) => res.json())
      .then((data) => setApiStatus(data.status))
      .catch(() => setApiStatus("offline"));

    fetchProjects();
  }, []);

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const selectedFile = e.target.files?.[0];

    if (!selectedFile) {
      setFile(null);
      return;
    }

    const lowerName = selectedFile.name.toLowerCase();
    const isValidAudio =
      lowerName.endsWith(".mp3") ||
      lowerName.endsWith(".wav") ||
      selectedFile.type === "audio/mpeg" ||
      selectedFile.type === "audio/wav" ||
      selectedFile.type === "audio/x-wav";

    if (!isValidAudio) {
      setFile(null);
      setUploadStatus("Please select an MP3 or WAV file.");
      return;
    }

    setFile(selectedFile);
    setUploadStatus(`Selected file: ${selectedFile.name}`);
  }

  async function handleUpload(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLastResponse("");

    if (!projectName.trim()) {
      setUploadStatus("Please add a project name.");
      return;
    }

    if (!storyPrompt.trim()) {
      setUploadStatus("Please add a story prompt.");
      return;
    }

    if (!file) {
      setUploadStatus("Please select an MP3 or WAV file.");
      return;
    }

    const formData = new FormData();
    formData.append("project_name", projectName.trim());
    formData.append("story_prompt", storyPrompt.trim());
    formData.append("file", file);

    setIsUploading(true);
    setUploadStatus("Uploading...");

    try {
      const res = await fetch(`${API_BASE_URL}/uploads/song`, {
        method: "POST",
        body: formData,
      });

      const text = await res.text();

      if (!res.ok) {
        setLastResponse(text);
        throw new Error(text || "Upload failed");
      }

      const data = JSON.parse(text);
      setLastResponse(JSON.stringify(data, null, 2));

      setUploadStatus("Upload complete.");
      setProjectName("");
      setStoryPrompt("");
      setFile(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

      await fetchProjects();
    } catch (error) {
      setUploadStatus("Upload failed. Check backend logs or response below.");
      if (error instanceof Error) {
        setLastResponse(error.message);
      }
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#050505] text-white p-6 md:p-10">
      <section className="max-w-6xl mx-auto space-y-8">
        <div className="flex flex-col md:flex-row md:items-center gap-6">
          <Image
            src="/versio-logo.svg"
            alt="Versio AI Studio"
            width={88}
            height={88}
            priority
          />

          <div>
            <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-purple-400 via-cyan-400 to-yellow-300 bg-clip-text text-transparent">
              Versio AI Studio
            </h1>

            <p className="text-lg text-gray-300 mt-2">
              AI Anime Cinema Engine
            </p>

            <p className="text-sm text-gray-500">
              Transform music into cinematic anime experiences.
            </p>
          </div>
        </div>

        <div className="rounded-2xl border border-purple-900/50 bg-gradient-to-r from-purple-950/40 to-cyan-950/20 p-6">
          <h2 className="text-2xl font-bold mb-2">
            Welcome to Versio
          </h2>

          <p className="text-gray-300">
            Upload an MP3 or WAV file, store assets in object storage,
            persist metadata in PostgreSQL, and prepare projects for AI
            storyboard and anime video generation.
          </p>

          <div className="mt-4 flex gap-3 flex-wrap">
            <span className="px-3 py-1 rounded-full bg-purple-900/50 text-purple-300 text-sm">
              FastAPI
            </span>

            <span className="px-3 py-1 rounded-full bg-blue-900/50 text-blue-300 text-sm">
              PostgreSQL
            </span>

            <span className="px-3 py-1 rounded-full bg-green-900/50 text-green-300 text-sm">
              MinIO
            </span>

            <span className="px-3 py-1 rounded-full bg-yellow-900/50 text-yellow-300 text-sm">
              Vault
            </span>

            <span className="px-3 py-1 rounded-full bg-red-900/50 text-red-300 text-sm">
              Jenkins
            </span>
          </div>
        </div>

        <div className="rounded-xl border border-gray-800 bg-gray-950/70 p-6">
          <h2 className="text-2xl font-semibold mb-2">Backend Status</h2>
          <p>
            API:{" "}
            <span
              className={
                apiStatus === "healthy"
                  ? "font-bold text-green-400"
                  : "font-bold text-red-400"
              }
            >
              {apiStatus}
            </span>
          </p>
        </div>

        <form
          onSubmit={handleUpload}
          className="rounded-xl border border-gray-800 bg-gray-950/70 p-6 space-y-4"
        >
          <h2 className="text-2xl font-semibold">Upload Song Project</h2>

          <input
            className="w-full rounded bg-black border border-gray-700 p-3 outline-none focus:border-cyan-400"
            placeholder="Project name"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
          />

          <textarea
            className="w-full rounded bg-black border border-gray-700 p-3 min-h-28 outline-none focus:border-cyan-400"
            placeholder="Describe the anime story..."
            value={storyPrompt}
            onChange={(e) => setStoryPrompt(e.target.value)}
          />

          <input
            ref={fileInputRef}
            type="file"
            accept=".mp3,.wav,audio/mpeg,audio/wav,audio/x-wav"
            className="w-full rounded bg-black border border-gray-700 p-3"
            onChange={handleFileChange}
          />

          {file && (
            <p className="text-sm text-green-400">
              Ready to upload: {file.name} (
              {Math.max(1, Math.round(file.size / 1024 / 1024))} MB)
            </p>
          )}

          <button
            type="submit"
            disabled={isUploading}
            className="rounded bg-white text-black px-5 py-3 font-semibold hover:bg-cyan-200 disabled:opacity-50"
          >
            {isUploading ? "Uploading..." : "🚀 Upload Project"}
          </button>

          {uploadStatus && (
            <p className="text-sm text-gray-300">{uploadStatus}</p>
          )}

          {lastResponse && (
            <pre className="overflow-auto rounded bg-black border border-gray-800 p-4 text-xs text-gray-300">
              {lastResponse}
            </pre>
          )}
        </form>

        <div className="rounded-xl border border-gray-800 bg-gray-950/70 p-6 space-y-4">
          <div className="flex items-center justify-between gap-4">
            <h2 className="text-2xl font-semibold">Uploaded Projects</h2>

            <button
              onClick={fetchProjects}
              className="rounded border border-gray-700 px-3 py-2 text-sm hover:border-cyan-400"
            >
              Refresh
            </button>
          </div>

          {projects.length === 0 ? (
            <p className="text-gray-400">No projects uploaded yet.</p>
          ) : (
            <div className="space-y-4">
              {projects.map((project) => (
                <div
                  key={project.project_id}
                  className="rounded-lg border border-gray-800 p-4 bg-black"
                >
                  <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                    <div>
                      <h3 className="text-xl font-bold text-cyan-300">
                        {project.project_name}
                      </h3>

                      <p className="text-gray-300 mt-1">
                        {project.story_prompt}
                      </p>

                      <p className="text-sm text-gray-400 mt-2">
                        File: {project.filename}
                      </p>

                      <p className="text-sm text-gray-400">
                        Status: {project.status}
                      </p>

                      <p className="text-sm text-gray-500 break-all">
                        Object: {project.object_key}
                      </p>
                    </div>

                    <a
                      href={`${API_BASE_URL}/projects/${project.project_id}/download`}
                      className="inline-block rounded bg-white text-black px-4 py-2 text-sm font-semibold hover:bg-cyan-200"
                    >
                      ⬇️ Download Audio
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
