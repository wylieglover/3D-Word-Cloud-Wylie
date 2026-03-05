export interface WordWeight {
  word: string
  weight: number
}

export interface AnalyzeResponse {
  words: WordWeight[]
}