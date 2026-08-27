import { coverTone } from '../lib/coverTone'
import type { PortfolioItem } from '../types/api'
import { Link } from './Link'

type PortfolioCardProps = {
  item: PortfolioItem
  onNavigate: (path: string) => void
}

export function PortfolioCard({ item, onNavigate }: PortfolioCardProps) {
  const [from, mid, to] = coverTone(item.slug)
  const background = item.cover_image
    ? `center / cover no-repeat url(${item.cover_image})`
    : `linear-gradient(145deg, ${from} 0%, ${mid} 52%, ${to} 100%)`

  return (
    <article className="project-card">
      <Link to={`/portfolio/${item.slug}`} className="project-link" onNavigate={onNavigate}>
        <div className="project-cover" style={{ background }} aria-hidden="true">
          {!item.cover_image && <span>{item.title.slice(0, 1)}</span>}
        </div>
        <div className="project-meta">
          <h3>{item.title}</h3>
          {item.description ? <p>{item.description}</p> : null}
        </div>
      </Link>
    </article>
  )
}
