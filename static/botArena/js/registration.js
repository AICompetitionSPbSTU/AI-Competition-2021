jQuery(function($) {
  $('#register').on('submit', function(event) {
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
    var el_l    = $("#login");
    if ( el_l.val().length < 4 ) {
      var v_login = true;
      document.getElementById('login').style.color = "red";
      document.getElementById('login_err').style.color = 'black';
    }
    else{
        document.getElementById('login').style.color = "blue";
        document.getElementById('login_err').style.color = 'transparent';

    }
    $("#login").toggleClass('error', v_login );

    // Проверка e-mail

    let reg     = /^\w+([\.-]?\w+)*@(((([a-z0-9]{2,})|([a-z0-9][-][a-z0-9]+))[\.][a-z0-9])|([a-z0-9]+[-]?))+[a-z0-9]+\.([a-z]{2}|(com|net|org|edu|int|mil|gov|arpa|biz|aero|name|coop|info|pro|museum))$/i;
    let el_e    = $('#email');
    let v_email = el_e.val()?false:true;

    if ( v_email ) {
      document.getElementById('email').style.color = "red";
      document.getElementById('email_err').innerText = 'E-mail is required!'
      document.getElementById('email_err').style.color = 'black'

    } else if ( !reg.test( el_e.val() ) ) {
      v_email = true;
      document.getElementById('email').style.color = "red";
      document.getElementById('email_err').innerText = 'You put in unacceptable e-mail!'
      document.getElementById('email_err').style.color = 'black'


    }
    else{
              document.getElementById('email').style.color = "blue";
              document.getElementById('email_err').style.color = 'transparent';

    }
    $("#email").toggleClass('error', v_email );

    // Проверка паролей

    var el_p1    = $("#pass1");
    var el_p2    = $("#pass2");

    var v_pass1 = el_p1.val()?false:true;
    var v_pass2 = el_p1.val()?false:true;


    if ( el_p1.val().length < 6 ) {
      var v_pass1 = true;
      var v_pass2 = true;
      document.getElementById('pass1').style.color = "red";
      document.getElementById('pass2').style.color = "red";
      document.getElementById('error_password').style.color = 'black';

    }
        else{
        document.getElementById('pass1').style.color = "blue";
        document.getElementById('error_password').style.color = 'transparent';
    }

    if ( el_p1.val() != el_p2.val() ) {
      var v_pass1 = true;
      var v_pass2 = true;
      document.getElementById('pass1').style.color = "red";
      document.getElementById('pass2').style.color = "red";
      document.getElementById('mismatch').style.color = 'black';

    }
    else{
        document.getElementById('pass1').style.color = "blue";
        document.getElementById('pass2').style.color = "blue";
        document.getElementById('error_password').style.color = 'transparent';
        document.getElementById('mismatch').style.color = 'transparent';


    }

    $("#pass1").toggleClass('error', v_pass1 );
    $("#pass2").toggleClass('error', v_pass2 );

    return ( v_login || v_email || v_pass1 || v_pass2 );
  }

})