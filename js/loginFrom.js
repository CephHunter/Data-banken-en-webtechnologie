$('document').ready(function () {

    $('#login-form-link').on('click', function (e) {
        $('#login-form').delay(100).fadeIn(100);
        $('#register-form').fadeOut(100);
        $('#register-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });
    $('#register-form-link').on('click', function (e) {
        $('#register-form').delay(100).fadeIn(100);
        $('#login-form').fadeOut(100);
        $('#login-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });

    let password = $('#register-form #password');
    let confirm_password = $('#register-form #confirm-password');

    function validatePassword() {
        if (password.val() != confirm_password.val()) {
          confirm_password[0].setCustomValidity("Passwords Don't Match");
        } else {
          confirm_password[0].setCustomValidity('');
        }
      }
      
      password.change(validatePassword);
      confirm_password.keyup(validatePassword);
});