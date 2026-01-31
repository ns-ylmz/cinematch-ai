import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Arama hatası:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8 font-sans">
      {/* Header */}
      <header className="max-w-4xl mx-auto text-center mb-12">
        <h1 className="text-5xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-600 mb-4">
          Gemini Movie AI
        </h1>
        <p className="text-slate-400">DeepSeek destekli akıllı film keşif asistanı</p>
      </header>

      {/* Search Bar */}
      <div className="max-w-2xl mx-auto mb-12">
        <form onSubmit={handleSearch} className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ne tür bir film arıyorsun? (Örn: Crime and Power)"
            className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-cyan-600 hover:bg-cyan-500 disabled:bg-slate-700 px-6 py-3 rounded-lg font-bold transition-all"
          >
            {loading ? 'Düşünüyor...' : 'Ara'}
          </button>
        </form>
      </div>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
        {results && (
          <>
            {/* AI Analysis Section */}
            <div className="bg-slate-800/50 border border-slate-700 rounded-2xl p-6 h-fit">
              <h2 className="text-xl font-bold text-cyan-400 mb-4 flex items-center gap-2">
                <span className="animate-pulse">🤖</span> AI Analizi
              </h2>
              <div className="prose prose-invert max-w-none text-slate-300 whitespace-pre-wrap leading-relaxed">
                {results.recommended_movies}
              </div>
            </div>

            {/* Raw Results Section */}
            <div className="space-y-4">
              <h2 className="text-xl font-bold text-slate-400 mb-4">Eşleşen Filmler (Vector DB)</h2>
              {results.raw_data_source.map((movie, index) => (
                <div key={index} className="bg-slate-800 border border-slate-700 p-4 rounded-xl hover:border-cyan-500/50 transition-all group">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-lg font-bold group-hover:text-cyan-400">{movie.title}</h3>
                    <span className="bg-cyan-900/50 text-cyan-400 text-xs px-2 py-1 rounded">⭐ {movie.vote_average}</span>
                  </div>
                  <p className="text-sm text-slate-500">Yayın Yılı: {movie.release_date}</p>
                </div>
              ))}
            </div>
          </>
        )}
      </main>

      {/* Empty State / Loading */}
      {!results && !loading && (
        <div className="text-center text-slate-600 mt-20">
          <p>Henüz bir arama yapmadın. DeepSeek senin için hazır!</p>
        </div>
      )}
    </div>
  );
}

export default App;