// Blank page for login background
import HomePage from '../pages/home.f7.html';

// Account pages
import MyAccountPage from '../pages/account/my.f7.html';
import ChangePasswordPage from '../pages/account/password.f7.html';
import ResetPasswordPage from '../pages/account/reset.f7.html';

// Course pages
import MyCoursesPage from '../pages/courses/my.f7.html';
import CourseDetailPage from '../pages/courses/detail.f7.html';

// E-Mail password reset
import MailPasswordReset from '../pages/reset/start.f7.html';
import ConfirmMailReset from '../pages/reset/confirm.f7.html';

import NotFoundPage from '../pages/404.f7.html';

var routes = [
  {
    path: '/',
    component: HomePage,
  },
  {
    path: '/account',
    component: MyAccountPage,
  },
  {
    path: '/account/changepassword',
    component: ChangePasswordPage,
  },
  {
    path: '/account/resetpassword',
    component: ResetPasswordPage,
  },
  {
    path: '/courses',
    component: MyCoursesPage,
  },
  {
    path: '/courses/:id',
    component: CourseDetailPage,
  },
  {
    path: '/mailreset',
    component: MailPasswordReset,
  },
  {
    path: '/confirmreset/:token',
    component: ConfirmMailReset,
  },
  {
    path: '(.*)',
    component: NotFoundPage,
  },
];

export default routes;
