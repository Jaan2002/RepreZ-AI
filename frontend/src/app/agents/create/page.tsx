
"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type AgentResponse = {
  id: number;
  business_name: string;
};

export default function CreateAgentPage() {
  const router = useRouter();

  const [businessName, setBusinessName] = useState("");
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");

  async function handleCreateAgent(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedBusinessName = businessName.trim();

    if (!trimmedBusinessName) {
      setError("Please enter your business name.");
      return;
    }

    if (!API_URL) {
      setError(
        "NEXT_PUBLIC_API_URL is not configured. Check your frontend .env.local file."
      );
      return;
    }

    setCreating(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/agents/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          business_name: trimmedBusinessName,
        }),
      });

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        throw new Error(
          data?.detail || "Unable to create your AI Representative."
        );
      }

      const agent: AgentResponse = data;

      console.log("Created agent:", agent);
      console.log("Redirecting to:", `/agents/${agent.id}/train`);
      router.push(`/agents/${agent.id}/train`);
    } catch (error) {
      console.error("Create agent error:", error);

      setError(
        error instanceof Error
          ? error.message
          : "Something went wrong while creating your AI Representative."
      );
    } finally {
      setCreating(false);
    }
  }

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#f8f7ff]">
      {/* Decorative background */}
      <div className="absolute left-[-100px] top-[-100px] h-72 w-72 rounded-full bg-purple-200/40 blur-3xl" />
      <div className="absolute bottom-[-120px] right-[-80px] h-80 w-80 rounded-full bg-pink-200/40 blur-3xl" />
      <div className="absolute right-[15%] top-[20%] h-48 w-48 rounded-full bg-blue-200/30 blur-3xl" />

      <div className="relative mx-auto flex min-h-screen max-w-6xl flex-col px-6 py-6 sm:px-10">
        {/* Header */}
        <header className="flex items-center justify-between">
          <button
            onClick={() => router.back()}
            className="group flex items-center gap-2 rounded-full border border-gray-200 bg-white/80 px-4 py-2 text-sm font-medium text-gray-700 shadow-sm backdrop-blur transition hover:border-gray-300 hover:bg-white"
          >
            <span className="transition-transform group-hover:-translate-x-1">
              ←
            </span>
            Back
          </button>

          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gray-950 text-sm font-bold text-white shadow-lg">
              R
            </div>

            <span className="text-lg font-bold tracking-tight text-gray-950">
              REPREZ
            </span>
          </div>
        </header>

        {/* Main content */}
        <div className="flex flex-1 items-center justify-center py-12">
          <div className="grid w-full max-w-5xl items-center gap-12 lg:grid-cols-2">
            {/* Left side */}
            <section>
              <div className="inline-flex items-center gap-2 rounded-full border border-purple-100 bg-white/80 px-4 py-2 text-sm font-medium text-purple-700 shadow-sm backdrop-blur">
                <span className="flex h-2 w-2 rounded-full bg-purple-500" />
                Create your AI Representative
              </div>

              <h1 className="mt-6 text-4xl font-bold tracking-tight text-gray-950 sm:text-5xl">
                Give your business
                <span className="block bg-gradient-to-r from-purple-600 via-violet-600 to-pink-500 bg-clip-text text-transparent">
                  someone who knows it.
                </span>
              </h1>

              <p className="mt-6 max-w-lg text-lg leading-8 text-gray-600">
                Create an AI Representative that learns about your business,
                talks to your customers, and grows with you over time.
              </p>

              <div className="mt-10 space-y-4">
                {[
                  ["01", "Tell it about your business"],
                  ["02", "Teach it through a natural conversation"],
                  ["03", "Let it represent you to your customers"],
                ].map(([number, text]) => (
                  <div
                    key={number}
                    className="flex items-center gap-4 text-sm font-medium text-gray-700"
                  >
                    <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-xs font-bold text-purple-600 shadow-sm ring-1 ring-gray-100">
                      {number}
                    </div>

                    {text}
                  </div>
                ))}
              </div>
            </section>

            {/* Create card */}
            <section className="rounded-[2rem] border border-white/80 bg-white/80 p-6 shadow-2xl shadow-purple-100/50 backdrop-blur-xl sm:p-8">
              <div className="mb-8">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-purple-600 to-violet-700 text-2xl text-white shadow-lg shadow-purple-200">
                  ✦
                </div>

                <h2 className="mt-6 text-2xl font-bold tracking-tight text-gray-950">
                  Let's create your representative
                </h2>

                <p className="mt-2 text-sm leading-6 text-gray-500">
                  Start with your business name. Your AI will learn the rest
                  from you through conversation.
                </p>
              </div>

              <form onSubmit={handleCreateAgent}>
                <label
                  htmlFor="businessName"
                  className="text-sm font-semibold text-gray-800"
                >
                  What is your business called?
                </label>

                <input
                  id="businessName"
                  type="text"
                  value={businessName}
                  onChange={(event) => setBusinessName(event.target.value)}
                  placeholder="e.g. Bean Theory"
                  disabled={creating}
                  autoFocus
                  minLength={2}
                  maxLength={100}
                  className="mt-3 w-full rounded-2xl border border-gray-200 bg-white px-5 py-4 text-base text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-purple-400 focus:ring-4 focus:ring-purple-100 disabled:cursor-not-allowed disabled:opacity-60"
                />

                {error && (
                  <div className="mt-4 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600">
                    {error}
                  </div>
                )}

                <button
                  type="submit"
                  disabled={creating || !businessName.trim()}
                  className="mt-6 flex w-full items-center justify-center gap-3 rounded-2xl bg-gray-950 px-5 py-4 text-sm font-semibold text-white shadow-xl shadow-gray-200 transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {creating ? (
                    <>
                      <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                      Creating your representative...
                    </>
                  ) : (
                    <>
                      Create AI Representative
                      <span className="text-lg">→</span>
                    </>
                  )}
                </button>
              </form>

              <p className="mt-5 text-center text-xs leading-5 text-gray-400">
                Next, you'll have a conversation with your AI Representative
                and teach it everything it needs to know about your business.
              </p>
            </section>
          </div>
        </div>

        {/* Footer */}
        <footer className="pb-2 text-center text-xs text-gray-400">
          Your business. Your knowledge. Your AI Representative.
        </footer>
      </div>
    </main>
  );
}

