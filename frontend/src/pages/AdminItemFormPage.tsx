import { useEffect, useState, type ChangeEvent, type FormEvent } from 'react'
import {
  createAdminPortfolioItem,
  fetchAdminPortfolioItem,
  updateAdminPortfolioItem,
  uploadAdminImage,
} from '../api/admin'
import { ApiError } from '../api/client'
import { Link } from '../components/Link'
import type { PortfolioItem, PortfolioItemWrite } from '../types/api'

type AdminItemFormPageProps = {
  itemId: number | null
  onNavigate: (path: string) => void
}

type GalleryImage = {
  url: string
  alt: string
}

type FormState = {
  title: string
  slug: string
  description: string
  cover_image: string
  is_published: boolean
  sort_order: string
  gallery: GalleryImage[]
}

const emptyForm: FormState = {
  title: '',
  slug: '',
  description: '',
  cover_image: '',
  is_published: true,
  sort_order: '0',
  gallery: [],
}

function toForm(item: PortfolioItem): FormState {
  return {
    title: item.title,
    slug: item.slug,
    description: item.description,
    cover_image: item.cover_image ?? '',
    is_published: item.is_published,
    sort_order: String(item.sort_order),
    gallery: item.images.map((image) => ({ url: image.url, alt: image.alt ?? '' })),
  }
}

function toPayload(form: FormState): PortfolioItemWrite {
  return {
    title: form.title.trim(),
    slug: form.slug.trim(),
    description: form.description,
    cover_image: form.cover_image.trim() || null,
    is_published: form.is_published,
    sort_order: Number(form.sort_order) || 0,
    images: form.gallery.map((image, index) => ({
      url: image.url,
      alt: image.alt,
      sort_order: index,
    })),
  }
}

export function AdminItemFormPage({ itemId, onNavigate }: AdminItemFormPageProps) {
  const isEdit = itemId !== null
  const [form, setForm] = useState<FormState>(emptyForm)
  const [loading, setLoading] = useState(isEdit)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [uploadingCover, setUploadingCover] = useState(false)
  const [uploadingGallery, setUploadingGallery] = useState(false)

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

  const handleUploadError = (err: unknown) => {
    if (err instanceof ApiError && err.status === 401) {
      onNavigate('/admin/login')
      return
    }
    setError(err instanceof Error ? err.message : 'Не удалось загрузить изображение')
  }

  const onCoverFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    event.target.value = ''
    if (!file) return
    setUploadingCover(true)
    setError('')
    try {
      const { url } = await uploadAdminImage(file)
      setForm((prev) => ({ ...prev, cover_image: url }))
    } catch (err) {
      handleUploadError(err)
    } finally {
      setUploadingCover(false)
    }
  }

  const onGalleryFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files ? Array.from(event.target.files) : []
    event.target.value = ''
    if (files.length === 0) return
    setUploadingGallery(true)
    setError('')
    try {
      for (const file of files) {
        const { url } = await uploadAdminImage(file)
        setForm((prev) => ({ ...prev, gallery: [...prev.gallery, { url, alt: '' }] }))
      }
    } catch (err) {
      handleUploadError(err)
    } finally {
      setUploadingGallery(false)
    }
  }

  const removeGalleryImage = (index: number) => {
    setForm((prev) => ({ ...prev, gallery: prev.gallery.filter((_, i) => i !== index) }))
  }

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
            onChange={(event) =>
              setForm((prev) => ({ ...prev, description: event.target.value }))
            }
            rows={5}
          />
        </label>

        <div className="admin-upload-field">
          <span>Обложка</span>
          {form.cover_image ? (
            <div className="admin-cover-preview">
              <img src={form.cover_image} alt="" />
              <button
                type="button"
                className="linkish"
                onClick={() => setForm((prev) => ({ ...prev, cover_image: '' }))}
              >
                Убрать
              </button>
            </div>
          ) : (
            <p className="admin-hint">Обложка не выбрана</p>
          )}
          <input
            type="file"
            accept="image/png,image/jpeg,image/webp,image/gif"
            disabled={uploadingCover}
            onChange={onCoverFileChange}
          />
          {uploadingCover ? <p className="admin-hint">Загружаем…</p> : null}
        </div>

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

        <div className="admin-upload-field">
          <span>Галерея</span>
          {form.gallery.length > 0 ? (
            <ul className="admin-gallery">
              {form.gallery.map((image, index) => (
                <li key={`${image.url}-${index}`}>
                  <img src={image.url} alt={image.alt} />
                  <button
                    type="button"
                    className="linkish"
                    onClick={() => removeGalleryImage(index)}
                  >
                    Удалить
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <p className="admin-hint">Изображений пока нет</p>
          )}
          <input
            type="file"
            accept="image/png,image/jpeg,image/webp,image/gif"
            multiple
            disabled={uploadingGallery}
            onChange={onGalleryFileChange}
          />
          {uploadingGallery ? <p className="admin-hint">Загружаем…</p> : null}
        </div>

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
