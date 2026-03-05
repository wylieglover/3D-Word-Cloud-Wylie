import type { AnalyzeResponse } from "../types"

const API_BASE_URL = "http://localhost:8000"

export async function analyzeArticle(url: string): Promise<AnalyzeResponse> {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url }),
  })

  if (!response.ok) {
    throw new Error(`Failed to analyze article: ${response.statusText}`)
  }

  return response.json()
}