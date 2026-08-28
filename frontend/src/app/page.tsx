import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      <nav className="flex items-center justify-between border-b bg-white px-8 py-5">
        <h1 className="text-2xl font-bold">Reprez</h1>

        <span className="text-sm text-gray-500">
          AI Representative Platform
        </span>
      </nav>

      <section className="mx-auto max-w-6xl px-8 py-20">
        <div className="max-w-3xl">
          <p className="mb-4 text-sm font-semibold uppercase tracking-wider text-gray-500">
            AI Representative
          </p>

          <h2 className="text-5xl font-bold tracking-tight text-gray-900">
            Make your business ready for the AI economy.
          </h2>

          <p className="mt-6 text-lg leading-8 text-gray-600">
            Reprez gives your business an AI Representative that understands
            your products, talks to customers, recommends products, and can
            safely help complete transactions.
          </p>

          <div className="mt-8 flex gap-4">
            <Link  href="/dashboard" className="rounded-lg bg-black px-6 py-3 font-medium text-white hover:bg-gray-800">
              Create AI Representative
            </Link>

            <Link href="/dashboard" className="rounded-lg border border-gray-300 bg-white px-6 py-3 font-medium text-gray-700 hover:bg-gray-100">
              View Demo
            </Link>
          </div>
        </div>

        <div className="mt-20 grid gap-6 md:grid-cols-3">
          <div className="rounded-xl border bg-white p-6">
            <h3 className="text-xl font-semibold">🧠 Merchant Brain</h3>
            <p className="mt-3 text-gray-600">
              Give your AI accurate business knowledge, products, prices and
              policies.
            </p>
          </div>

          <div className="rounded-xl border bg-white p-6">
            <h3 className="text-xl font-semibold">🤖 AI Representative</h3>
            <p className="mt-3 text-gray-600">
              Let customers interact naturally with your business through AI.
            </p>
          </div>

          <div className="rounded-xl border bg-white p-6">
            <h3 className="text-xl font-semibold">💳 AI Commerce</h3>
            <p className="mt-3 text-gray-600">
              Move from conversation to cart and eventually secure payment.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}