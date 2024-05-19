'use client';

import { Inter } from "next/font/google";
import "./globals.css";
import {Providers} from "./providers";
import {ToastContainer} from 'react-toastify';
import NavigationBar from "@/components/global/Navigationbar";


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
          <ToastContainer/>
          <NavigationBar/>
          {children}
        </Providers>
      </body>
    </html>
  );
}
