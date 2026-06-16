"use client"; 
import { useEffect, useRef, useState } from "react";
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js'; 

const DARK_PIECE_COLUMNS: Record<string, number> = {
  'bP': 0, 'bN': 1, 'bR': 2, 'bB': 3, 'bQ': 5, 'bK': 4
};

const WHITE_PIECE_COLUMNS: Record<string, number> = {
  'wP': 0, 'wN': 1, 'wR': 2, 'wB': 3, 'wQ': 5, 'wK': 4
};

export default function Home() {
  const [game, setGame] = useState(new Chess());
  const [position, setPosition] = useState(game.fen());
  const [thinking, setThinking] = useState(false);
  const [playas, setPlayas] = useState('w');
  const [enginestat, setEnginestat] = useState('Starting Engine...')
  const [engineready, setEngeready] = useState(false)
  const workerRef = useRef<Worker | null>(null)
  const [depth, setdepth] = useState<1 | 2 | 3 | 4 | 5>(4)

  const customPieces: Record<string, any> = {};


  Object.keys(DARK_PIECE_COLUMNS).forEach((piece) => {
    const colIndex = DARK_PIECE_COLUMNS[piece];
    customPieces[piece] = () => (
      <div
        style={{
          width: '100%',
          aspectRatio: 1,
          backgroundImage: `url('/pieces/d_pieces.png')`,
          backgroundRepeat: "no-repeat",
          backgroundSize: `600% 100%`,
          backgroundPosition: `${colIndex/5*100}% 0px`,
          transform: 'scale(0.75)',
          transformOrigin:'center',
          imageRendering: 'pixelated'
        }}
      />
    );
  });

  Object.keys(WHITE_PIECE_COLUMNS).forEach((piece) => {
    const colIndex = WHITE_PIECE_COLUMNS[piece];
    customPieces[piece] = () => (
      <div
        style={{
          width: '100%',
          aspectRatio: 1,
          backgroundImage: `url('/pieces/w_pieces.png')`,
          backgroundRepeat: "no-repeat",
          backgroundSize: `600% 100%`,
          backgroundPosition: `${colIndex/5*100}% 0px`,
          transform: 'scale(0.75)',
          transformOrigin:'center',
          imageRendering: 'pixelated'
        }}
      />
    );
  });

  useEffect(() => {
    const worker = new Worker("/engine.worker.js");
    workerRef.current = worker;

    worker.onmessage = (e) => {
      const { type, data } = e.data
      if (type === 'status') {
        setEnginestat(data)
      }
      else if (type === "ready") {
        setEngeready(true)
        setEnginestat("Your Turn")
      } else if (type === "move") {
        if (data) {
          game.move(data);
          setPosition(game.fen());
        }
        setThinking(false);
        setEnginestat("Your Turn");
      } else if (type === "error") {
        console.error("Worker Engine Error:", data);
        setThinking(false);
        setEnginestat("Engine Error");
      }
    }
    return () => worker.terminate();
  }, [game])

  useEffect(() => {
    if (game.turn() !== playas && !game.isGameOver() && engineready) {
      setThinking(true)
      setEnginestat("Engine Thinking...")
      workerRef.current?.postMessage({
        type: 'search',
        fen: position,
        depth: depth,
      })
    }
  }, [position, game, engineready])

  function onPieceDrop({sourceSquare, targetSquare, piece}: any) {
    if (thinking || !engineready || game.isGameOver() || game.turn() !== playas) return false;
    try {
      const move = game.move({
        from: sourceSquare,
        to: targetSquare,
        promotion: "q",
      });

      if (move === null) return false;

      setPosition(game.fen()); 
      return true;
    } catch (error) {
      return false; 
    }
  }

  const chessboardOptions: any = {
    onPieceDrop,
    id: 'pyngin-board',
    position: position,
    pieces: customPieces,
    darkSquareStyle: { backgroundColor: "#784F48" },
    lightSquareStyle: { backgroundColor: "#E2D5A1" }
  };

  const _history = game.history()
  const m_pairs = []
  for (let i = 0; i < _history.length; i += 2) {
  m_pairs.push({
      turn: Math.floor(i / 2) + 1,
      w: _history[i],
      b: _history[i+1] || "*",
  });}


  return (
  <div className="min-h-screen w-full font-dogica bg-[#403241] text-white">
  <main className="min-h-screen grid w-full md:grid-cols-2 p-4 md:p-12 gap-8 items-center">
    <div className="flex flex-col gap-3 w-full max-w-[480px] mx-auto md:ml-auto md:mr-0">
      <div className="flex w-full items-center justify-between">
        <span className="text-sm text-[#E2D5A1]">{enginestat}</span>
        <span className={`text-xs transition-opacity duration-300 ${thinking ? "opacity-100 animate-pulse" : "opacity-0"}`}>
          thinking...
        </span>
      </div>
      <div className="w-full aspect-square">
        <Chessboard options={chessboardOptions} />
      </div>
      <p className="text-xs text-white/40">
        artwork by{" "}
        <a href="https://dani-maccari.itch.io/" className="text-[#E2D5A1] hover:text-[#784F48] transition-colors">
          Dani Maccari
        </a>
      </p>
    </div>

    <div className="flex flex-col gap-6 w-full max-w-[400px] mx-auto md:mx-0">
      <div className="flex items-center gap-6">
        <span className="text-sm shrink-0">Depth</span>
        <div className="flex flex-col gap-1 w-full">
          <input
            type="range"
            step={1} min={1} max={5}
            value={depth}
            onChange={(e) => setdepth(Number(e.target.value) as typeof depth)}
            className="sliderr"
          />
          <div className="flex justify-between px-2">
            {[1, 2, 3, 4, 5].map((n) => (
              <span key={n} className="text-xs text-[#E2D5A1]">{n}</span>
            ))}
          </div>
        </div>
      </div>

      <div className="w-full h-64 overflow-y-auto bg-[#784F48] border-2 border-[#E2D5A1] p-2 flex flex-col gap-0.5">
        {m_pairs.map((pair) => (
          <div key={pair.turn} className="flex gap-2 text-sm">
            <span className="text-[#E2D5A1]/60 w-6 shrink-0">{pair.turn}.</span>
            <span>{pair.w}</span>
            <span className="text-[#E2D5A1]/50">—</span>
            <span>{pair.b}</span>
          </div>
        ))}
      </div>

      <button
        onClick={() => navigator.clipboard.writeText(game.pgn())}
        className="w-fit bg-[#E2D5A1] px-4 py-3 text-sm text-[#784F48] cursor-pointer hover:bg-white active:scale-[0.99] transition-all"
      >
        copy PGN
      </button>

    </div>
  </main>
</div>
  );
}