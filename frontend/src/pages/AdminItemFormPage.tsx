import { useEffect, useState, type FormEvent } from 'react'
import {
  createAdminPortfolioItem,
  fetchAdminPortfolioItem,
  updateAdminPortfolioItem,
} from '../api/admin'
import { ApiError } from '../api/client'
import { Link } from '../components/Link'
import type { PortfolioItem, PortfolioItemWrite } from '../types/api'

type AdminItemFormPageProps = {
  itemId: number | null
  onNavigate: (path: string) => void
}

type FormState = {
  title: string
  slug: string
  description: string
  cover_image: string
  is_published: boolean
  sort_order: string
  gallery: string
}

const emptyForm: FormState = {
  title: '',
  slug: '',
  description: '',
  cover_image: '',
  is_published: true,
  sort_order: '0',
  gallery: '',
}

function toForm(item: PortfolioItem): FormState {
  return {
    title: item.title,
    slug: item.slug,
    description: item.description,
    cover_image: item.cover_image ?? '',
    is_published: item.is_published,
    sort_order: String(item.sort_order),
    gallery: item.images.map((image) => image.url).join('\n'),
  }
}

function parseGallery(text: string) {
  return text
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
    .map((url, index) => ({ url, sort_order: index }))
}

function toPayload(form: FormState): PortfolioItemWrite {
  return {
    title: form.title.trim(),
    slug: form.slug.trim(),
    description: form.description,
    cover_image: form.cover_image.trim() || null,
    is_published: form.is_published,
    sort_order: Number(form.sort_order) || 0,
    images: parseGallery(form.gallery),
  }
}

export function AdminItemFormPage({ itemId, onNavigate }: AdminItemFormPageProps) {
  const isEdit = itemId !== null
  const [form, setForm] = useState<FormState>(emptyForm)
  const [loading, setLoading] = useState(isEdit)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (itemId === null) return
    fetchAdminPortfolioItem(itemId)
      .then((item) => {
        setForm(toForm(item))
        setError('')
      })
      .catch((err: unknown) => {
        if (err instanceof ApiError && err.status === 401) {
          onNavigate('/admin/login')
          return
        }
        setError(err instanceof Error ? err.message : 'Не удалось открыть работу')
      })
      .finally(() => setLoading(false))
  }, [itemId, onNavigate])

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setBusy(true)
    setError('')
    const payload = toPayload(form)
    try {
      if (isEdit && itemId !== null) {
        await updateAdminPortfolioItem(itemId, payload)
      } else {
        await createAdminPortfolioItem(payload)
      }
      onNavigate('/admin')
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        onNavigate('/admin/login')
        return
      }
      setError(err instanceof Error ? err.message : 'Не удалось сохранить')
    } finally {
      setBusy(false)
    }
  }

  if (loading) return <p className="state">Открываем форму…</p>

  return (
    <section className="admin-block">
      <p className="eyebrow">Админка</p>
      <h1>{isEdit ? 'Правка работы' : 'Новая работа'}</h1>
      <form className="lead-form admin-form" onSubmit={onSubmit}>
        <label>
          <span>Название</span>
          <input
            value={form.title}
            onChange={(event) => setForm((prev) => ({ ...prev, title: event.target.value }))}
            required
            maxLength={200}
          />
        </label>
        <label>
          <span>Slug</span>
          <input
            value={form.slug}
            onChange={(event) => setForm((prev) => ({ ...prev, slug: event.target.value }))}
            required
            pattern="[a-z0-9]+(?:-[a-z0-9]+)*"
            placeholder="kvartira-na-sadovoy"
          />
        </label>
        <label>
          <span>Описание</span>
          <textarea
            value={form.description}
            onChange={(event) => setForm((prev) => ({ ...prev, description: event.target.value }))}
            rows={5}
          />
        </label>
        <label>
          <span>Обложка — URL</span>
          <input
            value={form.cover_image}
            onChange={(event) => setForm((prev) => ({ ...prev, cover_image: event.target.value }))}
            placeholder="https://…"
          />
        </label>
        <label className="check-row">
          <input
            type="checkbox"
            checked={form.is_published}
            onChange={(event) =>
              setForm((prev) => ({ ...prev, is_published: event.target.checked }))
            }
          />
          <span>Опубликована</span>
        </label>
        <label>
          <span>Порядок</span>
          <input
            type="number"
            value={form.sort_order}
            onChange={(event) => setForm((prev) => ({ ...prev, sort_order: event.target.value }))}
          />
        </label>
        <label>
          <span>Галерея — URL по одному в строке</span>
          <textarea
            value={form.gallery}
            onChange={(event) => setForm((prev) => ({ ...prev, gallery: event.target.value }))}
            rows={4}
            placeholder="https://example.com/1.jpg"
          />
        </label>
        <div className="hero-actions">
          <button type="submit" disabled={busy}>
            {busy ? 'Сохраняем…' : 'Сохранить'}
          </button>
          <Link to="/admin" className="btn btn-ghost" onNavigate={onNavigate}>
            Отмена
          </Link>
        </div>
        {error ? <p className="form-note">{error}</p> : null}
      </form>
    </section>
  )
}
