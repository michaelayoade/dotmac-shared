import * as react_jsx_runtime from 'react/jsx-runtime';
import * as React from 'react';
import { QueryClient } from '@tanstack/react-query';
export { Permission, Role, User, checkPermission, usePermissions, useRBAC } from '@dotmac/rbac';

type PortalType = "admin" | "customer" | "reseller" | "technician" | "management";
interface UniversalProviderProps {
    children: React.ReactNode;
    portal: PortalType;
    features?: FeatureFlags;
    tenantVariant?: TenantVariant;
    queryClient?: QueryClient;
    enableDevtools?: boolean;
    config?: {
        apiConfig?: {
            baseUrl?: string;
            timeout?: number;
        };
        queryOptions?: {
            staleTime?: number;
            retry?: (failureCount: number, error: unknown) => boolean;
        };
        notificationOptions?: {
            maxNotifications?: number;
            defaultDuration?: number;
        };
        websocketUrl?: string;
        apiKey?: string;
    };
}
interface FeatureFlags {
    notifications?: boolean;
    realtime?: boolean;
    analytics?: boolean;
    offline?: boolean;
    websocket?: boolean;
    tenantManagement?: boolean;
    errorHandling?: boolean;
    pwa?: boolean;
    toasts?: boolean;
    devtools?: boolean;
}
type TenantVariant = "single" | "multi" | "isp";
/**
 * Universal Provider System
 *
 * Provides a standardized provider architecture across all portals.
 * Eliminates the need for custom provider compositions in each app.
 *
 * Usage:
 * ```tsx
 * <UniversalProviders portal="admin" features={{ realtime: true }}>
 *   <App />
 * </UniversalProviders>
 * ```
 */
declare function UniversalProviders({ children, portal, features, tenantVariant, queryClient, enableDevtools, config, }: UniversalProviderProps): react_jsx_runtime.JSX.Element;

declare global {
    interface Window {
        gtag?: (...args: any[]) => void;
    }
}
interface ErrorBoundaryState {
    hasError: boolean;
    error?: Error;
    errorInfo?: React.ErrorInfo;
}
interface ErrorBoundaryProps {
    children: React.ReactNode;
    portal: PortalType;
    fallback?: string | React.ComponentType<ErrorFallbackProps>;
    onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
}
interface ErrorFallbackProps {
    error: Error;
    errorInfo?: React.ErrorInfo;
    resetError: () => void;
    portal: PortalType;
}
/**
 * Universal Error Boundary with portal-specific fallbacks
 */
declare class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
    constructor(props: ErrorBoundaryProps);
    static getDerivedStateFromError(error: Error): ErrorBoundaryState;
    componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void;
    private logError;
    private resetError;
    render(): string | number | boolean | Iterable<React.ReactNode> | react_jsx_runtime.JSX.Element | null | undefined;
    private getFallbackComponent;
}

/**
 * Universal Provider System for DotMac Frontend Applications
 * Provides standardized provider patterns across all portals
 */

declare const PORTAL_DEFAULTS: {
    readonly customer: {
        readonly features: {
            readonly notifications: true;
            readonly realtime: false;
            readonly analytics: false;
            readonly tenantManagement: true;
            readonly errorHandling: true;
            readonly performanceMonitoring: true;
        };
        readonly theme: "customer";
        readonly cacheStrategy: "aggressive";
    };
    readonly admin: {
        readonly features: {
            readonly notifications: true;
            readonly realtime: true;
            readonly analytics: true;
            readonly tenantManagement: true;
            readonly errorHandling: true;
            readonly performanceMonitoring: true;
        };
        readonly theme: "admin";
        readonly cacheStrategy: "balanced";
    };
    readonly reseller: {
        readonly features: {
            readonly notifications: true;
            readonly realtime: false;
            readonly analytics: true;
            readonly tenantManagement: false;
            readonly errorHandling: true;
            readonly performanceMonitoring: false;
        };
        readonly theme: "reseller";
        readonly cacheStrategy: "conservative";
    };
    readonly technician: {
        readonly features: {
            readonly notifications: false;
            readonly realtime: false;
            readonly analytics: false;
            readonly tenantManagement: false;
            readonly errorHandling: true;
            readonly performanceMonitoring: false;
        };
        readonly theme: "technician";
        readonly cacheStrategy: "minimal";
    };
    readonly "management-admin": {
        readonly features: {
            readonly notifications: true;
            readonly realtime: true;
            readonly analytics: true;
            readonly tenantManagement: true;
            readonly errorHandling: true;
            readonly performanceMonitoring: true;
        };
        readonly theme: "management";
        readonly cacheStrategy: "aggressive";
    };
    readonly "management-reseller": {
        readonly features: {
            readonly notifications: true;
            readonly realtime: false;
            readonly analytics: true;
            readonly tenantManagement: false;
            readonly errorHandling: true;
            readonly performanceMonitoring: false;
        };
        readonly theme: "management-reseller";
        readonly cacheStrategy: "balanced";
    };
    readonly "tenant-portal": {
        readonly features: {
            readonly notifications: true;
            readonly realtime: false;
            readonly analytics: false;
            readonly tenantManagement: true;
            readonly errorHandling: true;
            readonly performanceMonitoring: false;
        };
        readonly theme: "tenant";
        readonly cacheStrategy: "conservative";
    };
};

export { ErrorBoundary, type FeatureFlags, PORTAL_DEFAULTS, type TenantVariant, UniversalProviders };
