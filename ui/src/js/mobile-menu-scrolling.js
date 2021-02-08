/*
 * Add a background to the mobile menu toggle if the page is scrolled (blurry if supported)
 * © 2018 - 2021 Johannes Kreutz. All rights reserved.
 */
window.onload = () => {
  window.onscroll = () => {
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
    if (scrollTop <= 0) {
      Array.prototype.forEach.call(document.getElementsByClassName('mobile-menu-toggle'), (element) => {
        element.classList.remove('scrolled');
      });
    } else {
      Array.prototype.forEach.call(document.getElementsByClassName('mobile-menu-toggle'), (element) => {
        element.classList.add('scrolled');
      });
    }
  }
}
