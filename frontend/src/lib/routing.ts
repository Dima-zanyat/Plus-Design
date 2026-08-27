export type AppRoute =
  | { name: 'home' }
  | { name: 'portfolio' }
  | { name: 'portfolioItem'; slug: string }
  | { name: 'about' }
  | { name: 'contact' }
  | { name: 'notFound' }

export function parsePath(pathname: string): AppRoute {
  const path = pathname.replace(/\/+$/, '') || '/'
  if (path === '/') return { name: 'home' }
  if (path === '/portfolio') return { name: 'portfolio' }
  if (path === '/about') return { name: 'about' }
  if (path === '/contact') return { name: 'contact' }

  const match = path.match(/^\/portfolio\/([a-z0-9]+(?:-[a-z0-9]+)*)$/)
  if (match) return { name: 'portfolioItem', slug: match[1] }

  return { name: 'notFound' }
}

export function hrefFor(route: AppRoute): string {
  switch (route.name) {
    case 'home':
      return '/'
    case 'portfolio':
      return '/portfolio'
    case 'portfolioItem':
      return `/portfolio/${route.slug}`
    case 'about':
      return '/about'
    case 'contact':
      return '/contact'
    case 'notFound':
      return '/'
  }
}
