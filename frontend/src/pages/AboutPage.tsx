import { Link } from '../components/Link'

type AboutPageProps = {
  onNavigate: (path: string) => void
}

export function AboutPage({ onNavigate }: AboutPageProps) {
  return (
    <section className="about">
      <div>
        <p className="eyebrow">О себе</p>
        <h1>Анастасия Плюснина</h1>
        <p className="lead">
          Дизайнер-проектировщик и дизайнер-визуализатор. Четыре года работаю с
          интерьерами квартир и домов: от планировки до картинки, которую можно
          согласовать до ремонта. На объектах веду авторский надзор.
        </p>
        <Link to="/contact" className="btn btn-solid" onNavigate={onNavigate}>
          Оставить заявку
        </Link>
      </div>
      <aside className="about-notes">
        <article>
          <strong>Проектирование</strong>
          <span>Планировочные решения и рабочая документация для квартиры или дома.</span>
        </article>
        <article>
          <strong>Визуализация</strong>
          <span>Понять объём, свет и материалы до начала работ на объекте.</span>
        </article>
        <article>
          <strong>Авторский надзор</strong>
          <span>Следить, чтобы реализация совпала с проектом.</span>
        </article>
      </aside>
    </section>
  )
}
