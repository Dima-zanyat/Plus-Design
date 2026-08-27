export type PortfolioItem = {
  id: number
  title: string
  slug: string
  description: string
  cover_image: string | null
  created_at: string
}

export type Page<T> = {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
  has_next: boolean
  has_prev: boolean
}

export type LeadPayload = {
  name: string
  phone: string
  email: string | null
  message: string | null
}

export type Lead = LeadPayload & {
  id: number
  status: 'new' | 'in_progress' | 'done' | 'rejected'
  created_at: string
}
