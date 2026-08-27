import { Link } from './Link'

type FooterProps = {
  onNavigate: (path: string) => void
}

export function Footer({ onNavigate }: FooterProps) {
  return (
    <footer className="site-footer">
      <div>
        <p className="footer-brand">Плюс Дизайн</p>
        <p>Анастасия Плюснина · дизайн интерьера</p>
      </div>
      <div className="footer-links">
        <Link to="/portfolio" onNavigate={onNavigate}>
          Портфолио
        </Link>
        <Link to="/contact" onNavigate={onNavigate}>
          Заявка
        </Link>
      </div>
    </footer>
  )
}
