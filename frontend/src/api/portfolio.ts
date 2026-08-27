import type { Page, PortfolioItem } from '../types/api'
import { apiFetch } from './client'

export function fetchPortfolio(page = 1, size = 12) {
  const params = new URLSearchParams({ page: String(page), size: String(size) })
  return apiFetch<Page<PortfolioItem>>(`/api/v1/portfolio?${params}`)
}

export function fetchPortfolioItem(slug: string) {
  return apiFetch<PortfolioItem>(`/api/v1/portfolio/${encodeURIComponent(slug)}`)
}
