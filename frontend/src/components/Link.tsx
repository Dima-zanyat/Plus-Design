import type { MouseEvent, ReactNode } from 'react'

type Navigate = (path: string) => void

type LinkProps = {
  to: string
  className?: string
  children: ReactNode
  onNavigate: Navigate
}

export function Link({ to, className, children, onNavigate }: LinkProps) {
  const handleClick = (event: MouseEvent<HTMLAnchorElement>) => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return
    event.preventDefault()
    onNavigate(to)
  }

  return (
    <a href={to} className={className} onClick={handleClick}>
      {children}
    </a>
  )
}
