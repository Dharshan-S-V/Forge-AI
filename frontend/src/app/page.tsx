import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="px-4 lg:px-6 h-14 flex items-center border-b">
        <Link className="flex items-center justify-center font-bold text-xl" href="/">
          ForgeAI
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link href="/login">
            <Button variant="ghost">Login</Button>
          </Link>
          <Link href="/register">
            <Button>Get Started</Button>
          </Link>
        </nav>
      </header>
      <main className="flex-1 flex items-center justify-center">
        <div className="container px-4 md:px-6 text-center space-y-8">
          <div className="space-y-4">
            <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
              Enterprise AI Operations <span className="text-primary">Copilot</span>
            </h1>
            <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400">
              Upload documents and interact with your company's knowledge securely using RAG-powered AI. No hallucinations.
            </p>
          </div>
          <div className="space-x-4">
            <Link href="/register">
              <Button size="lg" className="h-12 px-8 text-lg">
                Start Building
              </Button>
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
