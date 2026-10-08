
"use client";

import {
  FormEvent,
  KeyboardEvent,
  useEffect,
  useRef,
  useState,
} from "react";
import { useParams, useRouter } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type Agent = {
  id: number;
  business_name: string;
  status: string;
  created_at: string;
};

type Message = {
  id: string;
  role: "assistant" | "user";
  content: string;
};

type OnboardingResponse = {
  reply: string;
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
  const inputRef = useRef<HTMLTextAreaElement | null>(null);

  useEffect(() => {
    if (!agentId) {
      return;
    }

    async function loadAgent() {
      try {
        if (!API_URL) {
          throw new Error(
            "The frontend API URL is not configured. Please check your .env.local file."
          );
        }

        const response = await fetch(`${API_URL}/agents/${agentId}/`);

        const data = await response.json().catch(() => null);

        if (!response.ok) {
          throw new Error(
            typeof data?.detail === "string"
              ? data.detail
              : "Unable to load your AI Representative."
          );
        }

        setAgent(data);

        setMessages([
          {
            id: "welcome",
            role: "assistant",
            content: `Hi! I'm your AI Representative for ${data.business_name}. 👋

Let's teach me about your business.

Tell me anything you'd like me to know to get started. I'll ask follow-up questions one at a time and remember what you tell me.`,
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

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages, sending]);

  useEffect(() => {
    if (!sending && agent && !loading) {
      inputRef.current?.focus();
    }
  }, [sending, agent, loading]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedMessage = input.trim();

    if (!trimmedMessage || sending || !agentId) {
      return;
    }

    if (!API_URL) {
      setError(
        "The frontend API URL is not configured. Please check your .env.local file."
      );
      return;
    }

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: trimmedMessage,
    };

    setMessages((current) => [...current, userMessage]);
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

      const data: OnboardingResponse | null = await response
        .json()
        .catch(() => null);

      if (!response.ok) {
        throw new Error(
          typeof data?.reply === "string"
            ? data.reply
            : "The AI Representative could not process your message."
        );
      }

      if (!data?.reply) {
        throw new Error(
          "The AI Representative returned an empty response."
        );
      }

      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: data.reply,
      };

      setMessages((current) => [...current, assistantMessage]);
    } catch (error) {
      console.error("Training chat error:", error);

      setError(
        error instanceof TypeError
          ? "Could not connect to Reprez. Make sure the backend is running."
          : error instanceof Error
            ? error.message
            : "Something went wrong while talking to your AI Representative."
      );
    } finally {
      setSending(false);
    }
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key !== "Enter" || event.shiftKey) {
      return;
    }

    event.preventDefault();

    if (!sending && input.trim()) {
      event.currentTarget.form?.requestSubmit();
    }
  }

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#faf9f6]">
        <div className="text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-[#171717] text-xl font-bold text-white shadow-xl">
            R
          </div>

          <div className="mt-5 flex items-center justify-center gap-2">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#6d5dfc]" />
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#6d5dfc] [animation-delay:150ms]" />
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#6d5dfc] [animation-delay:300ms]" />
          </div>

          <p className="mt-3 text-sm text-black/45">
            Preparing your AI Representative...
          </p>
        </div>
      </main>
    );
  }

  if (error && !agent) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#faf9f6] px-6">
        <div className="w-full max-w-md rounded-[2rem] border border-black/5 bg-white p-8 text-center shadow-xl">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-red-50 text-xl font-bold text-red-600">
            !
          </div>

          <h1 className="mt-5 text-xl font-bold text-[#171717]">
            Something went wrong
          </h1>

          <p className="mt-2 text-sm leading-6 text-red-600">
            {error}
          </p>

          <button
            type="button"
            onClick={() => router.back()}
            className="mt-6 rounded-xl bg-[#171717] px-5 py-3 text-sm font-medium text-white transition hover:bg-black"
          >
            Go Back
          </button>
        </div>
      </main>
    );
  }

  if (!agent) {
    return null;
  }

  return (
    <main className="min-h-screen bg-[#faf9f6] text-[#171717]">
      {/* HEADER */}
      <header className="sticky top-0 z-30 border-b border-black/5 bg-white/90 backdrop-blur-xl">
        <div className="mx-auto flex h-[72px] max-w-[1400px] items-center justify-between px-5 lg:px-8">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#171717] text-sm font-bold text-white">
              R
            </div>

            <span className="text-lg font-bold tracking-tight">
              RepreZ<span className="text-[#6d5dfc]">.</span>
            </span>
          </div>

          {/* Center */}
          <div className="hidden items-center gap-3 md:flex">
            <div className="h-1.5 w-1.5 rounded-full bg-[#6d5dfc]" />

            <span className="text-sm font-medium text-black/55">
              Build your AI Representative
            </span>
          </div>

          {/* Right */}
          <div className="flex items-center gap-3">
            <div className="hidden text-right sm:block">
              <p className="text-xs font-semibold">{agent.business_name}</p>
              <p className="text-[10px] text-black/40">
                AI Representative
              </p>
            </div>

            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#eee9ff] text-xs font-bold text-[#6d5dfc]">
              {agent.business_name.charAt(0).toUpperCase()}
            </div>

            <div className="flex items-center gap-3">
       <button
          onClick={() => router.push(`/knowledge/${agentId}`)}
          className="rounded-xl border border-black/10 bg-white px-4 py-2 text-sm font-medium text-black/70 transition hover:bg-[#faf9f6] hover:text-black"
       >
      Review Knowledge
       </button>

            <button
              type="button"
              onClick={() => router.back()}
              disabled={sending}
              className="ml-1 rounded-xl border border-black/10 px-3.5 py-2 text-xs font-semibold text-black/55 transition hover:bg-black/[0.03] hover:text-black disabled:opacity-50"
            >
              Exit
            </button>
            </div>
          </div>
        </div>
      </header>

      {/* PAGE */}
      <div className="mx-auto max-w-[1400px] px-4 py-6 sm:px-6 lg:px-8">
        {/* PAGE TITLE */}
        <div className="mb-7">
          <div className="mb-3 flex items-center gap-2 text-xs font-medium text-black/40">
            <span>Setup</span>
            <span>/</span>
            <span className="text-[#6d5dfc]">Train AI</span>
          </div>

          <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
            <div>
              <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
                Teach your AI about {agent.business_name}
              </h1>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-black/50">
                Have a conversation with your AI Representative and give it
                the knowledge it needs to understand your business.
              </p>
            </div>

            <div className="flex items-center gap-2 rounded-full border border-black/5 bg-white px-3.5 py-2 shadow-sm">
              <span className="h-2 w-2 rounded-full bg-amber-400" />
              <span className="text-xs font-semibold text-black/55">
                Training in progress
              </span>
            </div>
          </div>
        </div>

        {/* WORKSPACE */}
        <div className="grid min-h-[calc(100vh-210px)] gap-5 lg:grid-cols-[230px_minmax(0,1fr)_250px]">
          {/* LEFT SIDEBAR */}
          <aside className="hidden lg:block">
            <div className="sticky top-[96px] space-y-4">
              {/* Progress */}
              <div className="rounded-3xl border border-black/5 bg-white p-5 shadow-[0_8px_30px_rgba(0,0,0,0.04)]">
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-black/35">
                  Setup
                </p>

                <div className="mt-5 space-y-4">
                  {/* Step 1 */}
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#171717] text-xs font-bold text-white">
                      ✓
                    </div>

                    <div>
                      <p className="text-xs font-semibold">
                        Create business
                      </p>
                      <p className="text-[10px] text-black/35">
                        Completed
                      </p>
                    </div>
                  </div>

                  <div className="ml-[15px] h-5 w-px bg-black/10" />

                  {/* Step 2 */}
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#6d5dfc] text-xs font-bold text-white shadow-lg shadow-[#6d5dfc]/20">
                      2
                    </div>

                    <div>
                      <p className="text-xs font-semibold">
                        Train AI
                      </p>
                      <p className="text-[10px] text-[#6d5dfc]">
                        In progress
                      </p>
                    </div>
                  </div>

                  <div className="ml-[15px] h-5 w-px bg-black/10" />

                  {/* Step 3 */}
                  <div className="flex items-center gap-3 opacity-45">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full border border-black/10 text-xs font-semibold">
                      3
                    </div>

                    <div>
                      <p className="text-xs font-semibold">
                        Review & launch
                      </p>
                      <p className="text-[10px] text-black/35">
                        Next
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Business */}
              <div className="rounded-3xl bg-[#171717] p-5 text-white">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white/10 text-sm">
                  ✦
                </div>

                <p className="mt-4 text-xs font-semibold text-white/45">
                  YOUR BUSINESS
                </p>

                <p className="mt-1 truncate text-sm font-semibold">
                  {agent.business_name}
                </p>

                <div className="mt-4 h-px bg-white/10" />

                <p className="mt-4 text-[11px] leading-5 text-white/45">
                  Everything you tell your AI here becomes part of its
                  business knowledge.
                </p>
              </div>
            </div>
          </aside>

          {/* CHATBOT */}
          <section className="flex min-h-[650px] min-w-0 flex-col overflow-hidden rounded-[2rem] border border-black/5 bg-white shadow-[0_20px_60px_rgba(0,0,0,0.06)]">
            {/* Chat top */}
            <div className="border-b border-black/5 px-5 py-5 sm:px-7">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="relative">
                    <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#171717] text-lg text-white">
                      ✦
                    </div>

                    <span className="absolute -bottom-1 -right-1 h-3 w-3 rounded-full border-2 border-white bg-green-500" />
                  </div>

                  <div>
                    <h2 className="text-sm font-bold">
                      Your AI Representative
                    </h2>

                    <p className="text-xs text-black/40">
                      Learning about {agent.business_name}
                    </p>
                  </div>
                </div>

                <div className="rounded-full bg-[#f4f1ff] px-3 py-1.5 text-[10px] font-semibold text-[#6d5dfc]">
                  LIVE TRAINING
                </div>
              </div>
            </div>

            {/* Messages */}
            <div
              className="min-h-0 flex-1 overflow-y-auto bg-[#fdfcfb] px-4 py-7 sm:px-7"
              aria-live="polite"
              aria-label="Training conversation"
            >
              <div className="mx-auto max-w-2xl space-y-6">
                {messages.map((message) => {
                  const isUser = message.role === "user";

                  return (
                    <div
                      key={message.id}
                      className={`flex ${
                        isUser ? "justify-end" : "justify-start"
                      }`}
                    >
                      <div
                        className={`flex max-w-[92%] gap-3 ${
                          isUser ? "flex-row-reverse" : ""
                        }`}
                      >
                        <div
                          className={`mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-xl text-[9px] font-bold ${
                            isUser
                              ? "bg-[#171717] text-white"
                              : "bg-[#eee9ff] text-[#6d5dfc]"
                          }`}
                        >
                          {isUser ? "YOU" : "✦"}
                        </div>

                        <div
                          className={`rounded-[1.25rem] px-4 py-3.5 text-sm leading-6 ${
                            isUser
                              ? "rounded-tr-md bg-[#171717] text-white shadow-md"
                              : "rounded-tl-md border border-black/5 bg-white text-black/65 shadow-sm"
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

                {sending && (
                  <div className="flex justify-start">
                    <div className="flex gap-3">
                      <div className="mt-1 flex h-8 w-8 items-center justify-center rounded-xl bg-[#eee9ff] text-xs text-[#6d5dfc]">
                        ✦
                      </div>

                      <div className="rounded-[1.25rem] rounded-tl-md border border-black/5 bg-white px-5 py-4 shadow-sm">
                        <div className="flex gap-1.5">
                          <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-black/25 [animation-delay:-0.3s]" />
                          <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-black/25 [animation-delay:-0.15s]" />
                          <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-black/25" />
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
              <div
                role="alert"
                className="mx-4 mb-3 flex items-start justify-between gap-3 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600"
              >
                <span>{error}</span>

                <button
                  type="button"
                  onClick={() => setError("")}
                  className="shrink-0 font-semibold text-red-500 hover:text-red-700"
                  aria-label="Dismiss error"
                >
                  ×
                </button>
              </div>
            )}

            {/* Input */}
            <div className="border-t border-black/5 bg-white p-3 sm:p-5">
              <form
                onSubmit={handleSubmit}
                className="mx-auto flex max-w-2xl items-end gap-2 rounded-2xl border border-black/10 bg-[#faf9f6] p-2 transition focus-within:border-[#b8adff] focus-within:bg-white focus-within:ring-4 focus-within:ring-[#6d5dfc]/5"
              >
                <textarea
                  ref={inputRef}
                  value={input}
                  onChange={(event) => {
                    setInput(event.target.value);

                    if (error) {
                      setError("");
                    }
                  }}
                  onKeyDown={handleKeyDown}
                  placeholder="Tell me about your business..."
                  rows={1}
                  maxLength={5000}
                  disabled={sending}
                  aria-label="Your message"
                  className="max-h-32 min-h-[48px] flex-1 resize-none bg-transparent px-3 py-3 text-sm text-[#171717] outline-none placeholder:text-black/30 disabled:cursor-not-allowed"
                />

                <button
                  type="submit"
                  disabled={sending || !input.trim()}
                  className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#171717] text-lg text-white shadow-md transition hover:-translate-y-0.5 hover:bg-black disabled:cursor-not-allowed disabled:opacity-30"
                  aria-label="Send message"
                >
                  {sending ? (
                    <span
                      aria-hidden="true"
                      className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"
                    />
                  ) : (
                    "↑"
                  )}
                </button>
              </form>

              <p className="mt-3 text-center text-[10px] text-black/30">
                Press Enter to send · Shift + Enter for a new line
              </p>
            </div>
          </section>

          {/* RIGHT SIDEBAR */}
          <aside className="hidden lg:block">
            <div className="sticky top-[96px] space-y-4">
              {/* Progress */}
              <div className="rounded-3xl border border-black/5 bg-white p-5 shadow-[0_8px_30px_rgba(0,0,0,0.04)]">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-semibold">
                    Training progress
                  </p>

                  <span className="text-sm font-bold text-[#6d5dfc]">
                    25%
                  </span>
                </div>

                <div className="mt-4 h-2 overflow-hidden rounded-full bg-black/5">
                  <div className="h-full w-1/4 rounded-full bg-[#6d5dfc]" />
                </div>

                <p className="mt-3 text-xs leading-5 text-black/40">
                  Keep teaching your AI about the business.
                </p>
              </div>

              {/* Topics */}
              <div className="rounded-3xl border border-black/5 bg-white p-5 shadow-[0_8px_30px_rgba(0,0,0,0.04)]">
                <p className="text-sm font-semibold">
                  Suggested topics
                </p>

                <div className="mt-4 space-y-2">
                  {[
                    "Business basics",
                    "Products & services",
                    "Hours & location",
                    "Policies",
                  ].map((topic) => (
                    <button
                      key={topic}
                      type="button"
                      onClick={() => setInput(topic)}
                      className="flex w-full items-center justify-between rounded-xl border border-black/5 bg-[#faf9f6] px-3 py-2.5 text-left text-xs font-medium text-black/55 transition hover:border-[#d8d0ff] hover:bg-[#faf8ff] hover:text-[#6d5dfc]"
                    >
                      <span>{topic}</span>
                      <span className="text-black/20">+</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Tip */}
              <div className="rounded-3xl bg-[#eee9ff] p-5">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-sm text-[#6d5dfc] shadow-sm">
                  ✦
                </div>

                <p className="mt-4 text-xs font-semibold text-[#171717]">
                  Knowledge note
                </p>

                <p className="mt-2 text-[11px] leading-5 text-black/50">
                  You don't need to write perfect instructions. Just explain
                  your business naturally and let your AI ask the questions.
                </p>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </main>
  );
}

