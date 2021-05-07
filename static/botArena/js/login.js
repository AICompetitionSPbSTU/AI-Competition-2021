jQuery(function($) {
  $('#login_form').on('submit', function(event) {
    if ( validateForm() ) { // если есть ошибки возвращает true

      event.preventDefault();
      $( "send" ).effect("shake");

    }});


  $('#register').on('input', function (event) {
      validateForm()
  });


  function validateForm() {
    $(".text-error").remove();

    // Проверка логина
    var el_l = $("#login");
    if ( el_l.val().length < 4 ) {
      var v_login = true;
      el_l.after('<span class="text-error for-login">Логин должен быть больше 3 символов</span>');
      document.getElementById('login').style.color = "red";
      $(".for-login").css({top: el_l.position().top + el_l.outerHeight() + 2});
    }
    else{
        document.getElementById('login').style.color = "blue";
    }
    $("#login").toggleClass('error', v_login );


    // Проверка паролей

    var el_p1    = $("#pass1");

    var v_pass1 = el_p1.val()?false:true;

    if ( el_p1.val() != el_p2.val() ) {
      var v_pass1 = true;
      var v_pass2 = true;
      el_p1.after('<span class="text-error for-pass1">Пароли не совпадают!</span>');
      document.getElementById('pass1').style.color = "red";
        document.getElementById('pass2').style.color = "red";
      $(".for-pass1").css({top: el_p1.position().top + el_p1.outerHeight() + 2});
    }
    else{
        document.getElementById('pass1').style.color = "blue";
    }

    $("#pass1").toggleClass('error', v_pass1 );

    return ( v_login || v_email || v_pass1 || v_pass2 );
  }

})