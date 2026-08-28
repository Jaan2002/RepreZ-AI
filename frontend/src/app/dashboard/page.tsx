"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL;
type Agent = {
  id: number;
  business_name: string;
  status: string;
};

export default function Dashboard() {
    const [agent,setAgent] = useState<Agent | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() =>{
        async function fetchAgent(){
            try {
                const response = await fetch(`${API_URL}/agents/`);

                if(!response.ok){
                    throw new Error("Failed to fetch agent");
                }
                const data: Agent[] = await response.json();
                
                setAgent(data[0] ?? null);
            }catch (error){
                console.error("Failed to load agent:",error)
            }finally{
                setLoading(false)
            }
        }
        fetchAgent();
    }, []);

    if(loading){
        return <div className="p-8"> Loading Dashboard...</div>
    }
    if(!agent){
        return <div className="p-8">No AI Representative found.</div>
    }

  return (
    <main className="min-h-screen bg-gray-50">
      <nav className="flex items-center justify-between border-b bg-white px-8 py-5">
        <div>
          <h1 className="text-2xl font-bold">Reprez</h1>
          <p className="text-sm text-gray-500">
            AI Representative Platform
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-full bg-black text-center leading-9 text-white">
            G
          </div>

          <span className="font-medium">{agent.business_name}</span>
        </div>
      </nav>

      <section className="mx-auto max-w-7xl px-8 py-10">
        <div>
          <p className="text-sm font-medium text-gray-500">
            BUSINESS DASHBOARD
          </p>

          <h2 className="mt-2 text-3xl font-bold text-gray-900">
            Welcome back 👋
          </h2>

          <p className="mt-2 text-gray-600">
            Manage your AI Representative and business knowledge.
          </p>
        </div>

        <div className="mt-10 grid gap-6 md:grid-cols-3">
          {/* Merchant Brain */}

          <div className="rounded-xl border bg-white p-6 shadow-sm">
            <div className="text-3xl">🧠</div>

            <h3 className="mt-4 text-xl font-semibold">
              Merchant Brain
            </h3>

            <p className="mt-2 text-sm leading-6 text-gray-600">
              Your AI's source of truth. Manage your business information,
              products, services, prices and policies.
            </p>

            <Link href={`/knowledge/${agent.id}`} className="mt-6 rounded-lg border px-4 py-2 text-sm font-medium hover:bg-gray-50">
              Manage Knowledge
            </Link>
          </div>

          {/* AI Representative */}

          <div className="rounded-xl border bg-white p-6 shadow-sm">
            <div className="text-3xl">🤖</div>

            <h3 className="mt-4 text-xl font-semibold">
              AI Representative
            </h3>

            <div className="mt-3 flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-green-500" />
              <span className="text-sm text-green-600">
                Active
              </span>
            </div>

            <p className="mt-3 text-sm leading-6 text-gray-600">
              Your AI Representative can answer customer questions and
              understand your business.
            </p>

            <Link href={`/representative/${agent.id}`} className="mt-6 rounded-lg bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800">
              Open Representative
            </Link>
          </div>

          {/* Analytics */}

          <div className="rounded-xl border bg-white p-6 shadow-sm">
            <div className="text-3xl">📊</div>

            <h3 className="mt-4 text-xl font-semibold">
              Analytics
            </h3>

            <p className="mt-2 text-sm leading-6 text-gray-600">
              See how customers interact with your AI Representative.
            </p>

            <div className="mt-6 grid grid-cols-2 gap-4">
              <div>
                <p className="text-2xl font-bold">0</p>
                <p className="text-xs text-gray-500">
                  Conversations
                </p>
              </div>

              <div>
                <p className="text-2xl font-bold">₹0</p>
                <p className="text-xs text-gray-500">
                  Revenue
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* AI Representative preview */}

        <div className="mt-8 rounded-xl border bg-white p-8 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">
                YOUR REPRESENTATIVE
              </p>

              <h3 className="mt-2 text-2xl font-bold">
                {agent.business_name} AI Representative
              </h3>

              <p className="mt-2 text-gray-600">
                Your business's official AI interface.
              </p>
            </div>

            <div className="rounded-lg bg-gray-100 px-4 py-2 text-sm">
              Agent ID: {agent.id}
            </div>
          </div>

          <div className="mt-8 grid gap-4 md:grid-cols-4">
            <div className="rounded-lg bg-gray-50 p-4">
              <p className="text-sm text-gray-500">
                Business
              </p>

              <p className="mt-1 font-semibold">
                {agent.business_name}
              </p>
            </div>

            <div className="rounded-lg bg-gray-50 p-4">
              <p className="text-sm text-gray-500">
                Location
              </p>

              <p className="mt-1 font-semibold">
                -
              </p>
            </div>

            <div className="rounded-lg bg-gray-50 p-4">
              <p className="text-sm text-gray-500">
                Conversations
              </p>

              <p className="mt-1 font-semibold">
                0
              </p>
            </div>

            <div className="rounded-lg bg-gray-50 p-4">
              <p className="text-sm text-gray-500">
                Status
              </p>

              <p className="mt-1 font-semibold text-green-600">
                {agent.status}
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}