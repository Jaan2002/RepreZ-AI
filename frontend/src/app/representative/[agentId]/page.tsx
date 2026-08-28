"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

type Message = {
  role: "user" | "assistant";
  content: string;
};

type Agent = {
  id: number;
  business_name: string;
  status: string;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function RepresentativePage() {
  const params = useParams();
  const agentId = params.agentId as string;

  const [agent, setAgent] = useState<Agent | null>(null);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!agentId) return;

    const startRepresentative = async () => {
      try {
        setLoading(true);
        setError(false);

        // 1. Get agent information
        const agentResponse = await fetch(
          `${API_URL}/agents/${agentId}`
        );

        if (!agentResponse.ok) {
          throw new Error("Failed to fetch agent");
        }

        const agentData: Agent = await agentResponse.json();

        setAgent(agentData);

        // 2. Create a new customer session
        const sessionResponse = await fetch(
          `${API_URL}/customer/agents/${agentId}/session`,
          {
            method: "POST",
          }
        );

        if (!sessionResponse.ok) {
          throw new Error("Failed to create session");
        }

        const sessionData = await sessionResponse.json();

        setSessionId(sessionData.id);

        // 3. Initial AI message
        setMessages([
          {
            role: "assistant",
            content: `Hi! I'm the AI Representative for ${agentData.business_name}. How can I help you?`,
          },
        ]);
      } catch (error) {
        console.error("Failed to start representative:", error);

        setError(true);

        setMessages([
          {
            role: "assistant",
            content:
              "Sorry, I couldn't start the AI Representative. Please try again.",
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    startRepresentative();
  }, [agentId]);

  const sendMessage = async () => {
    if (!input.trim() || sessionId === null || sending) {
      return;
    }

    const userMessage = input.trim();

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setInput("");
    setSending(true);

    try {
      const response = await fetch(
        `${API_URL}/customer/${agentId}/chat?message=${encodeURIComponent(
          userMessage
        )}&session_id=${sessionId}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to get AI response");
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.reply,
        },
      ]);
    } catch (error) {
      console.error("Chat error:", error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setSending(false);
    }
  };

  if (!agent && loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-gray-50">
        <p className="text-gray-500">
          Starting AI Representative...
        </p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-6 py-4">
          <div>
            <p className="text-sm text-gray-500">
              REPREZ
            </p>

            <h1 className="text-xl font-bold">
              {agent?.business_name ?? "AI Representative"} AI Representative
            </h1>
          </div>

          <div className="rounded-full bg-green-100 px-3 py-1 text-sm text-green-700">
            ● Active
          </div>
        </div>
      </header>

      <section className="mx-auto flex min-h-[calc(100vh-73px)] max-w-4xl flex-col px-6 py-6">
        <div className="mb-4 flex items-center justify-between text-sm text-gray-500">
          <span>
            {loading
              ? "Starting conversation..."
              : error
                ? "Unable to start"
                : `Session ID: ${sessionId}`}
          </span>

          {agent && (
            <span>
              Agent ID: {agent.id}
            </span>
          )}
        </div>

        <div className="flex-1 space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === "user"
                  ? "justify-end"
                  : "justify-start"
              }`}
            >
              <div
                className={`max-w-[75%] rounded-2xl px-4 py-3 ${
                  message.role === "user"
                    ? "bg-black text-white"
                    : "border bg-white text-gray-800"
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}

          {sending && (
            <div className="flex justify-start">
              <div className="rounded-2xl border bg-white px-4 py-3 text-gray-500">
                Reprez is thinking...
              </div>
            </div>
          )}
        </div>

        <div className="mt-6 flex gap-3 border-t pt-4">
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                sendMessage();
              }
            }}
            placeholder={
              agent
                ? `Ask ${agent.business_name} anything...`
                : "Ask anything..."
            }
            disabled={loading || sending || sessionId === null}
            className="flex-1 rounded-xl border bg-white px-4 py-3 outline-none focus:ring-2 focus:ring-gray-300"
          />

          <button
            onClick={sendMessage}
            disabled={
              loading ||
              sending ||
              sessionId === null ||
              !input.trim()
            }
            className="rounded-xl bg-black px-6 py-3 font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </section>
    </main>
  );
}