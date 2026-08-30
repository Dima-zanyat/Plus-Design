import type {
  Page,
  PortfolioItem,
  PortfolioItemUpdate,
  PortfolioItemWrite,
  TokenResponse,
} from '../types/api'
import { apiFetch } from './client'

export function loginAdmin(username: string, password: string) {
  return apiFetch<TokenResponse>('/api/v1/admin/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

export function fetchAdminPortfolio(page = 1, size = 50) {
  const params = new URLSearchParams({ page: String(page), size: String(size) })
  return apiFetch<Page<PortfolioItem>>(`/api/v1/admin/portfolio?${params}`)
}

export function fetchAdminPortfolioItem(id: number) {
  return apiFetch<PortfolioItem>(`/api/v1/admin/portfolio/${id}`)
}

export function createAdminPortfolioItem(payload: PortfolioItemWrite) {
  return apiFetch<PortfolioItem>('/api/v1/admin/portfolio', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateAdminPortfolioItem(id: number, payload: PortfolioItemUpdate) {
  return apiFetch<PortfolioItem>(`/api/v1/admin/portfolio/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

export function deleteAdminPortfolioItem(id: number) {
  return apiFetch<void>(`/api/v1/admin/portfolio/${id}`, { method: 'DELETE' })
}
