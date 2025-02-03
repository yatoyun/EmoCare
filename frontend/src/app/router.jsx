import { useQueryClient } from '@tanstack/react-query';
import { useMemo } from 'react';
import { createBrowserRouter } from 'react-router';
import { RouterProvider } from 'react-router/dom';

import { paths } from '@/configs/paths';
import { ProtectedRoute } from '@/lib/auth';

import {
  default as AppRoot,
  ErrorBoundary as AppRootErrorBoundary,
} from './routes/app/root';

const convert = (queryClient) => (m) => {
  const { clientLoader, clientAction, default: Component, ...rest } = m;
  return {
    ...rest,
    loader: clientLoader?.(queryClient),
    action: clientAction?.(queryClient),
    Component,
  };
};

export const createAppRouter = (queryClient) =>
  createBrowserRouter([
    {
      path: paths.register.path,
      lazy: () => import('./routes/Register').then(convert(queryClient)).catch((error) => {
        console.error('Error loading Register route:', error);
      }),
    },
    {
      path: paths.login.path,
      lazy: () => import('./routes/Login').then(convert(queryClient)).catch((error) => {
        console.error('Error loading Login route:', error);
      }),
    },
    {
      path: paths.app.root.path,
      element: (
        <ProtectedRoute>
          <AppRoot />
        </ProtectedRoute>
      ),
      ErrorBoundary: AppRootErrorBoundary,
      children: [
        {
          path: paths.app.chat.path,
          lazy: () => import('./routes/app/Chat').then(convert(queryClient)).catch((error) => {
            console.error('Error loading Chat route:', error);
          }),
        },
        {
          path: paths.app.statistics.path,
          lazy: () => import('./routes/app/Statistics').then(convert(queryClient)).catch((error) => {
            console.error('Error loading Statistics route:', error);
          }),
        },
      ],
    },
    {
      path: '*',
      lazy: () => import('./routes/not-found').then(convert(queryClient)).catch((error) => {
        console.error('Error loading Not Found route:', error);
      }),
    },
  ]);

export const AppRouter = () => {
  const queryClient = useQueryClient();

  const router = useMemo(() => createAppRouter(queryClient), [queryClient]);

  return <RouterProvider router={router} />;
};
