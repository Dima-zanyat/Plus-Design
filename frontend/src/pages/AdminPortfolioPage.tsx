import { useEffect, useState } from 'react'
import { deleteAdminPortfolioItem, fetchAdminPortfolio } from '../api/admin'
import { ApiError } from '../api/client'
import { Link } from '../components/Link'
import type { PortfolioItem } from '../types/api'

type AdminPortfolioPageProps = {
  onNavigate: (path: string) => void
}

export function AdminPortfolioPage({ onNavigate }: AdminPortfolioPageProps) {
  const [items, setItems] = useState<PortfolioItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    fetchAdminPortfolio()
      .then((page) => {
        if (cancelled) return
        setItems(page.items)
        setError(null)
      })
      .catch((err: unknown) => {
        if (cancelled) return
        if (err instanceof ApiError && err.status === 401) {
          onNavigate('/admin/login')
          return
        }
        setError(err instanceof Error ? err.message : 'Не удалось загрузить работы')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [onNavigate])

  const onDelete = async (item: PortfolioItem) => {
    if (!window.confirm(`Удалить «${item.title}»?`)) return
    try {
      await deleteAdminPortfolioItem(item.id)
      setItems((prev) => prev.filter((row) => row.id !== item.id))
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        onNavigate('/admin/login')
        return
      }
      setError(err instanceof Error ? err.message : 'Не удалось удалить')
    }
  }

  return (
    <section className="admin-block">
      <div className="block-head admin-head">
        <div>
          <p className="eyebrow">Админка</p>
          <h1>Работы</h1>
        </div>
        <Link to="/admin/new" className="btn btn-solid" onNavigate={onNavigate}>
          Новая работа
        </Link>
      </div>
      {loading ? <p className="state">Загружаем…</p> : null}
      {error ? <p className="form-note">{error}</p> : null}
      {!loading && items.length === 0 ? <p className="state">Пока нет работ.</p> : null}
      {items.length > 0 ? (
        <div className="admin-table-wrap">
          <table className="admin-table">
            <thead>
              <tr>
                <th>Название</th>
                <th>Slug</th>
                <th>Публикация</th>
                <th>Порядок</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td>{item.title}</td>
                  <td className="muted">{item.slug}</td>
                  <td>{item.is_published ? 'да' : 'черновик'}</td>
                  <td>{item.sort_order}</td>
                  <td className="admin-actions">
                    <Link to={`/admin/${item.id}`} onNavigate={onNavigate}>
                      Править
                    </Link>
                    <button type="button" className="linkish" onClick={() => onDelete(item)}>
                      Удалить
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </section>
  )
}
