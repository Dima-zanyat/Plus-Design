import { Link } from '../components/Link'
import { PortfolioCard } from '../components/PortfolioCard'
import type { PortfolioItem } from '../types/api'

type HomePageProps = {
  items: PortfolioItem[]
  loading: boolean
  error: string | null
  onNavigate: (path: string) => void
}

const steps = [
  { n: '01', title: 'Бриф', text: 'Площадь, планировка, как живёте сейчас и какой результат нужен.' },
  { n: '02', title: 'Проект', text: 'Планировочные решения, материалы и чертежи под реализацию.' },
  { n: '03', title: 'Визуализация', text: 'Картинка будущего интерьера, чтобы согласовать решения до стройки.' },
  { n: '04', title: 'Надзор', text: 'Авторский надзор: чтобы на объекте получилось как в проекте.' },
]

export function HomePage({ items, loading, error, onNavigate }: HomePageProps) {
  return (
    <>
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">Анастасия Плюснина</p>
          <h1>Интерьеры квартир и домов.</h1>
          <p className="lead">
            Проектирование, визуализация и авторский надзор. Сайт-визитка: здесь можно
            посмотреть работы и оставить заявку на проект.
          </p>
          <div className="hero-actions">
            <Link to="/contact" className="btn btn-solid" onNavigate={onNavigate}>
              Обсудить проект
            </Link>
            <Link to="/portfolio" className="btn btn-ghost" onNavigate={onNavigate}>
              Смотреть работы
            </Link>
          </div>
        </div>

        <div className="hero-visual" aria-hidden="true">
          <div className="stone stone-a" />
          <div className="stone stone-b" />
          <div className="stone stone-c" />
          <p>
            практика
            <strong>4 года · квартиры · дома</strong>
          </p>
        </div>
      </section>

      <section className="band">
        <article>
          <strong>4 года</strong>
          <span>проектирование и визуализация интерьеров</span>
        </article>
        <article>
          <strong>квартиры</strong>
          <span>планировки и интерьеры жилых пространств</span>
        </article>
        <article>
          <strong>надзор</strong>
          <span>сопровождение проекта на объекте</span>
        </article>
      </section>

      <section className="block">
        <header className="block-head">
          <p className="eyebrow">Портфолио</p>
          <h2>Проекты, которые можно посмотреть без лишних слов.</h2>
        </header>
        {loading ? <p className="state">Загружаем витрину…</p> : null}
        {error ? <p className="state">{error}</p> : null}
        {!loading && !error && items.length === 0 ? (
          <p className="state">Пока витрина пустая. Когда API отдаст работы — они появятся здесь.</p>
        ) : null}
        <div className="portfolio-grid">
          {items.map((item) => (
            <PortfolioCard key={item.id} item={item} onNavigate={onNavigate} />
          ))}
        </div>
        {items.length > 0 ? (
          <p className="block-more">
            <Link to="/portfolio" onNavigate={onNavigate}>
              Все проекты
            </Link>
          </p>
        ) : null}
      </section>

      <section className="block">
        <header className="block-head">
          <p className="eyebrow">Как идём</p>
          <h2>От заявки до объекта.</h2>
        </header>
        <div className="process">
          {steps.map((step) => (
            <article key={step.n}>
              <span>{step.n}</span>
              <h3>{step.title}</h3>
              <p>{step.text}</p>
            </article>
          ))}
        </div>
      </section>
    </>
  )
}
