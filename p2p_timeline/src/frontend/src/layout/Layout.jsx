import React from 'react'

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-white dark:bg-slate-800 text-slate-700 dark:text-white font-sans font-medium">
      <div className="max-w-7xl mx-auto">{children}</div>
    </div>
  )
}
