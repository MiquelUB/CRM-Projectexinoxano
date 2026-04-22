import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CRM Projecte Xino Xano",
  description: "B2G CRM per Projecte Xino Xano",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ca">
      <body className="font-sans">{children}</body>
    </html>
  );
}
