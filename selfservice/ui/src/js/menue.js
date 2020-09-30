/*
 Menue
 © 2020 Johannes Kreutz
 */

// Import libraries
import Swal from 'sweetalert2';

// Import modules
import api from './api.js';

// Module definition
let menue = {
    entries: [
        ["Mein Account","/account",["usermgmt"],
            [
                ["Passwort ändern","/account/changepassword"]
            ]
        ],
        ["Meine Kurse","/courses",["usermgmt"]],
    ],
    currentUserHasPermission: function(wanted) {
      if (wanted.includes("*")) {
        return true;
      }
      for (const permission of wanted) {
        if (window.currentUserPermissions.includes(permission)) {
          return true;
        }
      }
      return false;
    },
    rebuild: function() {
      if (window.isLoggedIn) {
        document.getElementById("menue").innerHTML = "";
        for (const element of this.entries) {
          if (this.currentUserHasPermission(element[2])) {
            document.getElementById("menue").innerHTML += "<li id=\"menu-" + element[0] + "\" class=\"menu-item\"><a href=\"#\" onclick=\"window.app.views.main.router.navigate('" + element[1] + "')\">" + element[0] + "</a></li>";
            if (element.length > 3) {
              for (const subelement of element[3]) {
                document.getElementById("menue").innerHTML += "<li id=\"menu-" + subelement[0] + "\" class=\"menu-item\"><a href=\"#\" onclick=\"window.app.views.main.router.navigate('" + subelement[1] + "')\" class=\"subnav\">" + subelement[0] + "</a></li>";
              }
            }
          }
        }
        document.getElementById("menue").innerHTML += "<li class=\"menu-item\"><a href=\"#\" id=\"logout\">Logout</a></li>";
        document.getElementById("logout").addEventListener("click", function(e) {
          this.logout();
        }.bind(this));
      }
    },
    logout: function() {
      api.send("/api/logout", "POST", {}).then(function(response) {
        window.location.reload();
      }.bind(this))
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
