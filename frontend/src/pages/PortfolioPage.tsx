import { Pagination } from '../components/Pagination'
import { PortfolioCard } from '../components/PortfolioCard'
import type { Page, PortfolioItem } from '../types/api'

type PortfolioPageProps = {
  data: Page<PortfolioItem> | null
  loading: boolean
  error: string | null
  onPage: (page: number) => void
  onNavigate: (path: string) => void
}

export function PortfolioPage({ data, loading, error, onPage, onNavigate }: PortfolioPageProps) {
  return (
    <section className="block">
      <header className="block-head">
        <p className="eyebrow">Проекты</p>
        <h1>Портфолио</h1>
        <p className="lead">Интерьеры квартир и домов. Одна обложка на проект — так сейчас устроен API.</p>
      </header>

      {loading ? <p className="state">Загружаем работы…</p> : null}
      {error ? <p className="state">{error}</p> : null}
      {data && data.items.length === 0 && !loading ? (
        <p className="state">Работ пока нет. Пустая витрина — это нормальный ответ API, не ошибка.</p>
      ) : null}

      {data ? (
        <>
          <div className="portfolio-grid">
            {data.items.map((item) => (
              <PortfolioCard key={item.id} item={item} onNavigate={onNavigate} />
            ))}
          </div>
          <Pagination
            page={data.page}
            pages={data.pages}
            hasPrev={data.has_prev}
            hasNext={data.has_next}
            onChange={onPage}
          />
        </>
      ) : null}
    </section>
  )
}
