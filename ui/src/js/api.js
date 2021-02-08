/*
 API-Request-Engine
 © 2019 - 2021 Johannes Kreutz
 */

// Import libraries
import Swal from 'sweetalert2';

// Import modules
import login from './login.js';
import errormsg from './errormessages.js';
import preloader from './preloader.js';
import my from './my.js';

// Module definition
let api = {
  send: function(url, type, data, disableErrorMessages) {
    url = "https://172.16.0.27:450" + url
    return new Promise(function(resolve, reject) {
      let request = new XMLHttpRequest;
      request.addEventListener("load", function(event) {
        if (disableErrorMessages) {
          resolve(event.target);
        } else {
          if (event.target.status == 401) {
            if (my.isLoggedIn || my.app.views.main.router.url != "/") {
              window.location.href = "/";
            } else {
              Swal.showValidationMessage('Anmeldedaten falsch.');
              Swal.hideLoading();
              resolve(event.target.responseText);
            }
          } else if (event.target.status == 403) {
            if (my.isLoggedIn) {
              Swal.fire({
                title: "Zugriffsfehler",
                text: "Der Account verfügt nicht über die nötigen Berechtigungen für diesen Bereich.",
                icon: "warning"
              })
            } else {
              Swal.showValidationMessage('Anmeldedaten falsch.');
              Swal.hideLoading();
            }
          } else if (event.target.status == 429) {
            if (my.isLoggedIn) {
              Swal.fire({
                title: "Zu viele Anfragen",
                text: "Bitte warte einen Moment unt versuche es erneut.",
                icon: "warning"
              })
            } else {
              Swal.showValidationMessage('Zu viele Anmeldeversuche.');
              Swal.hideLoading();
            }
          } else if (event.target.status == 502) {
            this.fireBackendConnectionError();
          } else if (event.target.status == 404) {
            preloader.hide();
            this.fire404Error();
          } else if (event.target.status >= 400) {
            preloader.hide();
            errormsg.fire(event.target.responseText);
            reject(event.target.responseText);
          } else if (event.target.status == 200 || event.target.status == 201) {
            resolve(event.target.responseText);
          }
        }
      }.bind(this))
      request.addEventListener("error", function(event) {
        if (!disableErrorMessages) {
          this.fireBackendConnectionError();
          reject(event);
        } else {
          resolve(event.target);
        }
      }.bind(this))
      let formData = new FormData();
      for (let key in data) {
        formData.append(key, data[key])
      }
      request.open(type, url, true);
      request.send(formData);
    }.bind(this))
  },
  fireBackendConnectionError: function() {
    Swal.fire({
      title: "Es konnte keine Verbindung zum Backend-Server hergestellt werden.",
      icon: "error",
      showConfirmButton: false,
      allowEscapeKey: false,
      allowOutsideClick: false
    });
  },
  fire404Error: function() {
    Swal.fire({
      title: "Der angeforderte API-Endpunkt konnte nicht gefunden werden.",
      icon: "error",
    });
  }
}

export default api;
