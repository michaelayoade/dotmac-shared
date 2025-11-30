/**
 * @fileoverview RBAC (Role-Based Access Control) package for DotMac platform
 * Provides React components and hooks for permission-based UI rendering
 */
export interface Role {
    id: string;
    name: string;
    permissions: string[];
}
export interface Permission {
    id: string;
    resource: string;
    action: string;
}
export interface User {
    id: string;
    roles: Role[];
    permissions: Permission[] | undefined;
}
export declare const usePermissions: () => {
    hasPermission: (permission: string) => boolean;
    hasRole: (role: string) => boolean;
};
export declare const useRBAC: () => {
    canAccess: (resource: string, action: string) => boolean;
    hasPermission: (permission: string) => boolean;
    hasRole: (role: string) => boolean;
};
export declare const checkPermission: (user: User, permission: string) => boolean;
declare const RBAC: {
    usePermissions: () => {
        hasPermission: (permission: string) => boolean;
        hasRole: (role: string) => boolean;
    };
    useRBAC: () => {
        canAccess: (resource: string, action: string) => boolean;
        hasPermission: (permission: string) => boolean;
        hasRole: (role: string) => boolean;
    };
    checkPermission: (user: User, permission: string) => boolean;
};
export default RBAC;
//# sourceMappingURL=index.d.ts.map