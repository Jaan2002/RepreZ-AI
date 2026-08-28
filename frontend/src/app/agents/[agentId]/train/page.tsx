"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { useParams, useRouter } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type Agent = {
  id: number;
  business_name: string;
};

type Message = {
  id: string;
  role: "assistant" | "user";
  content: string;
};

export default function TrainAgentPage() {
  const params = useParams();
  const router = useRouter();

  const agentId = params.agentId as string;

  const [agent, setAgent] = useState<Agent | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  /*
   * Load the Agent
   */
  useEffect(() => {
    if (!agentId) return;

    async function loadAgent() {
      try {
        if (!API_URL) {
          throw new Error(
            "NEXT_PUBLIC_API_URL is not configured."
          );
        }

        const response = await fetch(
          `${API_URL}/agents/${agentId}/`
        );

        if (!response.ok) {
          const errorData = await response.json().catch(() => null);

          throw new Error(
            errorData?.detail || "Unable to load AI Representative."
          );
        }

        const data: Agent = await response.json();

        setAgent(data);

        /*
         * Initial welcome message.
         *
         * The backend onboarding endpoint starts responding
         * after the owner sends their first message.
         */
        setMessages([
          {
            id: "welcome",
            role: "assistant",
            content: `Hi! I'm your AI Representative for ${data.business_name}. 👋

Let's get to know your business.

I'll ask you one question at a time and remember what you tell me.

What products or services does ${data.business_name} offer?`,
          },
        ]);
      } catch (error) {
        console.error("Load agent error:", error);

        setError(
          error instanceof Error
            ? error.message
            : "Unable to load your AI Representative."
        );
      } finally {
        setLoading(false);
      }
    }

    loadAgent();
  }, [agentId]);

  /*
   * Automatically scroll to newest message.
   */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, sending]);

  /*
   * Send owner's message to FastAPI.
   */
  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedMessage = input.trim();

    if (!trimmedMessage || sending || !agentId) {
      return;
    }

    if (!API_URL) {
      setError(
        "NEXT_PUBLIC_API_URL is not configured. Check your frontend .env.local file."
      );
      return;
    }

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: trimmedMessage,
    };

    /*
     * Immediately show owner's message.
     */
    setMessages((current) => [
      ...current,
      userMessage,
    ]);

    setInput("");
    setSending(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/agents/${agentId}/onboarding/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: trimmedMessage,
          }),
        }
      );

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            "The AI Representative could not process your message."
        );
      }

      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content:
          data?.reply ||
          "I received your message, but I couldn't generate a response.",
      };

      setMessages((current) => [
        ...current,
        assistantMessage,
      ]);
    } catch (error) {
      console.error("Training chat error:", error);

      setError(
        error instanceof Error
          ? error.message
          : "Something went wrong while talking to your AI Representative."
      );
    } finally {
      setSending(false);
    }
  }

  /*
   * Loading state
   */
  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#f8f7ff]">
        <div className="text-center">
          <div className="mx-auto flex h-14 w-14 animate-pulse items-center justify-center rounded-2xl bg-gray-950 text-xl font-bold text-white">
            R
          </div>

          <p className="mt-4 text-sm text-gray-500">
            Preparing your AI Representative...
          </p>
        </div>
      </main>
    );
  }

  /*
   * Error state
   */
  if (error && !agent) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#f8f7ff] px-6">
        <div className="w-full max-w-md rounded-3xl border border-red-100 bg-white p-8 text-center shadow-xl">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-red-50 text-xl">
            !
          </div>

          <h1 className="mt-5 text-xl font-bold text-gray-950">
            Something went wrong
          </h1>

          <p className="mt-2 text-sm leading-6 text-red-600">
            {error}
          </p>

          <button
            onClick={() => router.back()}
            className="mt-6 rounded-xl bg-gray-950 px-5 py-3 text-sm font-medium text-white hover:bg-gray-800"
          >
            Go Back
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#f8f7ff]">
      {/* Background decoration */}
      <div className="pointer-events-none absolute left-[-120px] top-[-120px] h-80 w-80 rounded-full bg-purple-200/40 blur-3xl" />

      <div className="pointer-events-none absolute bottom-[-120px] right-[-100px] h-96 w-96 rounded-full bg-pink-200/30 blur-3xl" />

      <div className="relative flex min-h-screen flex-col">
        {/* Header */}
        <header className="border-b border-gray-200/70 bg-white/80 backdrop-blur-xl">
          <div className="mx-auto flex h-20 w-full max-w-6xl items-center justify-between px-6 sm:px-8">
            {/* Brand */}
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gray-950 text-sm font-bold text-white shadow-lg">
                R
              </div>

              <div>
                <p className="text-sm font-bold tracking-tight text-gray-950">
                  REPREZ
                </p>

                <p className="text-xs text-gray-400">
                  AI Representative
                </p>
              </div>
            </div>

            {/* Business */}
            <div className="hidden items-center gap-3 sm:flex">
              <div className="text-right">
                <p className="text-xs text-gray-400">
                  TRAINING
                </p>

                <p className="text-sm font-semibold text-gray-800">
                  {agent?.business_name}
                </p>
              </div>

              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-purple-100 text-sm font-bold text-purple-700">
                {agent?.business_name?.charAt(0).toUpperCase()}
              </div>
            </div>

            {/* Exit */}
            <button
              onClick={() => router.back()}
              className="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-600 transition hover:bg-gray-50"
            >
              Exit
            </button>
          </div>
        </header>

        {/* Main */}
        <div className="flex flex-1 justify-center px-4 py-6 sm:px-6">
          <div className="flex w-full max-w-4xl flex-col overflow-hidden rounded-[2rem] border border-white/80 bg-white/90 shadow-2xl shadow-purple-100/50 backdrop-blur-xl">
            {/* Chat header */}
            <div className="border-b border-gray-100 px-5 py-5 sm:px-7">
              <div className="flex items-center gap-4">
                {/* AI avatar */}
                <div className="relative">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-purple-600 to-violet-700 text-xl text-white shadow-lg shadow-purple-200">
                    ✦
                  </div>

                  <span className="absolute -bottom-1 -right-1 h-3.5 w-3.5 rounded-full border-2 border-white bg-green-500" />
                </div>

                <div>
                  <h1 className="font-bold text-gray-950">
                    Your AI Representative
                  </h1>

                  <p className="text-sm text-gray-500">
                    Learning about {agent?.business_name}
                  </p>
                </div>
              </div>

              {/* Progress hint */}
              <div className="mt-5 rounded-xl bg-purple-50 px-4 py-3">
                <p className="text-xs leading-5 text-purple-700">
                  <span className="font-semibold">
                    Training mode
                  </span>{" "}
                  — Tell me about your business naturally. I'll ask
                  follow-up questions and build your business knowledge as we
                  talk.
                </p>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-5 py-6 sm:px-8">
              <div className="space-y-6">
                {messages.map((message) => {
                  const isUser = message.role === "user";

                  return (
                    <div
                      key={message.id}
                      className={`flex ${
                        isUser
                          ? "justify-end"
                          : "justify-start"
                      }`}
                    >
                      <div
                        className={`flex max-w-[85%] gap-3 sm:max-w-[75%] ${
                          isUser
                            ? "flex-row-reverse"
                            : "flex-row"
                        }`}
                      >
                        {/* Avatar */}
                        <div
                          className={`mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-xl text-xs font-bold ${
                            isUser
                              ? "bg-gray-950 text-white"
                              : "bg-purple-100 text-purple-700"
                          }`}
                        >
                          {isUser
                            ? "You"
                            : "✦"}
                        </div>

                        {/* Bubble */}
                        <div
                          className={`rounded-2xl px-4 py-3 text-sm leading-6 ${
                            isUser
                              ? "rounded-tr-md bg-gray-950 text-white"
                              : "rounded-tl-md border border-gray-100 bg-gray-50 text-gray-700"
                          }`}
                        >
                          <p className="whitespace-pre-line">
                            {message.content}
                          </p>
                        </div>
                      </div>
                    </div>
                  );
                })}

                {/* Typing indicator */}
                {sending && (
                  <div className="flex justify-start">
                    <div className="flex max-w-[75%] gap-3">
                      <div className="mt-1 flex h-8 w-8 items-center justify-center rounded-xl bg-purple-100 text-xs text-purple-700">
                        ✦
                      </div>

                      <div className="rounded-2xl rounded-tl-md border border-gray-100 bg-gray-50 px-5 py-4">
                        <div className="flex gap-1.5">
                          <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400 [animation-delay:-0.3s]" />
                          <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400 [animation-delay:-0.15s]" />
                          <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400" />
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="mx-5 mb-3 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600 sm:mx-7">
                {error}
              </div>
            )}

            {/* Input */}
            <div className="border-t border-gray-100 bg-white p-4 sm:p-5">
              <form
                onSubmit={handleSubmit}
                className="flex items-end gap-3 rounded-2xl border border-gray-200 bg-gray-50 p-2 transition focus-within:border-purple-300 focus-within:ring-4 focus-within:ring-purple-50"
              >
                <textarea
                  value={input}
                  onChange={(event) =>
                    setInput(event.target.value)
                  }
                  onKeyDown={(event) => {
                    if (
                      event.key === "Enter" &&
                      !event.shiftKey
                    ) {
                      event.preventDefault();

                      if (!sending && input.trim()) {
                        event.currentTarget.form?.requestSubmit();
                      }
                    }
                  }}
                  placeholder="Tell me about your business..."
                  rows={1}
                  disabled={sending}
                  className="max-h-32 min-h-[48px] flex-1 resize-none bg-transparent px-3 py-3 text-sm text-gray-900 outline-none placeholder:text-gray-400 disabled:cursor-not-allowed"
                />

                <button
                  type="submit"
                  disabled={sending || !input.trim()}
                  className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gray-950 text-lg text-white shadow-md transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-40"
                  aria-label="Send message"
                >
                  ↑
                </button>
              </form>

              <p className="mt-3 text-center text-[11px] text-gray-400">
                Press Enter to send · Shift + Enter for a new line
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="pb-4 text-center">
          <p className="text-[11px] text-gray-400">
            Your AI learns from the information you provide.
          </p>
        </div>
      </div>
    </main>
  );
}

