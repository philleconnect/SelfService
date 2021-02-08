/*
 Login-Engine
 © 2020 - 2021 Johannes Kreutz
 */

// Import libraries
import Swal from 'sweetalert2'

// Import modules
import api from './api.js';
import errormsg from './errormessages.js';
import menue from './menue.js';
import preloader from './preloader.js';
import my from './my.js';

// Module definition
let login = {
  show: () => {
    document.getElementById("app").classList.add("login-shown");
    preloader.hide();
    Swal.fire({
      title: 'Bitte Nutzerdaten eingeben.',
      html: '<input type="text" id="swal-input1" placeholder="Nutzername" class="swal2-input"/><input type="password" id="swal-input2" placeholder="Passwort" class="swal2-input"/><br /><a href="#" class="nodisplay" id="reset-link" tabindex="999999">Passwort vergessen</a>',
      showCancelButton: false,
      confirmButtonText: 'Anmelden',
      showLoaderOnConfirm: true,
      allowOutsideClick: false,
      allowEscapeKey: false,
      willOpen: () => {
        document.getElementById("reset-link").addEventListener("click", function(e) {
          document.getElementById("app").classList.remove("login-shown");
          my.app.views.main.router.navigate("/mailreset");
        });
        api.send("/api/permissions/resetenabled", "GET", {}).then((response) => {
          if (response == "ENABLED") {
            document.getElementById("reset-link").classList.remove("nodisplay");
          }
        });
      },
      preConfirm: () => {
        return new Promise((resolve) => {
          if (document.getElementById("swal-input1").value == "" || document.getElementById("swal-input2").value == "") {
            Swal.showValidationMessage('Bitte geben Sie Nutzername und Passwort ein.');
            Swal.hideLoading();
          } else {
            login.login();
          }
        })
      }
    });
  },
  login: () => {
    my.isLoggedIn = false;
    api.send("/api/login", "POST", {uname: document.getElementById("swal-input1").value, passwd: document.getElementById("swal-input2").value}).then((response) => {
      response = JSON.parse(response);
      if (response.status == "ERR_TOO_MANY_FAILED_ATTEMPTS" || response.timeout > 0) {
        Swal.close();
        let timerInterval;
        let title = response.status == "ERR_TOO_MANY_FAILED_ATTEMPTS" ? "Zu viele fehlgeschlagene Anmeldeversuche." : "Anmeldedaten falsch.";
        Swal.fire({
          title: title,
          html: "Bitte versuche es in <b id=\"secs\"></b> Sekunden erneut.",
          timerProgressBar: true,
          timer: response.timeout * 1000,
          showCancelButton: false,
          showConfirmButton: false,
          allowOutsideClick: false,
          allowEscapeKey: false,
          icon: 'info',
          didOpen: () => {
            timerInterval = setInterval(() => {
              let timerPure = Math.round(Swal.getTimerLeft() / 1000);
              document.getElementById("secs").innerHTML = timerPure;
            }, 100)
          },
          willClose: () => {
            clearInterval(timerInterval)
          }
        }).then(() => {
          login.show();
        })
      } else if (response.status == "SUCCESS") {
        my.isLoggedIn = true;
        document.getElementById("app").classList.remove("login-shown");
        my.currentUserPermissions = response.permissions;
        my.currentUserGroups = response.groups;
        Swal.close();
        preloader.hide();
        menue.rebuild();
        my.app.views.main.router.navigate("/account", {reloadAll: true});
      }
    }, (error) => {
      errormsg.fire(error);
    });
  }
}

export default login;
