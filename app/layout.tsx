import type { Metadata } from "next";
import localFont from 'next/font/local'
import "./globals.css";



export const metadata: Metadata = {
  title: "pyngin",
  description: "A chess engine written in python",
};

const dogica = localFont({
  src: 'dogicapixel.ttf',
  variable: '--font-dogica', 
  display: 'swap',               
})

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={` ${dogica.variable} h-full antialiased bg-[#403241]`}
    >
      <body className="min-h-full flex flex-col font-dogica]">{children}</body>
    </html>
  );
}
