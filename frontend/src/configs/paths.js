export const paths = {
  register: {
    path: '/register',
    getHref: (redirectTo) =>
      `/register${redirectTo ? `?redirectTo=${encodeURIComponent(redirectTo)}` : ''}`,
  },
  login: {
    path: '/login',
    getHref: (redirectTo) =>
      `/login${redirectTo ? `?redirectTo=${encodeURIComponent(redirectTo)}` : ''}`,
  },
  app: {
    root: {
      path: '/app',
      getHref: () => '/app',
    },
    chat: {
      path: 'chat',
      getHref: () => '/app/chat',
    },
    statistics: {
      path: 'statistics',
      getHref: () => '/app/statistics',
    },
  }
};