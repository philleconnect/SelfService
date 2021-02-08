import $ from 'dom7';
import Framework7 from 'framework7';

// Import F7 components
import Form from 'framework7/components/form';

Framework7.use([Form]);

// Import Icons and App Custom Styles
import '../css/app.css';
import '../css/diverse.css';
import '../css/icons.css';
import '../css/input.css';
import '../css/preloader.css';
import '../css/responsivenav.css';
import '../css/table.css';
import '../css/progress.css';
import '../css/hamburgers.min.css';

// Import libraries
import Swal from 'sweetalert2';

// Import Routes
import routes from './routes.js';

// Import JS Modules
import api from './api.js';
import login from './login.js';
import menue from './menue.js';
import timeout from './timeout.js';
import mobilemenu from './mobile-menu.js';
import my from './my.js';

import './mobile-menu-scrolling.js';

// Import main app component
import App from '../app.f7.html';

my.app = new Framework7({
  name: 'PhilleConnect SelfService', // App name
  el: '#app', // App root element
  component: App, // App main component

  // App routes
  routes: routes,

  // Events
  on: {
    init: () => {
      // Create main view
      let mainView = my.app.views.create(".view-main", {
        animate: false,
        preloadPreviousPage: false,
        browserHistory: true,
        browserHistoryAnimate: false,
        browserHistorySeparator: "#page",
        removeElements: false
      })
      // Start app
      let location = window.location.href;
      if (location.includes("confirmreset")) {
        let token = location.split("/confirmreset/")[1];
        mainView.router.navigate("/confirmreset/" + token);
      } else if (!location.includes("mailreset") && location.includes("#page")) {
        Swal.fire({
          title: "Session prüfen...",
          didOpen: () => {
            Swal.showLoading();
            api.send("/api/login/check", "GET", {}).then((response) => {
              my.isLoggedIn = true;
              response = JSON.parse(response);
              my.currentUserPermissions = response.permissions;
              my.currentUserGroups = response.groups;
              Swal.close();
              menue.rebuild();
              menue.markActive(mainView.router.currentPageEl.dataset.name);
              timeout.resetClock();
            });
          }
        });
      } else if (!location.includes("mailreset")) {
        login.show();
      }
    },
    pageInit: (page) => {
      if (my.isLoggedIn) {
        timeout.resetClock();
        menue.markActive(page.name);
      }
    }
  }
});

// Make the back button work
window.onpopstate = (event) => {
  if (event.state) {
    app.views.main.router.back();
  }
}
