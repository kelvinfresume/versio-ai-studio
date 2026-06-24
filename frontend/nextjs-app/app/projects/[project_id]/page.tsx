"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

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

type StoryboardScene = {
  storyboard_id?: string;
  project_id?: string;
  scene: number;
  title: string;
  visual: string;
  camera: string;
  emotion: string;
  created_at?: string;
};

type StoryboardResponse = {
  project_id?: string;
  project_name?: string;
  status?: string;
  storyboard?: StoryboardScene[];
};

type SceneImage = {
  image_id: string;
  project_id: string;
  scene: number;
  bucket: string;
  object_key: string;
  prompt: string;
  status: string;
  created_at: string;
  download_url: string;
};

type SceneImagesResponse = {
  project_id?: string;
  project_name?: string;
  status?: string;
  images?: SceneImage[];
};

export default function ProjectDetailsPage() {
  const params = useParams();
  const projectId = params.project_id as string;

  const [project, setProject] = useState<Project | null>(null);
  const [storyboard, setStoryboard] = useState<StoryboardResponse | null>(null);
  const [sceneImages, setSceneImages] = useState<SceneImagesResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [imageStatus, setImageStatus] = useState("");
  const [generatingImages, setGeneratingImages] = useState(false);
  const [error, setError] = useState("");

  const scenes = storyboard?.storyboard ?? [];
  const images = sceneImages?.images ?? [];

  async function loadProject() {
    try {
      const projectRes = await fetch(`${API_BASE_URL}/projects/${projectId}`);

      if (!projectRes.ok) {
        throw new Error("Project not found");
      }

      const projectData = await projectRes.json();
      setProject(projectData);

      const storyboardRes = await fetch(
        `${API_BASE_URL}/projects/${projectId}/storyboard`
      );

      if (storyboardRes.ok) {
        const storyboardData = await storyboardRes.json();
        setStoryboard(storyboardData);
      } else {
        setStoryboard({ storyboard: [] });
      }

      const imagesRes = await fetch(`${API_BASE_URL}/projects/${projectId}/images`);

      if (imagesRes.ok) {
        const imagesData = await imagesRes.json();
        setSceneImages(imagesData);
      } else {
        setSceneImages({ images: [] });
      }
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Unable to load project.");
      }
    } finally {
      setLoading(false);
    }
  }

  async function generateImages() {
    setGeneratingImages(true);
    setImageStatus("Generating scene images...");

    try {
      const res = await fetch(`${API_BASE_URL}/projects/${projectId}/images`, {
        method: "POST",
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Image generation failed.");
      }

      setSceneImages(data);
      setImageStatus("Scene images generated.");
      await loadProject();
    } catch (err) {
      if (err instanceof Error) {
        setImageStatus(err.message);
      } else {
        setImageStatus("Image generation failed.");
      }
    } finally {
      setGeneratingImages(false);
    }
  }

  useEffect(() => {
    loadProject();
  }, []);

  if (loading) {
    return (
      <main className="min-h-screen bg-[#050505] text-white p-10">
        <p>Loading project...</p>
      </main>
    );
  }

  if (error || !project) {
    return (
      <main className="min-h-screen bg-[#050505] text-white p-10 space-y-4">
        <p className="text-red-400">{error || "Project not found."}</p>
        <Link href="/" className="text-cyan-300">
          Back to dashboard
        </Link>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#050505] text-white p-6 md:p-10">
      <section className="max-w-6xl mx-auto space-y-8">
        <Link href="/" className="text-cyan-300">
          ← Back to Dashboard
        </Link>

        <div>
          <h1 className="text-4xl md:text-6xl font-bold text-cyan-300">
            {project.project_name}
          </h1>
          <p className="text-gray-400 mt-2">{project.story_prompt}</p>
        </div>

        <div className="rounded-xl border border-gray-800 bg-gray-950/70 p-6 space-y-3">
          <h2 className="text-2xl font-semibold">Project Metadata</h2>

          <p>
            Project ID:{" "}
            <span className="text-gray-400">{project.project_id}</span>
          </p>

          <p>
            Status: <span className="text-green-400">{project.status}</span>
          </p>

          <p>
            File: <span className="text-gray-400">{project.filename}</span>
          </p>

          <p>
            Content Type:{" "}
            <span className="text-gray-400">{project.content_type}</span>
          </p>

          <p className="break-all">
            Object Key:{" "}
            <span className="text-gray-400">{project.object_key}</span>
          </p>

          <a
            href={`${API_BASE_URL}/projects/${project.project_id}/download`}
            className="inline-block rounded bg-white text-black px-4 py-2 text-sm font-semibold hover:bg-cyan-200"
          >
            ⬇️ Download Audio
          </a>
        </div>

        <div className="rounded-xl border border-purple-900/50 bg-purple-950/20 p-6 space-y-4">
          <h2 className="text-2xl font-semibold text-purple-300">
            Persistent Storyboard
          </h2>

          {scenes.length === 0 ? (
            <p className="text-gray-400">No storyboard generated yet.</p>
          ) : (
            scenes.map((scene) => (
              <div
                key={scene.storyboard_id || `${project.project_id}-${scene.scene}`}
                className="rounded border border-gray-800 bg-black p-4"
              >
                <h3 className="text-xl font-bold text-cyan-300">
                  Scene {scene.scene}: {scene.title}
                </h3>
                <p className="text-gray-300 mt-2">Visual: {scene.visual}</p>
                <p className="text-gray-400">Camera: {scene.camera}</p>
                <p className="text-gray-400">Emotion: {scene.emotion}</p>
              </div>
            ))
          )}
        </div>

        <div className="rounded-xl border border-cyan-900/50 bg-cyan-950/10 p-6 space-y-4">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h2 className="text-2xl font-semibold text-cyan-300">
                Scene Images
              </h2>
              <p className="text-gray-400 text-sm">
                Mock generated images stored in MinIO and tracked in PostgreSQL.
              </p>
            </div>

            <button
              onClick={generateImages}
              disabled={generatingImages}
              className="rounded bg-cyan-400 text-black px-4 py-2 text-sm font-semibold hover:bg-cyan-300 disabled:opacity-50"
            >
              {generatingImages ? "Generating..." : "🖼 Generate Images"}
            </button>
          </div>

          {imageStatus && <p className="text-sm text-gray-300">{imageStatus}</p>}

          {images.length === 0 ? (
            <p className="text-gray-400">
              No scene images generated yet. Generate a storyboard first, then generate images.
            </p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {images.map((image) => (
                <div
                  key={image.image_id}
                  className="rounded border border-gray-800 bg-black p-4 space-y-3"
                >
                  <h3 className="text-lg font-bold text-cyan-300">
                    Scene {image.scene}
                  </h3>

                <Image
                  src={`${API_BASE_URL}${image.download_url}`}
                  alt={`Scene ${image.scene}`}
                  width={512}
                  height={512}
                  unoptimized
                  className="w-full rounded border border-gray-800 bg-gray-950"
                />

                  <p className="text-sm text-gray-400">
                    Status: {image.status}
                  </p>

                  <p className="text-sm text-gray-500 break-all">
                    Object: {image.object_key}
                  </p>

                  <p className="text-sm text-gray-300">
                    Prompt: {image.prompt}
                  </p>

                  <a
                    href={`${API_BASE_URL}${image.download_url}`}
                    className="inline-block rounded bg-white text-black px-4 py-2 text-sm font-semibold hover:bg-cyan-200"
                  >
                    ⬇️ Download Image
                  </a>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="rounded-xl border border-gray-800 bg-gray-950/70 p-6">
          <h2 className="text-2xl font-semibold">Future Assets</h2>
          <p className="text-gray-400 mt-2">
            Video clips, captions, timeline exports, and final anime videos will
            appear here later.
          </p>
        </div>
      </section>
    </main>
  );
}
