"use client"; 
import { useState } from "react";
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

  interface PieceDropHandlerArgs {
    piece: string;
    sourceSquare: string;
    targetSquare: string;
  }

  function onDrop({ piece, sourceSquare, targetSquare }: any) {
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
 const chessboardOptions = {
    id: 'pyngin-board',
    position: position,
    onPieceDrop: onDrop,
    pieces: customPieces,                              
    darkSquareStyle: { backgroundColor: "#784F48" },   
    lightSquareStyle: { backgroundColor: "#E2D5A1" }   
  };

  return (
    <div className="min-h-screen w-screen font-dogica bg-[#403241] text-white">
      <main className="grid w-full min-h-screen h-full grid-cols-2 p-12 gap-8 items-center">
        
        <div className="w-full max-w-[500px] aspect-square justify-self-end shadow-2xl rounded overflow-hidden">
          <Chessboard options={chessboardOptions} />
        </div>

        <div className="w-full h-full flex flex-col justify-center p-6">
          <h1 className="text-3xl font-dogica">Depth</h1>
        </div>

      </main>
    </div>
  );
}