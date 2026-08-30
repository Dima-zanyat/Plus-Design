import { useState, type FormEvent } from 'react'
import { loginAdmin } from '../api/admin'
import { ApiError } from '../api/client'
import { setAdminToken } from '../api/auth'

type AdminLoginPageProps = {
  onNavigate: (path: string) => void
}

export function AdminLoginPage({ onNavigate }: AdminLoginPageProps) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setBusy(true)
    setError('')
    try {
      const token = await loginAdmin(username.trim(), password)
      setAdminToken(token.access_token)
      onNavigate('/admin')
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('Не удалось войти. Проверьте, что API запущен.')
      }
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="admin-login">
      <p className="eyebrow">Админка</p>
      <h1>Вход</h1>
      <form className="lead-form" onSubmit={onSubmit}>
        <label>
          <span>Логин</span>
          <input
            name="username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            autoComplete="username"
            required
          />
        </label>
        <label>
          <span>Пароль</span>
          <input
            name="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
            required
          />
        </label>
        <button type="submit" disabled={busy}>
          {busy ? 'Входим…' : 'Войти'}
        </button>
        {error ? <p className="form-note">{error}</p> : null}
      </form>
    </section>
  )
}
