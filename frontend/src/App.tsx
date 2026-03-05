import { useState } from "react"
import UrlInput from "./components/UrlInput"
import WordCloud from "./components/WordCloud"
import { analyzeArticle } from "./api/analyze"
import type { WordWeight } from "./types"

export default function App() {
  const [words, setWords] = useState<WordWeight[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (url: string) => {
    setIsLoading(true)
    setError(null)
    setWords([])

    try {
      const data = await analyzeArticle(url)
      setWords(data.words)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center w-screen h-screen bg-gray-950 text-white p-6 gap-6">
      <h1 className="text-2xl font-semibold tracking-[0.2em] uppercase text-white/70">
        3D Article Word Cloud
      </h1>
      <UrlInput onSubmit={handleSubmit} isLoading={isLoading} />
      {error && (
        <p className="text-red-400/70 text-xs tracking-wide">{error}</p>
      )}
      {words.length > 0 && (
        <div className="flex-1 w-full">
          <WordCloud words={words} />
        </div>
      )}
      {!isLoading && words.length === 0 && !error && (
        <p className="text-white/20 text-xs tracking-widest uppercase mt-8">
          Paste a news article URL above to generate a word cloud
        </p>
      )}
    </div>
  )
}