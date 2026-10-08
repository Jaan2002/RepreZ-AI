
"use client";

import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#faf9f6] text-[#171717]">
      {/* Navbar */}
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-10">
        <Link href="/" className="text-2xl font-bold tracking-tight">
          RepreZ<span className="text-[#6d5dfc]">.</span>
        </Link>

        <div className="hidden items-center gap-8 text-sm font-medium md:flex">
          <a href="#how-it-works" className="transition hover:opacity-60">
            How it works
          </a>
          <a href="#features" className="transition hover:opacity-60">
            Features
          </a>
          <a href="#for-business" className="transition hover:opacity-60">
            For businesses
          </a>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className="hidden rounded-full px-5 py-2.5 text-sm font-medium transition hover:bg-black/5 sm:block"
          >
            Log in
          </Link>

          <Link
            href="/signup"
            className="rounded-full bg-[#171717] px-5 py-2.5 text-sm font-medium text-white transition hover:scale-[1.02] hover:bg-black"
          >
            Get started
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="mx-auto max-w-7xl px-6 pb-24 pt-16 lg:px-10 lg:pb-32 lg:pt-24">
        <div className="grid items-center gap-16 lg:grid-cols-2">
          <div>
            <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium shadow-sm">
              <span className="h-2 w-2 rounded-full bg-[#6d5dfc]" />
              Your business, represented by AI
            </div>

            <h1 className="max-w-3xl text-5xl font-bold leading-[1.05] tracking-[-0.04em] sm:text-6xl lg:text-7xl">
              Give your business an
              <span className="text-[#6d5dfc]"> AI Representative.</span>
            </h1>

            <p className="mt-7 max-w-xl text-lg leading-8 text-black/60">
              Create an AI that learns about your business, understands your
              knowledge, and helps customers whenever they need you.
            </p>

            <div className="mt-9 flex flex-col gap-3 sm:flex-row">
              <Link
                href="/agents/create"
                className="rounded-full bg-[#171717] px-7 py-4 text-center text-sm font-semibold text-white transition hover:-translate-y-0.5"
              >
                Create your AI Representative →
              </Link>

              <a
                href="#how-it-works"
                className="rounded-full border border-black/10 bg-white px-7 py-4 text-center text-sm font-semibold transition hover:bg-black/[0.03]"
              >
                See how it works
              </a>
            </div>

            <p className="mt-5 text-sm text-black/40">
              No complicated setup. Teach it. Review it. Make it live.
            </p>
          </div>

          {/* AI Representative Card */}
          <div className="relative">
            <div className="absolute -inset-8 rounded-[3rem] bg-[#6d5dfc]/10 blur-3xl" />

            <div className="relative overflow-hidden rounded-[2rem] border border-black/10 bg-white p-5 shadow-[0_30px_80px_rgba(0,0,0,0.08)]">
              <div className="rounded-[1.5rem] bg-[#f5f3ff] p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs font-medium uppercase tracking-widest text-black/40">
                      AI Representative
                    </p>
                    <h2 className="mt-1 text-2xl font-bold">
                      Aroma Cafe
                    </h2>
                  </div>

                  <div className="flex items-center gap-2 rounded-full bg-white px-3 py-1.5 text-xs font-medium shadow-sm">
                    <span className="h-2 w-2 rounded-full bg-green-500" />
                    Live
                  </div>
                </div>

                <div className="mt-8 space-y-4">
                  <div className="max-w-[85%] rounded-2xl rounded-tl-md bg-white p-4 shadow-sm">
                    <p className="text-xs font-medium text-black/40">
                      Customer
                    </p>
                    <p className="mt-1 text-sm leading-6">
                      What time do you close today?
                    </p>
                  </div>

                  <div className="ml-auto max-w-[85%] rounded-2xl rounded-tr-md bg-[#171717] p-4 text-white shadow-sm">
                    <p className="text-xs font-medium text-white/50">
                      Aroma Cafe AI
                    </p>
                    <p className="mt-1 text-sm leading-6">
                      We’re open until 10:00 PM today. Would you like to know
                      our menu or today’s specials?
                    </p>
                  </div>

                  <div className="max-w-[85%] rounded-2xl rounded-tl-md bg-white p-4 shadow-sm">
                    <p className="text-xs font-medium text-black/40">
                      Customer
                    </p>
                    <p className="mt-1 text-sm leading-6">
                      Yes, show me the specials.
                    </p>
                  </div>
                </div>

                <div className="mt-6 flex items-center gap-3 rounded-xl border border-black/5 bg-white px-4 py-3">
                  <div className="h-2 w-2 rounded-full bg-[#6d5dfc]" />
                  <span className="text-sm text-black/40">
                    AI is responding...
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Trust statement */}
      <section className="border-y border-black/5 bg-white">
        <div className="mx-auto max-w-5xl px-6 py-10 text-center">
          <p className="text-sm font-medium uppercase tracking-[0.2em] text-black/30">
            Built for businesses that want to be available beyond business
            hours
          </p>
        </div>
      </section>

      {/* How it works */}
      <section
        id="how-it-works"
        className="mx-auto max-w-7xl px-6 py-24 lg:px-10 lg:py-32"
      >
        <div className="max-w-2xl">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-[#6d5dfc]">
            How it works
          </p>

          <h2 className="mt-4 text-4xl font-bold tracking-[-0.03em] sm:text-5xl">
            From business knowledge to customer conversations.
          </h2>

          <p className="mt-5 text-lg leading-8 text-black/55">
            RepreZ gives you control over what your AI Representative knows
            before you put it in front of customers.
          </p>
        </div>

        <div className="mt-16 grid gap-5 md:grid-cols-4">
          {[
            {
              number: "01",
              title: "Create",
              text: "Create your business and give your AI Representative an identity.",
            },
            {
              number: "02",
              title: "Teach",
              text: "Provide information about your business, services, products, and policies.",
            },
            {
              number: "03",
              title: "Review",
              text: "See what your AI knows. Edit or remove anything before going live.",
            },
            {
              number: "04",
              title: "Go Live",
              text: "Let customers interact with your AI Representative through chat.",
            },
          ].map((step) => (
            <div
              key={step.number}
              className="rounded-3xl border border-black/10 bg-white p-7"
            >
              <span className="text-sm font-semibold text-[#6d5dfc]">
                {step.number}
              </span>

              <h3 className="mt-8 text-xl font-bold">{step.title}</h3>

              <p className="mt-3 text-sm leading-6 text-black/55">
                {step.text}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section id="features" className="bg-[#171717] text-white">
        <div className="mx-auto max-w-7xl px-6 py-24 lg:px-10 lg:py-32">
          <div className="max-w-2xl">
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-[#a99fff]">
              One workspace
            </p>

            <h2 className="mt-4 text-4xl font-bold tracking-[-0.03em] sm:text-5xl">
              Everything you need to manage your AI Representative.
            </h2>
          </div>

          <div className="mt-16 grid gap-5 md:grid-cols-3">
            <FeatureCard
              icon="✦"
              title="Train AI"
              text="Teach your representative about your business using information that actually matters."
            />

            <FeatureCard
              icon="◈"
              title="Manage Knowledge"
              text="Review, edit, add, and delete the information your AI uses when talking to customers."
            />

            <FeatureCard
              icon="◉"
              title="Test Customer Chat"
              text="Have conversations with your AI before making it available to real customers."
            />
          </div>
        </div>
      </section>

      {/* For businesses */}
      <section
        id="for-business"
        className="mx-auto max-w-7xl px-6 py-24 lg:px-10 lg:py-32"
      >
        <div className="rounded-[2rem] bg-[#f0edff] px-7 py-14 text-center sm:px-12 lg:px-20 lg:py-20">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-[#6d5dfc]">
            Your AI. Your knowledge. Your control.
          </p>

          <h2 className="mx-auto mt-5 max-w-3xl text-4xl font-bold tracking-[-0.04em] sm:text-5xl">
            Build a representative your customers can actually rely on.
          </h2>

          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-black/55">
            Don't just give an AI access to your business. Teach it what it
            should know, review what it learned, and decide when it's ready.
          </p>

          <Link
            href="/signup"
            className="mt-9 inline-flex rounded-full bg-[#171717] px-8 py-4 text-sm font-semibold text-white transition hover:-translate-y-0.5"
          >
            Create your AI Representative →
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-black/5 bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-8 text-sm text-black/45 sm:flex-row sm:items-center sm:justify-between lg:px-10">
          <p>
            © {new Date().getFullYear()} RepreZ. Your business, represented by
            AI.
          </p>

          <div className="flex gap-6">
            <Link href="/login" className="hover:text-black">
              Log in
            </Link>
            <Link href="/signup" className="hover:text-black">
              Get started
            </Link>
          </div>
        </div>
      </footer>
    </main>
  );
}

function FeatureCard({
  icon,
  title,
  text,
}: {
  icon: string;
  title: string;
  text: string;
}) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-7">
      <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/10 text-xl">
        {icon}
      </div>

      <h3 className="mt-8 text-xl font-bold">{title}</h3>

      <p className="mt-3 text-sm leading-6 text-white/55">{text}</p>
    </div>
  );
}
