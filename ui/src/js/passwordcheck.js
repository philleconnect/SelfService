/*
 * Password check JS by Johannes Kreutz for PhilleConnect Backend
 * © 2020 Johannes Kreutz.
 */
let passwordcheck = {
  check: function() {
    if (this.checkEquality()) {
      document.getElementById("same").classList.remove("nodisplay");
      document.getElementById("not-same").classList.add("nodisplay");
    } else {
      document.getElementById("same").classList.add("nodisplay");
      document.getElementById("not-same").classList.remove("nodisplay");
    }
    if (this.check8OrMore()) {
      document.getElementById("length-valid").classList.remove("nodisplay");
      document.getElementById("length-invalid").classList.add("nodisplay");
    } else {
      document.getElementById("length-valid").classList.add("nodisplay");
      document.getElementById("length-invalid").classList.remove("nodisplay");
    }
    if (this.checkLowercase()) {
      document.getElementById("lowercase-valid").classList.remove("nodisplay");
      document.getElementById("lowercase-invalid").classList.add("nodisplay");
    } else {
      document.getElementById("lowercase-valid").classList.add("nodisplay");
      document.getElementById("lowercase-invalid").classList.remove("nodisplay");
    }
    if (this.checkUppercase()) {
      document.getElementById("uppercase-valid").classList.remove("nodisplay");
      document.getElementById("uppercase-invalid").classList.add("nodisplay");
    } else {
      document.getElementById("uppercase-valid").classList.add("nodisplay");
      document.getElementById("uppercase-invalid").classList.remove("nodisplay");
    }
    if (this.checkNumber()) {
      document.getElementById("number-valid").classList.remove("nodisplay");
      document.getElementById("number-invalid").classList.add("nodisplay");
    } else {
      document.getElementById("number-valid").classList.add("nodisplay");
      document.getElementById("number-invalid").classList.remove("nodisplay");
    }
  },
  checkEquality: function() {
    return document.getElementById("password1").value === document.getElementById("password2").value;
  },
  check8OrMore: function() {
    return document.getElementById("password1").value.length >= 8;
  },
  checkLowercase: function() {
    return /[a-z]/.test(document.getElementById("password1").value);
  },
  checkUppercase: function() {
    return /[A-Z]/.test(document.getElementById("password1").value);
  },
  checkNumber: function() {
    return /[0-9]/.test(document.getElementById("password1").value);
  },
}

export default passwordcheck;
