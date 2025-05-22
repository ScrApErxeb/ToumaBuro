'use client'

import { useState } from 'react'
import { supabase } from '@/lib/supabase'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setMessage('Envoi du lien magique...')

    const { error } = await supabase.auth.signInWithOtp({ email })

    if (error) {
      setMessage(`Erreur : ${error.message}`)
    } else {
      setMessage('Lien envoyé ! Vérifie ta boîte mail ✉️')
    }
  }

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="mb-6 text-3xl font-bold">Connexion Magic Link</h1>
      <form onSubmit={handleLogin} className="flex flex-col gap-4 w-full max-w-sm">
        <input
          type="email"
          placeholder="Ton email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
          className="p-3 border border-gray-300 rounded"
        />
        <button
          type="submit"
          className="p-3 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          Envoyer le lien magique
        </button>
      </form>
      {message && <p className="mt-4 text-center">{message}</p>}
    </main>
  )
}
