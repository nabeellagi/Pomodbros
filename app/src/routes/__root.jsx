import { createRootRoute, Outlet } from '@tanstack/react-router';
import { TransitionProvider } from '@/transitions/TransitionOverlay';

export const Route = createRootRoute({
  component: () => (
    <TransitionProvider>
      <Outlet />
    </TransitionProvider>
  ),
});