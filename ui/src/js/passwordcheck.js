/*
 * Password check JS for PhilleConnect Backend
 * © 2020 - 2021 Johannes Kreutz.
 */
let passwordcheck = {
  checkEquality: function(p1, p2) {
    return p1 === p2;
  },
  check8OrMore: function(p1) {
    return p1.length >= 8;
  },
  checkLowercase: function(p1) {
    return /[a-z]/.test(p1);
  },
  checkUppercase: function(p1) {
    return /[A-Z]/.test(p1);
  },
  checkNumber: function(p1) {
    return /[0-9]/.test(p1);
  },
}

export default passwordcheck;
