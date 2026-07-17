import type React from 'react';
import { useEffect, useState } from 'react';
import { Menu } from 'lucide-react';
import { Outlet } from 'react-router-dom';
import { Drawer } from '../common/Drawer';
import { SidebarNav } from './SidebarNav';
import { cn } from '../../utils/cn';
import { ThemeToggle } from '../theme/ThemeToggle';
import { UiLanguageToggle } from '../i18n/UiLanguageToggle';
import { useUiLanguage } from '../../contexts/UiLanguageContext';

type ShellProps = {
  children?: React.ReactNode;
};

export const Shell: React.FC<ShellProps> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const collapsed = false;
  const { t } = useUiLanguage();

  useEffect(() => {
    if (!mobileOpen) return undefined;
    const handleResize = () => {
      if (window.innerWidth >= 1024) setMobileOpen(false);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [mobileOpen]);

  return (
    <div className="relative h-dvh w-full overflow-hidden bg-background text-foreground">
      {/* Full-page background image */}
      <div className="pointer-events-none fixed inset-0 z-0">
        <img src="/bg.jpg" alt="" className="h-full w-full object-cover opacity-[0.6]" />
      </div>

      {/* Mobile nav */}
      <div className="pointer-events-none fixed inset-x-0 top-3 z-40 flex items-start justify-between px-3 lg:hidden">
        <button
          type="button"
          onClick={() => setMobileOpen(true)}
          className="pointer-events-auto inline-flex h-10 w-10 items-center justify-center rounded-xl border border-border/70 bg-card/85 text-secondary-text shadow-soft-card backdrop-blur-md transition-colors hover:bg-hover hover:text-foreground"
          aria-label={t('layout.openNav')}
        >
          <Menu className="h-5 w-5" />
        </button>
        <div className="pointer-events-auto flex items-center gap-2">
          <UiLanguageToggle />
          <ThemeToggle />
        </div>
      </div>

      {/* Global semi-transparent cards */}
      <style>{`
        .terminal-card, .gradient-border-card, .home-panel-card, .settings-surface-panel,
        .home-report-hero, .home-insight-card, .chat-bubble-user, .chat-bubble-ai,
        .backtest-table-wrapper, .session-item, [class*="bg-card"]:not(aside)
        {
          background-color: color-mix(in srgb, var(--card) 70%, transparent) !important;
          backdrop-filter: blur(8px) !important;
          -webkit-backdrop-filter: blur(8px) !important;
        }
        .dark .terminal-card, .dark .gradient-border-card, .dark .home-panel-card {{
          background-color: color-mix(in srgb, var(--card) 65%, transparent) !important;
        }}
      `}</style>
      {/* Main layout */}
      <div className="relative z-10 flex h-full w-full">
        <aside
          className={cn(
            'sticky top-0 z-40 hidden h-full shrink-0 overflow-hidden border-r border-[var(--shell-sidebar-border)] bg-card/40 backdrop-blur-md transition-[width] duration-200 lg:flex',
            collapsed ? 'w-[64px]' : 'w-[220px]'
          )}
          aria-label={t('layout.desktopSidebar')}
        >
          <SidebarNav collapsed={collapsed} variant="rail" onNavigate={() => setMobileOpen(false)} />
        </aside>

        <main className="relative min-h-0 min-w-0 flex-1 overflow-hidden bg-background/40 backdrop-blur-[2px] touch-pan-y">
          {children ?? <Outlet />}
        </main>
      </div>

      <Drawer
        isOpen={mobileOpen}
        onClose={() => setMobileOpen(false)}
        title={t('layout.navMenu')}
        width="max-w-xs"
        zIndex={90}
        side="left"
      >
        <SidebarNav onNavigate={() => setMobileOpen(false)} />
      </Drawer>
    </div>
  );
};
