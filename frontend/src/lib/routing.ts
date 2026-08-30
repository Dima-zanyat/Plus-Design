export type AppRoute =
  | { name: 'home' }
  | { name: 'portfolio' }
  | { name: 'portfolioItem'; slug: string }
  | { name: 'about' }
  | { name: 'contact' }
  | { name: 'adminLogin' }
  | { name: 'admin' }
  | { name: 'adminNew' }
  | { name: 'adminEdit'; id: number }
  | { name: 'notFound' }

export function parsePath(pathname: string): AppRoute {
  const path = pathname.replace(/\/+$/, '') || '/'
  if (path === '/') return { name: 'home' }
  if (path === '/portfolio') return { name: 'portfolio' }
  if (path === '/about') return { name: 'about' }
  if (path === '/contact') return { name: 'contact' }
  if (path === '/admin/login') return { name: 'adminLogin' }
  if (path === '/admin') return { name: 'admin' }
  if (path === '/admin/new') return { name: 'adminNew' }

  const portfolioItem = path.match(/^\/portfolio\/([a-z0-9]+(?:-[a-z0-9]+)*)$/)
  if (portfolioItem) return { name: 'portfolioItem', slug: portfolioItem[1] }

  const adminEdit = path.match(/^\/admin\/(\d+)$/)
  if (adminEdit) return { name: 'adminEdit', id: Number(adminEdit[1]) }

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
    case 'adminLogin':
      return '/admin/login'
    case 'admin':
      return '/admin'
    case 'adminNew':
      return '/admin/new'
    case 'adminEdit':
      return `/admin/${route.id}`
    case 'notFound':
      return '/'
  }
}

export function isAdminRoute(route: AppRoute): boolean {
  return (
    route.name === 'adminLogin' ||
    route.name === 'admin' ||
    route.name === 'adminNew' ||
    route.name === 'adminEdit'
  )
}
