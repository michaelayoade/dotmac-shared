// src/UniversalProviders.tsx
import * as React3 from "react";
import { QueryClientProvider } from "@tanstack/react-query";

// src/components/ErrorBoundary.tsx
import * as React from "react";
import { jsx, jsxs } from "react/jsx-runtime";
var ErrorBoundary = class extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError(error) {
    return {
      hasError: true,
      error
    };
  }
  componentDidCatch(error, errorInfo) {
    this.setState({ errorInfo });
    this.logError(error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }
  logError = (error, errorInfo) => {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
    const portalContext = {
      portal: this.props.portal,
      timestamp: (/* @__PURE__ */ new Date()).toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href
    };
    if (typeof window !== "undefined" && window.gtag) {
      window.gtag("event", "exception", {
        description: error.message,
        fatal: true,
        custom_map: portalContext
      });
    }
  };
  resetError = () => {
    this.setState({ hasError: false, error: void 0, errorInfo: void 0 });
  };
  render() {
    if (this.state.hasError) {
      const FallbackComponent = this.getFallbackComponent();
      return /* @__PURE__ */ jsx(
        FallbackComponent,
        {
          error: this.state.error,
          errorInfo: this.state.errorInfo,
          resetError: this.resetError,
          portal: this.props.portal
        }
      );
    }
    return this.props.children;
  }
  getFallbackComponent() {
    if (typeof this.props.fallback === "function") {
      return this.props.fallback;
    }
    switch (this.props.portal) {
      case "admin":
        return AdminErrorFallback;
      case "customer":
        return CustomerErrorFallback;
      case "reseller":
        return ResellerErrorFallback;
      case "technician":
        return TechnicianErrorFallback;
      case "management":
        return ManagementErrorFallback;
      default:
        return DefaultErrorFallback;
    }
  }
};
function DefaultErrorFallback({ error, resetError, portal }) {
  return /* @__PURE__ */ jsx("div", { className: "min-h-screen flex items-center justify-center bg-gray-50", children: /* @__PURE__ */ jsxs("div", { className: "max-w-md w-full bg-white shadow-lg rounded-lg p-6", children: [
    /* @__PURE__ */ jsx("div", { className: "flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full mb-4", children: /* @__PURE__ */ jsx(
      "svg",
      {
        className: "w-6 h-6 text-red-600",
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        children: /* @__PURE__ */ jsx(
          "path",
          {
            strokeLinecap: "round",
            strokeLinejoin: "round",
            strokeWidth: "2",
            d: "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
          }
        )
      }
    ) }),
    /* @__PURE__ */ jsx("h1", { className: "text-xl font-semibold text-gray-900 text-center mb-2", children: "Something went wrong" }),
    /* @__PURE__ */ jsx("p", { className: "text-gray-600 text-center mb-6", children: "We're sorry, but something unexpected happened. Please try refreshing the page." }),
    /* @__PURE__ */ jsxs("div", { className: "space-y-3", children: [
      /* @__PURE__ */ jsx(
        "button",
        {
          onClick: resetError,
          className: "w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
          children: "Try again"
        }
      ),
      /* @__PURE__ */ jsx(
        "button",
        {
          onClick: () => window.location.reload(),
          className: "w-full px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2",
          children: "Refresh page"
        }
      )
    ] }),
    process.env["NODE_ENV"] === "development" && /* @__PURE__ */ jsxs("details", { className: "mt-6 p-4 bg-red-50 rounded-md", children: [
      /* @__PURE__ */ jsx("summary", { className: "cursor-pointer text-sm font-medium text-red-800", children: "Error Details (Development)" }),
      /* @__PURE__ */ jsxs("pre", { className: "mt-2 text-xs text-red-700 whitespace-pre-wrap", children: [
        error.message,
        error.stack
      ] })
    ] })
  ] }) });
}
function AdminErrorFallback(props) {
  return /* @__PURE__ */ jsx(DefaultErrorFallback, { ...props });
}
function CustomerErrorFallback(props) {
  return /* @__PURE__ */ jsx(DefaultErrorFallback, { ...props });
}
function ResellerErrorFallback(props) {
  return /* @__PURE__ */ jsx(DefaultErrorFallback, { ...props });
}
function TechnicianErrorFallback(props) {
  return /* @__PURE__ */ jsx(DefaultErrorFallback, { ...props });
}
function ManagementErrorFallback(props) {
  return /* @__PURE__ */ jsx(DefaultErrorFallback, { ...props });
}

// src/components/ThemeProvider.tsx
import { Fragment, jsx as jsx2 } from "react/jsx-runtime";
function ThemeProvider({ children, portal }) {
  const variant = portal === "admin" || portal === "management" ? "management" : portal === "reseller" ? "reseller" : portal === "technician" ? "technician" : "customer";
  return /* @__PURE__ */ jsx2(Fragment, { children });
}

// src/components/NotificationProvider.tsx
import { Fragment as Fragment2, jsx as jsx3 } from "react/jsx-runtime";
function NotificationProvider({
  children,
  maxNotifications,
  defaultDuration,
  position
}) {
  return /* @__PURE__ */ jsx3(Fragment2, { children });
}

// src/components/FeatureProvider.tsx
import { createContext, useContext } from "react";
import { jsx as jsx4 } from "react/jsx-runtime";
var FeatureContext = createContext({});
function FeatureProvider({
  children,
  features = {}
}) {
  return /* @__PURE__ */ jsx4(FeatureContext.Provider, { value: features, children });
}

// src/components/TenantProvider.tsx
import { Fragment as Fragment3, jsx as jsx5 } from "react/jsx-runtime";
function TenantProvider({ children }) {
  return /* @__PURE__ */ jsx5(Fragment3, { children });
}

// src/utils/queryClients.ts
import { QueryClient } from "@tanstack/react-query";
function createPortalQueryClient(_portal) {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 5 * 60 * 1e3,
        refetchOnWindowFocus: false,
        retry: (failureCount, error) => {
          if (error?.status === 401 || error?.status === 403) return false;
          return failureCount < 3;
        }
      }
    }
  });
}

// src/UniversalProviders.tsx
import { jsx as jsx6, jsxs as jsxs2 } from "react/jsx-runtime";
var ReactQueryDevtools = () => null;
var defaultFeatures = {
  notifications: true,
  realtime: false,
  analytics: false,
  offline: false
};
function UniversalProviders({
  children,
  portal,
  features = {},
  tenantVariant = "multi",
  queryClient,
  enableDevtools = process.env["NODE_ENV"] === "development",
  config = {}
}) {
  const client = React3.useMemo(
    () => queryClient || createPortalQueryClient(portal),
    [queryClient, portal]
  );
  const mergedFeatures = React3.useMemo(
    () => ({
      ...defaultFeatures,
      ...features
    }),
    [features]
  );
  const portalConfig = React3.useMemo(() => getPortalConfig(portal, config), [portal, config]);
  return /* @__PURE__ */ jsx6(ErrorBoundary, { portal, fallback: portalConfig.errorFallback, children: /* @__PURE__ */ jsxs2(QueryClientProvider, { client, children: [
    /* @__PURE__ */ jsx6(ThemeProvider, { portal, theme: portalConfig.theme, children: /* @__PURE__ */ jsx6(TenantProvider, { variant: tenantVariant, portal, children: /* @__PURE__ */ jsxs2(FeatureProvider, { features: mergedFeatures, children: [
      mergedFeatures.notifications && /* @__PURE__ */ jsx6(
        NotificationProvider,
        {
          maxNotifications: portalConfig.notifications.max,
          defaultDuration: portalConfig.notifications.duration,
          position: portalConfig.notifications.position
        }
      ),
      children
    ] }) }) }),
    enableDevtools && /* @__PURE__ */ jsx6(ReactQueryDevtools, { initialIsOpen: false })
  ] }) });
}
function getPortalConfig(portal, config = {}) {
  const baseAuthConfigs = {
    admin: {
      sessionTimeout: 60 * 60 * 1e3,
      // 1 hour
      enableMFA: true,
      enablePermissions: true,
      requirePasswordComplexity: true,
      maxLoginAttempts: 3,
      lockoutDuration: 30 * 60 * 1e3,
      // 30 minutes
      enableAuditLog: true,
      tokenRefreshThreshold: 5 * 60 * 1e3,
      // 5 minutes
      endpoints: {
        login: "/api/admin/auth/login",
        logout: "/api/admin/auth/logout",
        refresh: "/api/admin/auth/refresh",
        profile: "/api/admin/auth/profile"
      }
    },
    customer: {
      sessionTimeout: 30 * 60 * 1e3,
      // 30 minutes
      enableMFA: false,
      enablePermissions: false,
      requirePasswordComplexity: false,
      maxLoginAttempts: 5,
      lockoutDuration: 10 * 60 * 1e3,
      // 10 minutes
      enableAuditLog: false,
      tokenRefreshThreshold: 2 * 60 * 1e3,
      // 2 minutes
      endpoints: {
        login: "/api/customer/auth/login",
        logout: "/api/customer/auth/logout",
        refresh: "/api/customer/auth/refresh",
        profile: "/api/customer/auth/profile"
      }
    },
    reseller: {
      sessionTimeout: 45 * 60 * 1e3,
      // 45 minutes
      enableMFA: true,
      enablePermissions: true,
      requirePasswordComplexity: true,
      maxLoginAttempts: 3,
      lockoutDuration: 30 * 60 * 1e3,
      // 30 minutes
      enableAuditLog: true,
      tokenRefreshThreshold: 10 * 60 * 1e3,
      // 10 minutes
      endpoints: {
        login: "/api/reseller/auth/login",
        logout: "/api/reseller/auth/logout",
        refresh: "/api/reseller/auth/refresh",
        profile: "/api/reseller/auth/profile"
      }
    },
    technician: {
      sessionTimeout: 8 * 60 * 60 * 1e3,
      // 8 hours (field work)
      enableMFA: false,
      enablePermissions: true,
      requirePasswordComplexity: false,
      maxLoginAttempts: 5,
      lockoutDuration: 5 * 60 * 1e3,
      // 5 minutes
      enableAuditLog: true,
      tokenRefreshThreshold: 30 * 60 * 1e3,
      // 30 minutes
      endpoints: {
        login: "/api/technician/auth/login",
        logout: "/api/technician/auth/logout",
        refresh: "/api/technician/auth/refresh",
        profile: "/api/technician/auth/profile"
      }
    },
    management: {
      sessionTimeout: 2 * 60 * 60 * 1e3,
      // 2 hours
      enableMFA: true,
      enablePermissions: true,
      requirePasswordComplexity: true,
      maxLoginAttempts: 2,
      lockoutDuration: 60 * 60 * 1e3,
      // 1 hour
      enableAuditLog: true,
      tokenRefreshThreshold: 15 * 60 * 1e3,
      // 15 minutes
      endpoints: {
        login: "/api/management/auth/login",
        logout: "/api/management/auth/logout",
        refresh: "/api/management/auth/refresh",
        profile: "/api/management/auth/profile"
      }
    }
  };
  const configs = {
    admin: {
      theme: "professional",
      auth: { ...baseAuthConfigs.admin, ...config.auth },
      notifications: {
        max: config.notificationOptions?.maxNotifications || 5,
        duration: config.notificationOptions?.defaultDuration || 5e3,
        position: "top-right"
      },
      errorFallback: "AdminErrorFallback"
    },
    customer: {
      theme: "friendly",
      auth: { ...baseAuthConfigs.customer, ...config.auth },
      notifications: {
        max: config.notificationOptions?.maxNotifications || 3,
        duration: config.notificationOptions?.defaultDuration || 4e3,
        position: "bottom-right"
      },
      errorFallback: "CustomerErrorFallback"
    },
    reseller: {
      theme: "business",
      auth: { ...baseAuthConfigs.reseller, ...config.auth },
      notifications: {
        max: config.notificationOptions?.maxNotifications || 4,
        duration: config.notificationOptions?.defaultDuration || 6e3,
        position: "top-right"
      },
      errorFallback: "ResellerErrorFallback"
    },
    technician: {
      theme: "mobile",
      auth: { ...baseAuthConfigs.technician, ...config.auth },
      notifications: {
        max: config.notificationOptions?.maxNotifications || 2,
        duration: config.notificationOptions?.defaultDuration || 8e3,
        position: "bottom-center"
      },
      errorFallback: "TechnicianErrorFallback"
    },
    management: {
      theme: "enterprise",
      auth: { ...baseAuthConfigs.management, ...config.auth },
      notifications: {
        max: config.notificationOptions?.maxNotifications || 6,
        duration: config.notificationOptions?.defaultDuration || 7e3,
        position: "top-center"
      },
      errorFallback: "ManagementErrorFallback"
    }
  };
  return configs[portal] || configs.admin;
}

// src/index.ts
import { usePermissions, useRBAC, checkPermission } from "@dotmac/rbac";
var PORTAL_DEFAULTS = {
  customer: {
    features: {
      notifications: true,
      realtime: false,
      analytics: false,
      tenantManagement: true,
      errorHandling: true,
      performanceMonitoring: true
    },
    theme: "customer",
    cacheStrategy: "aggressive"
  },
  admin: {
    features: {
      notifications: true,
      realtime: true,
      analytics: true,
      tenantManagement: true,
      errorHandling: true,
      performanceMonitoring: true
    },
    theme: "admin",
    cacheStrategy: "balanced"
  },
  reseller: {
    features: {
      notifications: true,
      realtime: false,
      analytics: true,
      tenantManagement: false,
      errorHandling: true,
      performanceMonitoring: false
    },
    theme: "reseller",
    cacheStrategy: "conservative"
  },
  technician: {
    features: {
      notifications: false,
      realtime: false,
      analytics: false,
      tenantManagement: false,
      errorHandling: true,
      performanceMonitoring: false
    },
    theme: "technician",
    cacheStrategy: "minimal"
  },
  "management-admin": {
    features: {
      notifications: true,
      realtime: true,
      analytics: true,
      tenantManagement: true,
      errorHandling: true,
      performanceMonitoring: true
    },
    theme: "management",
    cacheStrategy: "aggressive"
  },
  "management-reseller": {
    features: {
      notifications: true,
      realtime: false,
      analytics: true,
      tenantManagement: false,
      errorHandling: true,
      performanceMonitoring: false
    },
    theme: "management-reseller",
    cacheStrategy: "balanced"
  },
  "tenant-portal": {
    features: {
      notifications: true,
      realtime: false,
      analytics: false,
      tenantManagement: true,
      errorHandling: true,
      performanceMonitoring: false
    },
    theme: "tenant",
    cacheStrategy: "conservative"
  }
};
export {
  ErrorBoundary,
  PORTAL_DEFAULTS,
  UniversalProviders,
  checkPermission,
  usePermissions,
  useRBAC
};
