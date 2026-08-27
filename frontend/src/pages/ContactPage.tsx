import { LeadForm } from '../components/LeadForm'

export function ContactPage() {
  return (
    <section className="contact">
      <div>
        <p className="eyebrow">Заявка</p>
        <h1>Опишите квартиру или дом — отвечу по задаче.</h1>
        <p className="lead">
          Имя и телефон обязательны. Email — если удобнее переписка. В сообщении
          достаточно площади, типа объекта и того, что нужно: проект, визуализация
          или надзор.
        </p>
      </div>
      <LeadForm />
    </section>
  )
}
