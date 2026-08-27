import { Link } from './Link'

type HeaderProps = {
  currentPath: string
  onNavigate: (path: string) => void
}

const links = [
  { to: '/', label: 'Главная' },
  { to: '/portfolio', label: 'Портфолио' },
  { to: '/about', label: 'О себе' },
  { to: '/contact', label: 'Контакты' },
]

export function Header({ currentPath, onNavigate }: HeaderProps) {
  return (
    <header className="site-header">
      <Link to="/" className="brand" onNavigate={onNavigate}>
        <span className="brand-mark" aria-hidden="true">
          ＋
        </span>
        <span className="brand-copy">
          <strong>Плюс Дизайн</strong>
          <em>интерьеры квартир и домов</em>
        </span>
      </Link>

      <nav className="site-nav" aria-label="Основная навигация">
        {links.map((link) => {
          const active =
            link.to === '/'
              ? currentPath === '/'
              : currentPath === link.to || currentPath.startsWith(`${link.to}/`)
          return (
            <Link
              key={link.to}
              to={link.to}
              className={active ? 'nav-link is-active' : 'nav-link'}
              onNavigate={onNavigate}
            >
              {link.label}
            </Link>
          )
        })}
      </nav>

      <Link to="/contact" className="header-cta" onNavigate={onNavigate}>
        Оставить заявку
      </Link>
    </header>
  )
}
