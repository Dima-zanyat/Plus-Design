import { Link } from './Link'
import { clearAdminToken } from '../api/auth'

type AdminHeaderProps = {
  onNavigate: (path: string) => void
}

export function AdminHeader({ onNavigate }: AdminHeaderProps) {
  const logout = () => {
    clearAdminToken()
    onNavigate('/admin/login')
  }

  return (
    <header className="site-header">
      <Link to="/admin" className="brand" onNavigate={onNavigate}>
        <span className="brand-mark" aria-hidden="true">
          ＋
        </span>
        <span className="brand-copy">
          <strong>Плюс Дизайн</strong>
          <em>админка</em>
        </span>
      </Link>
      <nav className="site-nav" aria-label="Админка">
        <Link to="/admin" className="nav-link" onNavigate={onNavigate}>
          Работы
        </Link>
        <Link to="/admin/leads" className="nav-link" onNavigate={onNavigate}>
          Заявки
        </Link>
        <Link to="/" className="nav-link" onNavigate={onNavigate}>
          На сайт
        </Link>
      </nav>
      <button type="button" className="header-cta" onClick={logout}>
        Выйти
      </button>
    </header>
  )
}
