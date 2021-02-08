/*
 Menue
 © 2020 - 2021 Johannes Kreutz
 */

// Import libraries
import Swal from 'sweetalert2';
import DOMPurify from 'dompurify';

// Import modules
import api from './api.js';
import my from './my.js';
import mobilemenu from './mobile-menu.js';

// Module definition
let menue = {
  entries: [
    ["Mein Account","/account",["*"],
      [
        ["Passwort ändern","/account/changepassword"],
        ["Schülerpasswort zurücksetzen","/account/resetpassword",["teachers"]]
      ]
    ],
    ["Meine Kurse","/courses",["*"]],
  ],
  currentUserHasPermission: function(wanted) {
    if (wanted.includes("*")) {
      return true;
    }
    for (const permission of wanted) {
      if (my.currentUserPermissions.includes(permission)) {
        return true;
      }
    }
    return false;
  },
  currentUserIsMemberOf: function(wanted) {
    if (wanted.includes("*")) {
      return true;
    }
    for (const group of wanted) {
      if (my.currentUserGroups.includes(group)) {
        return true;
      }
    }
    return false;
  },
  rebuild: function() {
    if (my.isLoggedIn) {
      document.getElementById("menue").innerHTML = "";
      for (const element of this.entries) {
        if (this.currentUserHasPermission(element[2])) {
          document.getElementById("menue").innerHTML += "<li id=\"menu-" + DOMPurify.sanitize(element[0]) + "\" class=\"menu-item\"><a href=\"#\" data-destination=\"" + DOMPurify.sanitize(element[1]) + "\" class=\"menu-link\">" + DOMPurify.sanitize(element[0]) + "</a></li>";
          if (element.length > 3) {
            for (const subelement of element[3]) {
              if (subelement[2] == null || this.currentUserIsMemberOf(subelement[2])) {
                document.getElementById("menue").innerHTML += "<li id=\"menu-" + DOMPurify.sanitize(subelement[0]) + "\" class=\"menu-item\"><a href=\"#\" data-destination=\"" + DOMPurify.sanitize(subelement[1]) + "\" class=\"menu-link subnav\">" + DOMPurify.sanitize(subelement[0]) + "</a></li>";
              }
            }
          }
        }
      }
      document.getElementById("menue").innerHTML += "<li class=\"menu-item\"><a href=\"#\" id=\"logout\">Logout</a></li>";
      document.getElementById("logout").addEventListener("click", function(e) {
        this.logout();
      }.bind(this));
      for (const element of document.getElementsByClassName("menu-link")) {
        element.addEventListener("click", function(e) {
          this.menuElementClick(e.target.dataset.destination);
        }.bind(this));
      }
    }
  },
  menuElementClick: function(destination) {
    mobilemenu.close();
    my.app.views.main.router.navigate(destination);
  },
  logout: function() {
    api.send("/api/logout", "POST", {}).then(function(response) {
      window.location.href = "/";
    });
  },
  markActive: function(currentPageName) {
    for (const element of document.getElementsByClassName("menu-item")) {
      if (element.id == "menu-" + currentPageName) {
        element.classList.add("active");
      } else {
        element.classList.remove("active");
      }
    }
  }
}

export default menue;
