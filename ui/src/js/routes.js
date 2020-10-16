// Blank page for login background
import HomePage from '../pages/home.f7.html';

// Account pages
import MyAccountPage from '../pages/account/my.f7.html';
import ChangePasswordPage from '../pages/account/password.f7.html';

// Course pages
import MyCoursesPage from '../pages/courses/my.f7.html';
import CourseDetailPage from '../pages/courses/detail.f7.html';

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
    path: '/courses',
    component: MyCoursesPage,
  },
  {
    path: '/courses/:id',
    component: CourseDetailPage,
  },
  {
    path: '(.*)',
    component: NotFoundPage,
  },
];

export default routes;
