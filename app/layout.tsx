import './globals.css'
export const metadata = {
  title: 'Penguin-NEO',
  description: 'Penguin powered by NeoMoment',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
