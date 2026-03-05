import { useState } from "react"

const SAMPLE_URLS = [
  "https://www.bbc.com/news/live/c62gg44d53xt",
  "https://www.theguardian.com/wellness/2026/mar/05/michael-pollan-book-a-world-appears-consciousness-hygiene",
  "https://www.cnn.com/2026/03/05/entertainment/britney-spears-arrest",
]

interface UrlInputProps {
  onSubmit: (url: string) => void
  isLoading: boolean
}

export default function UrlInput({ onSubmit, isLoading }: UrlInputProps) {
  const [url, setUrl] = useState("") // Start empty for a cleaner initial look

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault()
    if (url.trim()) onSubmit(url.trim())
  }

  return (
    <div className="flex flex-col items-center gap-6 w-full max-w-2xl px-4 z-10">
      <form 
        onSubmit={handleSubmit}
        className="group relative flex w-full items-center"
      >
        {/* Animated Glow Backdrop */}
        <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-pink-500 rounded-2xl blur opacity-20 group-focus-within:opacity-40 transition duration-1000"></div>
        
        <div className="relative flex w-full bg-black/40 backdrop-blur-xl rounded-xl border border-white/10 p-1.5 shadow-2xl">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Paste an article link..."
            className="flex-1 bg-transparent px-4 py-3 text-white placeholder-white/30 outline-none text-sm"
          />
          
          <button
            type="submit"
            disabled={isLoading || !url.trim()}
            className="px-6 py-2 rounded-lg bg-white text-black text-sm font-semibold hover:bg-indigo-50 active:scale-95 disabled:opacity-0 disabled:pointer-events-none transition-all duration-300"
          >
            {isLoading ? "..." : "Analyze"}
          </button>
        </div>
      </form>

      {/* Modern Sample Pills */}
      <div className="flex items-center gap-3 animate-fade-in">
        <span className="text-[10px] uppercase tracking-widest text-white/30 font-bold">Try:</span>
        <div className="flex gap-2">
          {SAMPLE_URLS.map((sample, i) => (
            <button
              key={i}
              onClick={() => {
                setUrl(sample)
              }}
              className="px-3 py-1 rounded-full border border-white/5 bg-white/5 text-[11px] text-white/50 hover:text-white hover:bg-white/10 hover:border-white/20 transition-all"
            >
              Link {i + 1}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}