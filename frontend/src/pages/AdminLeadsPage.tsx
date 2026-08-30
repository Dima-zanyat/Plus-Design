import { useEffect, useState } from 'react'
import { fetchAdminLeads, updateLeadStatus } from '../api/admin'
import { ApiError } from '../api/client'
import type { Lead } from '../types/api'

type AdminLeadsPageProps = {
  onNavigate: (path: string) => void
}

const STATUS_LABEL: Record<Lead['status'], string> = {
  new: 'Новая',
  in_progress: 'В работе',
  done: 'Завершена',
  rejected: 'Отклонена',
}

function formatDate(value: string): string {
  return new Date(value).toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function AdminLeadsPage({ onNavigate }: AdminLeadsPageProps) {
  const [leads, setLeads] = useState<Lead[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [busyId, setBusyId] = useState<number | null>(null)

  useEffect(() => {
    let cancelled = false
    fetchAdminLeads(1, 100)
      .then((page) => {
        if (cancelled) return
        setLeads(page.items)
        setError(null)
      })
      .catch((err: unknown) => {
        if (cancelled) return
        if (err instanceof ApiError && err.status === 401) {
          onNavigate('/admin/login')
          return
        }
        setError(err instanceof Error ? err.message : 'Не удалось загрузить заявки')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [onNavigate])

  const onStatusChange = async (lead: Lead, status: Lead['status']) => {
    setBusyId(lead.id)
    try {
      const updated = await updateLeadStatus(lead.id, status)
      setLeads((prev) => prev.map((row) => (row.id === lead.id ? updated : row)))
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        onNavigate('/admin/login')
        return
      }
      setError(err instanceof Error ? err.message : 'Не удалось обновить статус')
    } finally {
      setBusyId(null)
    }
  }

  return (
    <section className="admin-block">
      <div className="block-head admin-head">
        <div>
          <p className="eyebrow">Админка</p>
          <h1>Заявки</h1>
        </div>
      </div>
      {loading ? <p className="state">Загружаем…</p> : null}
      {error ? <p className="form-note">{error}</p> : null}
      {!loading && leads.length === 0 ? <p className="state">Заявок пока нет.</p> : null}
      {leads.length > 0 ? (
        <div className="admin-table-wrap">
          <table className="admin-table">
            <thead>
              <tr>
                <th>Дата</th>
                <th>Имя</th>
                <th>Телефон</th>
                <th>Email</th>
                <th>Сообщение</th>
                <th>Статус</th>
              </tr>
            </thead>
            <tbody>
              {leads.map((lead) => (
                <tr key={lead.id}>
                  <td className="muted">{formatDate(lead.created_at)}</td>
                  <td>{lead.name}</td>
                  <td>
                    <a href={`tel:${lead.phone}`}>{lead.phone}</a>
                  </td>
                  <td className="muted">
                    {lead.email ? <a href={`mailto:${lead.email}`}>{lead.email}</a> : '—'}
                  </td>
                  <td className="muted">{lead.message ?? '—'}</td>
                  <td>
                    <select
                      value={lead.status}
                      disabled={busyId === lead.id}
                      onChange={(event) =>
                        onStatusChange(lead, event.target.value as Lead['status'])
                      }
                    >
                      {(Object.keys(STATUS_LABEL) as Lead['status'][]).map((status) => (
                        <option key={status} value={status}>
                          {STATUS_LABEL[status]}
                        </option>
                      ))}
                    </select>
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
