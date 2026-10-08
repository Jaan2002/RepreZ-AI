
"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";

export default function SignupPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [agree, setAgree] = useState(false);

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Authentication will be connected later.
    console.log("Signup:", {
      name,
      email,
      password,
    });
  };

  return (
    <main className="min-h-screen bg-[#faf9f6] text-[#171717]">
      {/* Header */}
      <header className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-10">
        <Link href="/" className="text-2xl font-bold tracking-tight">
          RepreZ<span className="text-[#6d5dfc]">.</span>
        </Link>

        <p className="text-sm text-black/50">
          Already have an account?{" "}
          <Link
            href="/login"
            className="font-semibold text-[#171717] hover:underline"
          >
            Log in
          </Link>
        </p>
      </header>

      {/* Signup */}
      <section className="flex min-h-[calc(100vh-90px)] items-center justify-center px-6 py-12">
        <div className="w-full max-w-md">
          {/* Heading */}
          <div className="text-center">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-[#f0edff] text-2xl">
              ✦
            </div>

            <h1 className="mt-7 text-4xl font-bold tracking-[-0.03em]">
              Create your account
            </h1>

            <p className="mt-3 text-sm leading-6 text-black/50">
              Start building your AI Representative.
            </p>
          </div>

          {/* Card */}
          <div className="mt-9 rounded-[2rem] border border-black/10 bg-white p-7 shadow-[0_20px_60px_rgba(0,0,0,0.05)] sm:p-8">
            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Name */}
              <div>
                <label
                  htmlFor="name"
                  className="mb-2 block text-sm font-semibold"
                >
                  Your name
                </label>

                <input
                  id="name"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Your name"
                  autoComplete="name"
                  required
                  className="w-full rounded-xl border border-black/10 bg-[#faf9f6] px-4 py-3.5 text-sm outline-none transition placeholder:text-black/30 focus:border-[#6d5dfc] focus:ring-4 focus:ring-[#6d5dfc]/10"
                />
              </div>

              {/* Email */}
              <div>
                <label
                  htmlFor="email"
                  className="mb-2 block text-sm font-semibold"
                >
                  Email address
                </label>

                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@business.com"
                  autoComplete="email"
                  required
                  className="w-full rounded-xl border border-black/10 bg-[#faf9f6] px-4 py-3.5 text-sm outline-none transition placeholder:text-black/30 focus:border-[#6d5dfc] focus:ring-4 focus:ring-[#6d5dfc]/10"
                />
              </div>

              {/* Password */}
              <div>
                <label
                  htmlFor="password"
                  className="mb-2 block text-sm font-semibold"
                >
                  Password
                </label>

                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="At least 8 characters"
                  autoComplete="new-password"
                  minLength={8}
                  required
                  className="w-full rounded-xl border border-black/10 bg-[#faf9f6] px-4 py-3.5 text-sm outline-none transition placeholder:text-black/30 focus:border-[#6d5dfc] focus:ring-4 focus:ring-[#6d5dfc]/10"
                />

                <p className="mt-2 text-xs text-black/35">
                  Use at least 8 characters.
                </p>
              </div>

              {/* Terms */}
              <label className="flex cursor-pointer items-start gap-3 text-xs leading-5 text-black/50">
                <input
                  type="checkbox"
                  checked={agree}
                  onChange={(e) => setAgree(e.target.checked)}
                  required
                  className="mt-0.5 h-4 w-4 shrink-0 rounded border-black/20 accent-[#6d5dfc]"
                />

                <span>
                  I agree to the RepreZ terms and understand that I am
                  responsible for reviewing my AI Representative's knowledge
                  before making it live.
                </span>
              </label>

              {/* Submit */}
              <button
                type="submit"
                className="w-full rounded-xl bg-[#171717] px-5 py-3.5 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:bg-black disabled:cursor-not-allowed disabled:opacity-40"
                disabled={!agree}
              >
                Create account
              </button>
            </form>

            {/* Divider */}
            <div className="my-7 flex items-center gap-4">
              <div className="h-px flex-1 bg-black/10" />
              <span className="text-xs text-black/35">OR</span>
              <div className="h-px flex-1 bg-black/10" />
            </div>

            {/* Google */}
            <button
              type="button"
              className="flex w-full items-center justify-center gap-3 rounded-xl border border-black/10 bg-white px-5 py-3.5 text-sm font-semibold transition hover:bg-black/[0.02]"
            >
              <span className="text-base font-bold">G</span>
              Continue with Google
            </button>
          </div>

          {/* Login */}
          <p className="mt-7 text-center text-sm text-black/50">
            Already have an account?{" "}
            <Link
              href="/login"
              className="font-semibold text-[#171717] hover:underline"
            >
              Log in
            </Link>
          </p>
        </div>
      </section>
    </main>
  );
}

