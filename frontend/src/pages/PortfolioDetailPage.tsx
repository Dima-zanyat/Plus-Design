import { coverTone } from '../lib/coverTone'
import { Link } from '../components/Link'
import type { PortfolioItem } from '../types/api'

type PortfolioDetailPageProps = {
  item: PortfolioItem | null
  loading: boolean
  error: string | null
  onNavigate: (path: string) => void
}

export function PortfolioDetailPage({
  item,
  loading,
  error,
  onNavigate,
}: PortfolioDetailPageProps) {
  if (loading) return <p className="state">Открываем работу…</p>
  if (error || !item) {
    return (
      <section className="block">
        <p className="state">{error ?? 'Работа не найдена'}</p>
        <Link to="/portfolio" onNavigate={onNavigate}>
          К витрине
        </Link>
      </section>
    )
  }

  const [from, mid, to] = coverTone(item.slug)
  const background = item.cover_image
    ? `center / cover no-repeat url(${item.cover_image})`
    : `linear-gradient(160deg, ${from}, ${mid}, ${to})`

  return (
    <article className="detail">
      <p className="eyebrow">Проект</p>
      <h1>{item.title}</h1>
      <div className="detail-cover" style={{ background }} />
      {item.category ? <p className="muted">{item.category.name}</p> : null}
      {item.tags.length > 0 ? (
        <p className="muted">{item.tags.map((tag) => tag.name).join(' · ')}</p>
      ) : null}
      {item.description ? <p className="lead">{item.description}</p> : <p className="lead">Описание ещё не добавлено.</p>}
      {item.images.length > 0 ? (
        <div className="gallery">
          {item.images.map((image) => (
            <img key={image.id} src={image.url} alt={image.alt || item.title} />
          ))}
        </div>
      ) : null}
      <p className="muted">
        {new Date(item.created_at).toLocaleDateString('ru-RU', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        })}
      </p>
      <Link to="/contact" className="btn btn-solid" onNavigate={onNavigate}>
        Заказать похожий
      </Link>
    </article>
  )
}
