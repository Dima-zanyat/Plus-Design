import { useState, type ChangeEvent, type FormEvent } from 'react'
import { ApiError } from '../api/client'
import { createLead } from '../api/leads'

const initial = { name: '', phone: '', email: '', message: '' }

export function LeadForm() {
  const [form, setForm] = useState(initial)
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')
  const [ok, setOk] = useState(false)

  const onChange = (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setBusy(true)
    setMessage('')
    setOk(false)

    try {
      await createLead({
        name: form.name.trim(),
        phone: form.phone.trim(),
        email: form.email.trim() || null,
        message: form.message.trim() || null,
      })
      setForm(initial)
      setOk(true)
      setMessage('Спасибо. Свяжусь, когда посмотрю задачу.')
    } catch (error) {
      if (error instanceof ApiError && error.status === 409) {
        setMessage('Заявка с этого номера уже отправлена. Подождите несколько минут.')
      } else if (error instanceof Error) {
        setMessage(error.message)
      } else {
        setMessage('Не удалось отправить заявку. Проверьте, что API запущен.')
      }
    } finally {
      setBusy(false)
    }
  }

  return (
    <form className="lead-form" onSubmit={onSubmit} noValidate>
      <label>
        <span>Имя</span>
        <input
          name="name"
          value={form.name}
          onChange={onChange}
          minLength={2}
          maxLength={120}
          required
          placeholder="Анна Петрова"
          autoComplete="name"
        />
      </label>
      <label>
        <span>Телефон</span>
        <input
          name="phone"
          type="tel"
          value={form.phone}
          onChange={onChange}
          minLength={7}
          maxLength={25}
          required
          placeholder="+7 999 123 45 67"
          autoComplete="tel"
        />
      </label>
      <label>
        <span>Email — по желанию</span>
        <input
          name="email"
          type="email"
          value={form.email}
          onChange={onChange}
          maxLength={254}
          placeholder="anna@example.com"
          autoComplete="email"
        />
      </label>
      <label>
        <span>Задача</span>
        <textarea
          name="message"
          value={form.message}
          onChange={onChange}
          maxLength={2000}
          rows={5}
          placeholder="Квартира 72 м², нужен проект и визуализация"
        />
      </label>
      <button type="submit" disabled={busy}>
        {busy ? 'Отправляем…' : 'Отправить заявку'}
      </button>
      {message ? <p className={ok ? 'form-note is-ok' : 'form-note'}>{message}</p> : null}
    </form>
  )
}
