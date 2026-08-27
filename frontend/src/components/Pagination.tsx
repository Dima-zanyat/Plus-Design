type PaginationProps = {
  page: number
  pages: number
  hasPrev: boolean
  hasNext: boolean
  onChange: (page: number) => void
}

export function Pagination({ page, pages, hasPrev, hasNext, onChange }: PaginationProps) {
  if (pages <= 1) return null

  return (
    <nav className="pagination" aria-label="Страницы портфолио">
      <button type="button" disabled={!hasPrev} onClick={() => onChange(page - 1)}>
        Назад
      </button>
      <span>
        {page} из {pages}
      </span>
      <button type="button" disabled={!hasNext} onClick={() => onChange(page + 1)}>
        Дальше
      </button>
    </nav>
  )
}
