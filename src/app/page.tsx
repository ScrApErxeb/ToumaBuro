'use client'

import { useSupabaseAuth } from '@/hooks/useSupabaseAuth'
import { supabase } from '@/lib/supabase'

export default function Home() {
  const { user, loading } = useSupabaseAuth()

  if (loading) return <p className="p-4">Chargement...</p>

  if (!user)
    return (
      <main className="flex flex-col items-center justify-center min-h-screen p-4">
        <h1 className="text-3xl font-bold mb-4">Bienvenue sur ServiNow</h1>
        <p>Veuillez vous <a href="/login" className="text-blue-600 underline">connecter</a>.</p>
      </main>
    )

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-3xl font-bold mb-4">Bienvenue, {user.email} !</h1>
      <button
        onClick={async () => {
          await supabase.auth.signOut()
          // Optionnel : rediriger ou rafraîchir la page
          window.location.href = '/'
        }}
        className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
      >
        Déconnexion
      </button>
    </main>
  )
}
