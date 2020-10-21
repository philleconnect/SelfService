import $$ from 'dom7';
import Framework7 from 'framework7/framework7.esm.bundle.js';

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

import './mobile-menu-scrolling.js';

// Import main app component
import App from '../app.f7.html';

window.app = new Framework7({
  root: '#app', // App root element
  component: App, // App main component

  name: 'PhilleConnect SelfService', // App name

  // App routes
  routes: routes,

  // Events
  on: {
    pageInit: function(page) {
      if (window.isLoggedIn) {
        timeout.resetClock();
        menue.markActive(page.name);
      }
    }
  }
});

let mainView = window.app.views.create(".view-main", {
  animate: false,
  preloadPreviousPage: false,
  pushState: true,
  pushStateAnimate: false,
  pushStateSeparator: "#page",
  removeElements: false
})

// Make the back button work
window.onpopstate = function(event) {
  if (event.state) {
    window.app.views.main.router.back();
  }
}

// Global login state
window.isLoggedIn = false;
window.currentUserPermissions = [];

// Start app
let location = window.location.href;
if (location.includes("mailreset")) {
  window.app.views.main.router.navigate("/mailreset");
} else if (location.includes("confirmreset")) {
  let token = location.split("/confirmreset/")[1];
  window.app.views.main.router.navigate("/confirmreset/" + token);
} else {
  login.show();
}

window.mobilemenu = mobilemenu;
