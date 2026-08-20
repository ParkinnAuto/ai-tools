import "./globals.css";

export const metadata = {
  title: "AI Robot Assistant",
  description: "AI Robot Voice Assistant",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}