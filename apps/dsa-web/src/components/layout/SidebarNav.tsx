import React, { useEffect, useState } from 'react';
import { Activity, BarChart3, Bell, BriefcaseBusiness, Gauge, Home, LogOut, MessageSquareQuote, Search, Settings2 } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { ALPHASIFT_CONFIG_CHANGED_EVENT, SYSTEM_CONFIG_CHANGED_EVENT, alphasiftApi } from '../../api/alphasift';
import { useAuth } from '../../contexts/AuthContext';
import { useAgentChatStore } from '../../stores/agentChatStore';
import { useUiLanguage } from '../../contexts/UiLanguageContext';
import type { UiTextKey } from '../../i18n/uiText';
import { cn } from '../../utils/cn';
import { ConfirmDialog } from '../common/ConfirmDialog';
import { StatusDot } from '../common/StatusDot';
import { UiLanguageToggle } from '../i18n/UiLanguageToggle';
import { ThemeToggle } from '../theme/ThemeToggle';

type SidebarNavProps = {
  collapsed?: boolean;
  onNavigate?: () => void;
  variant?: 'default' | 'rail';
};

type NavItem = {
  key: string;
  labelKey: UiTextKey;
  to: string;
  icon: React.ComponentType<{ className?: string }>;
  exact?: boolean;
  badge?: 'completion';
};

const NAV_ITEMS: NavItem[] = [
  { key: 'home', labelKey: 'layout.nav.home', to: '/', icon: Home, exact: true },
  { key: 'chat', labelKey: 'layout.nav.chat', to: '/chat', icon: MessageSquareQuote, badge: 'completion' },
  { key: 'screening', labelKey: 'layout.nav.screening', to: '/screening', icon: Search },
  { key: 'portfolio', labelKey: 'layout.nav.portfolio', to: '/portfolio', icon: BriefcaseBusiness },
  { key: 'decision-signals', labelKey: 'layout.nav.decisionSignals', to: '/decision-signals', icon: Activity },
  { key: 'backtest', labelKey: 'layout.nav.backtest', to: '/backtest', icon: BarChart3 },
  { key: 'alerts', labelKey: 'layout.nav.alerts', to: '/alerts', icon: Bell },
  { key: 'usage', labelKey: 'layout.nav.usage', to: '/usage', icon: Gauge },
  { key: 'settings', labelKey: 'layout.nav.settings', to: '/settings', icon: Settings2 },
];

export const SidebarNav: React.FC<SidebarNavProps> = ({ collapsed = false, onNavigate, variant = 'default' }) => {
  const { authEnabled, logout } = useAuth();
  const { t } = useUiLanguage();
  const completionBadge = useAgentChatStore((state) => state.completionBadge);
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);
  const [showAlphaSiftNav, setShowAlphaSiftNav] = useState(false);

  useEffect(() => {
    let active = true;
    const refreshAlphaSiftStatus = async () => {
      try {
        const status = await alphasiftApi.getStatus();
        if (active) setShowAlphaSiftNav(status.enabled);
      } catch {
        if (active) setShowAlphaSiftNav(false);
      }
    };
    void refreshAlphaSiftStatus();
    window.addEventListener(ALPHASIFT_CONFIG_CHANGED_EVENT, refreshAlphaSiftStatus);
    window.addEventListener(SYSTEM_CONFIG_CHANGED_EVENT, refreshAlphaSiftStatus);
    return () => {
      active = false;
      window.removeEventListener(ALPHASIFT_CONFIG_CHANGED_EVENT, refreshAlphaSiftStatus);
      window.removeEventListener(SYSTEM_CONFIG_CHANGED_EVENT, refreshAlphaSiftStatus);
    };
  }, []);

  const navItems = showAlphaSiftNav ? NAV_ITEMS : NAV_ITEMS.filter((item) => item.key !== 'screening');
  const isRail = variant === 'rail';

  return (
    <div className="flex h-full flex-col px-3 py-4">
      <div className={cn(
        'flex flex-col items-center',
        isRail ? 'mb-3 gap-1 pt-5' : 'mb-5 gap-3 pt-8'
      )}>
        <div className={cn(
          'flex items-center justify-center bg-primary-gradient shadow-[0_12px_28px_var(--nav-brand-shadow)]',
          isRail ? 'h-9 w-9 rounded-[1rem]' : 'h-[100px] w-[100px] rounded-3xl'
        )}>
          <img src="/favicon-v2.svg" alt="如意金股" className={isRail ? 'h-[19px] w-[19px]' : 'h-[60px] w-[60px]'} />
        </div>
        {!collapsed && (
          <div className="flex flex-col items-center gap-1.5">
            <p className={cn('text-center font-bold tracking-wide text-foreground', isRail ? 'text-[0.7rem] leading-none' : 'text-2xl')}>如意金股</p>
            <p className={cn('text-center font-medium text-muted-text', isRail ? 'text-[0.55rem] leading-none' : 'text-sm')}>RuyiDailyStockAnalysis</p>
            <p className={cn('text-center text-foreground opacity-50', isRail ? 'text-[0.5rem] leading-none' : 'text-xs')}>柯冰妍</p>
          </div>
        )}
      </div>

      <nav className={cn('flex flex-col gap-0.5 flex-1')} aria-label={t('layout.mainNav')}>
        {navItems.map(({ key, labelKey, to, icon: Icon, exact, badge }) => {
          const label = t(labelKey);
          return (
            <NavLink
              key={key}
              to={to}
              end={exact}
              onClick={onNavigate}
              aria-label={label}
              className={({ isActive }) =>
                cn(
                  'group relative flex h-[var(--nav-item-height)] w-full items-center overflow-hidden rounded-2xl border border-transparent text-sm leading-none text-secondary-text transition-all',
                  'gap-3 px-[var(--nav-item-padding-x)]',
                  'hover:bg-[var(--nav-hover-bg)] hover:text-foreground',
                  isActive && 'border-[var(--nav-active-border)] bg-[var(--nav-active-bg)] font-medium text-[hsl(var(--primary))]'
                )
              }
            >
              {({ isActive }) => (
                <>
                  <Icon className={cn('h-5 w-5 shrink-0', isActive && 'text-[var(--nav-icon-active)]')} />
                  {!collapsed && <span className="truncate">{label}</span>}
                  {badge === 'completion' && completionBadge && (
                    <StatusDot tone="info" data-testid="chat-completion-badge" className="absolute right-3 border-2 border-background shadow-[0_0_10px_var(--nav-indicator-shadow)]" aria-label={t('layout.newChatMessage')} />
                  )}
                </>
              )}
            </NavLink>
          );
        })}

        <ThemeToggle variant={isRail ? 'rail' : 'nav'} collapsed={collapsed} wrapperClassName="w-full"
          triggerClassName="group relative flex h-[var(--nav-item-height)] w-full items-center overflow-hidden rounded-2xl border border-transparent text-sm leading-none text-secondary-text transition-all gap-3 px-[var(--nav-item-padding-x)] hover:bg-[var(--nav-hover-bg)] hover:text-foreground"
          triggerActiveClassName="border-[var(--nav-active-border)] bg-[var(--nav-active-bg)] font-medium text-[hsl(var(--primary))]"
          iconClassName="h-5 w-5 shrink-0" labelClassName="truncate" />
        <UiLanguageToggle variant={isRail ? 'rail' : 'nav'} collapsed={collapsed} wrapperClassName="w-full"
          triggerClassName="group relative flex h-[var(--nav-item-height)] w-full items-center overflow-hidden rounded-2xl border border-transparent text-sm leading-none text-secondary-text transition-all gap-3 px-[var(--nav-item-padding-x)] hover:bg-[var(--nav-hover-bg)] hover:text-foreground"
          triggerActiveClassName="border-[var(--nav-active-border)] bg-[var(--nav-active-bg)] font-medium text-[hsl(var(--primary))]"
          iconClassName="h-5 w-5 shrink-0" labelClassName="truncate" />
      </nav>

      {authEnabled && (
        <button type="button" onClick={() => setShowLogoutConfirm(true)}
          className="group relative flex h-[var(--nav-item-height)] w-full items-center overflow-hidden rounded-2xl border border-transparent text-sm leading-none text-secondary-text transition-all gap-3 px-[var(--nav-item-padding-x)] hover:bg-[var(--nav-hover-bg)] hover:text-foreground mt-5">
          <LogOut className="h-5 w-5 shrink-0" />
          {!collapsed && <span className="truncate">{t('layout.logout')}</span>}
        </button>
      )}

      <ConfirmDialog isOpen={showLogoutConfirm} title={t('layout.logoutTitle')} message={t('layout.logoutMessage')}
        confirmText={t('layout.logoutConfirm')} cancelText={t('common.cancel')} isDanger
        onConfirm={() => { setShowLogoutConfirm(false); onNavigate?.(); void logout(); }}
        onCancel={() => setShowLogoutConfirm(false)} />
    </div>
  );
};
