export type NamedSlug = {
  id: number
  name: string
  slug: string
}

export type PortfolioImage = {
  id: number
  url: string
  alt: string
  sort_order: number
}

export type PortfolioItem = {
  id: number
  title: string
  slug: string
  description: string
  cover_image: string | null
  created_at: string
  is_published: boolean
  sort_order: number
  category: NamedSlug | null
  tags: NamedSlug[]
  images: PortfolioImage[]
}

export type PortfolioItemWrite = {
  title: string
  slug: string
  description?: string
  cover_image?: string | null
  is_published?: boolean
  sort_order?: number
  images?: { url: string; alt?: string; sort_order?: number }[]
}

export type PortfolioItemUpdate = {
  title?: string
  slug?: string
  description?: string
  cover_image?: string | null
  is_published?: boolean
  sort_order?: number
  images?: { url: string; alt?: string; sort_order?: number }[]
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

export type TokenResponse = {
  access_token: string
  token_type: string
}
