'use client';

import { Inter } from "next/font/google";
import "./globals.css";
import SideBar from "@/components/SideBar";
import {Providers} from "./providers";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={"dark"}>
      <body className={inter.className}>
        <Providers>
          <SideBar/>
          {children}
        </Providers>
      </body>
    </html>
  );
}
