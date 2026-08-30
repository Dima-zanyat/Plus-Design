import { useEffect, useState } from 'react'
import { isAdminAuthenticated } from './api/auth'
import { fetchPortfolio, fetchPortfolioItem } from './api/portfolio'
import { AdminHeader } from './components/AdminHeader'
import { Footer } from './components/Footer'
import { Header } from './components/Header'
import { Link } from './components/Link'
import { useRoute } from './hooks/useRoute'
import { isAdminRoute } from './lib/routing'
import { AboutPage } from './pages/AboutPage'
import { AdminItemFormPage } from './pages/AdminItemFormPage'
import { AdminLeadsPage } from './pages/AdminLeadsPage'
import { AdminLoginPage } from './pages/AdminLoginPage'
import { AdminPortfolioPage } from './pages/AdminPortfolioPage'
import { ContactPage } from './pages/ContactPage'
import { HomePage } from './pages/HomePage'
import { PortfolioDetailPage } from './pages/PortfolioDetailPage'
import { PortfolioPage } from './pages/PortfolioPage'
import type { Page, PortfolioItem } from './types/api'
import './App.css'

export default function App() {
  const { path, route, navigate } = useRoute()
  const detailSlug = route.name === 'portfolioItem' ? route.slug : null
  const [homeItems, setHomeItems] = useState<PortfolioItem[]>([])
  const [homeLoading, setHomeLoading] = useState(true)
  const [homeError, setHomeError] = useState<string | null>(null)

  const [list, setList] = useState<Page<PortfolioItem> | null>(null)
  const [listPage, setListPage] = useState(1)
  const [listLoading, setListLoading] = useState(false)
  const [listError, setListError] = useState<string | null>(null)

  const [detail, setDetail] = useState<PortfolioItem | null>(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [detailError, setDetailError] = useState<string | null>(null)

  useEffect(() => {
    const needsAuth =
      route.name === 'admin' ||
      route.name === 'adminNew' ||
      route.name === 'adminEdit' ||
      route.name === 'adminLeads'
    if (needsAuth && !isAdminAuthenticated()) {
      navigate('/admin/login')
    }
  }, [route, navigate])

  useEffect(() => {
    let cancelled = false
    setHomeLoading(true)
    fetchPortfolio(1, 6)
      .then((page) => {
        if (!cancelled) {
          setHomeItems(page.items)
          setHomeError(null)
        }
      })
      .catch(() => {
        if (!cancelled) setHomeError('Не удалось загрузить портфолио. Запустите backend на :8000.')
      })
      .finally(() => {
        if (!cancelled) setHomeLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [])

  useEffect(() => {
    if (route.name !== 'portfolio') return
    let cancelled = false
    setListLoading(true)
    fetchPortfolio(listPage, 12)
      .then((page) => {
        if (!cancelled) {
          setList(page)
          setListError(null)
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setListError(error instanceof Error ? error.message : 'Не удалось загрузить витрину')
        }
      })
      .finally(() => {
        if (!cancelled) setListLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [route.name, listPage])

  useEffect(() => {
    if (!detailSlug) {
      setDetail(null)
      return
    }
    let cancelled = false
    setDetailLoading(true)
    fetchPortfolioItem(detailSlug)
      .then((item) => {
        if (!cancelled) {
          setDetail(item)
          setDetailError(null)
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setDetail(null)
          setDetailError(error instanceof Error ? error.message : 'Работа не найдена')
        }
      })
      .finally(() => {
        if (!cancelled) setDetailLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [detailSlug])

  if (isAdminRoute(route)) {
    const authed = isAdminAuthenticated()
    const showLogin = route.name === 'adminLogin' || !authed
    return (
      <div className="shell">
        {!showLogin ? <AdminHeader onNavigate={navigate} /> : null}
        <main>
          {showLogin ? <AdminLoginPage onNavigate={navigate} /> : null}
          {authed && route.name === 'admin' ? (
            <AdminPortfolioPage onNavigate={navigate} />
          ) : null}
          {authed && route.name === 'adminNew' ? (
            <AdminItemFormPage itemId={null} onNavigate={navigate} />
          ) : null}
          {authed && route.name === 'adminEdit' ? (
            <AdminItemFormPage itemId={route.id} onNavigate={navigate} />
          ) : null}
          {authed && route.name === 'adminLeads' ? (
            <AdminLeadsPage onNavigate={navigate} />
          ) : null}
        </main>
      </div>
    )
  }

  return (
    <div className="shell">
      <Header currentPath={path} onNavigate={navigate} />
      <main>
        {route.name === 'home' ? (
          <HomePage items={homeItems} loading={homeLoading} error={homeError} onNavigate={navigate} />
        ) : null}
        {route.name === 'portfolio' ? (
          <PortfolioPage
            data={list}
            loading={listLoading}
            error={listError}
            onPage={setListPage}
            onNavigate={navigate}
          />
        ) : null}
        {route.name === 'portfolioItem' ? (
          <PortfolioDetailPage
            item={detail}
            loading={detailLoading}
            error={detailError}
            onNavigate={navigate}
          />
        ) : null}
        {route.name === 'about' ? <AboutPage onNavigate={navigate} /> : null}
        {route.name === 'contact' ? <ContactPage /> : null}
        {route.name === 'notFound' ? (
          <section className="block">
            <h1>Страница не найдена</h1>
            <Link to="/" onNavigate={navigate}>
              На главную
            </Link>
          </section>
        ) : null}
      </main>
      <Footer onNavigate={navigate} />
    </div>
  )
}
