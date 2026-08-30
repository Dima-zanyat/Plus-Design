import { clearAdminToken, getAdminToken } from './auth'

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

type ErrorBody = {
  detail?: string | Array<{ msg?: string }>
}

function parseDetail(body: ErrorBody, fallback: string): string {
  const detail = body.detail
  if (typeof detail === 'string' && detail.trim()) return detail
  if (Array.isArray(detail) && detail[0]?.msg) return detail[0].msg
  return fallback
}

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getAdminToken()
  const isFormData = init?.body instanceof FormData
  const response = await fetch(path, {
    ...init,
    headers: {
      Accept: 'application/json',
      ...(init?.body && !isFormData ? { 'Content-Type': 'application/json' } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init?.headers,
    },
  })

  if (response.status === 204) {
    return undefined as T
  }

  const body = (await response.json().catch(() => ({}))) as ErrorBody & T

  if (!response.ok) {
    if (response.status === 401 && path !== '/api/v1/admin/login') {
      clearAdminToken()
    }
    throw new ApiError(parseDetail(body, 'Не удалось выполнить запрос'), response.status)
  }

  return body as T
}
