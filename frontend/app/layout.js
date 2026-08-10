export const metadata = {
  title: "Multi-Cloud Free-Tier Platform",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "system-ui, sans-serif", margin: 0, background: "#0b0f14", color: "#e6edf3" }}>
        {children}
      </body>
    </html>
  );
}
