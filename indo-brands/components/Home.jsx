import React, { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function getStylePills(styleDesc, max = 3) {
    if (!styleDesc) return []
    return styleDesc
        .split(/[,.]/)
        .map(s => s.trim())
        .filter(Boolean)
        .slice(0, max)
}

function BrandCard({ brand }) {
    const pills = getStylePills(brand.style_desc)

    return (
        <li className="border-batik border-2 rounded-lg bg-white/90 p-4">
            <h3 className="font-david text-zinc-800 font-semibold text-xl">{brand.name}</h3>
            {pills.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mt-2">
                    {pills.map((p) => (
                        <span key={p} className="font-david text-sm bg-batik/12 text-zinc-600 rounded px-2 py-0.5">
                            {p}
                        </span>
                    ))}
                </div>
            )}
            {brand.instagram && (
                <a
                    href={brand.instagram}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-david text-batik hover:underline text-base mt-2 inline-block"
                >
                    View on Instagram →
                </a>
            )}
        </li>
    )
}

function Home() {
    const [query, setQuery] = useState('')
    const [results, setResults] = useState([])
    const [isLoading, setIsLoading] = useState(false)
    const [errorMessage, setErrorMessage] = useState('')

    async function handleRecommend() {
        const trimmed = query.trim()
        if (!trimmed) return
        setIsLoading(true)
        setErrorMessage('')
        setResults([])
        try {
            const res = await fetch(`${API_URL}/recommend`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: trimmed, top_k: 5 })
            })
            if (!res.ok) throw new Error('Recommendation failed')
            const data = await res.json()
            setResults(data.results || [])
        } catch (e) {
            setErrorMessage(e.message || 'Could not reach Gaya. Is the backend running?')
        } finally {
            setIsLoading(false)
        }
    }

    function handleKeyDown(e) {
        if (e.key === 'Enter') handleRecommend()
    }

    return (
        <div>
            <div className="flex mt-6 items-center justify-center sm:gap-20 gap-4">
                <img src="/rafflesia.png" alt="" className="sm:w-2xs w-24" />
                <h1 className="sm:text-9xl text-5xl font-title text-zinc-800 text-center">
                    Gaya
                </h1>
                <img src="/pura.png" alt="" className="sm:w-2xs w-24" />
            </div>
            <div className="flex mt-6 items-center justify-center sm:gap-20 gap-4">
                <img src="/melati.png" alt="" className="w-24 sm:w-2xs fixed left-4 top-1/2 transform -translate-y-1/2" />
                <div className="flex flex-col items-center">
                    <h2 className="font-david text-zinc-800 sm:text-4xl text-2xl text-center">
                        Discover Indonesia's local clothing brands by just chatting with Gaya
                    </h2>

                    <div className="border-batik border-2 mt-4 w-full max-w-2xl h-14 rounded-md flex items-center px-4">
                        <input
                            type="text"
                            placeholder="Describe your style to gaya..."
                            className="flex-grow bg-transparent outline-none text-zinc-800 text-lg font-david"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            onKeyDown={handleKeyDown}
                            disabled={isLoading}
                        />
                        <div className="flex space-x-3 ml-4">
                            <button type="button" className="focus:outline-none" aria-label="Upload Image">
                                <img src="/pict.png" alt="Upload" className="w-8 h-8" />
                            </button>
                            <button
                                type="button"
                                className="focus:outline-none disabled:opacity-50"
                                onClick={handleRecommend}
                                disabled={isLoading}
                                aria-label="Send"
                            >
                                <img src="/send.png" alt="Send" className="w-8 h-8" />
                            </button>
                        </div>
                    </div>

                    {isLoading && (
                        <p className="font-david text-zinc-700 mt-4">Gaya is thinking...</p>
                    )}
                    {errorMessage && (
                        <p className="font-david text-red-600 mt-4">{errorMessage}</p>
                    )}
                    {results.length > 0 && (
                        <ul className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 max-w-4xl">
                            {results.map((brand, i) => (
                                <BrandCard key={`${brand.name}-${i}`} brand={brand} />
                            ))}
                        </ul>
                    )}
                </div>
                <img src="/kupukupu.png" alt="" className="w-24 sm:w-2xs fixed right-4 bottom-4" />
            </div>
        </div>
    )
}

export default Home
