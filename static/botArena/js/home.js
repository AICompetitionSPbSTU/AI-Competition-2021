(function () {
	window.addEventListener('DOMContentLoaded', function () {
		var
		inTriangle = false,
    last = null,
		navigation = document.getElementById('navigation'),
		x1, x2, x3, y1, y2, y3, link, timeout;

		navigation.addEventListener('mouseenter', onmouseenter);
		navigation.addEventListener('mouseleave', onmouseleave);

		function isInsideTriangle() {
			var
			b0 =  (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1),
			b1 = ((x2 - x0) * (y3 - y0) - (x3 - x0) * (y2 - y0)) / b0,
			b2 = ((x3 - x0) * (y1 - y0) - (x1 - x0) * (y3 - y0)) / b0,
			b3 = ((x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)) / b0;

			return b1 > 0 && b2 > 0 && b3 > 0;
		}

		function onmouseenter(event) {
			document.addEventListener('mousemove', onmousemove);
		}

		function onmouseleave(event) {
			document.removeEventListener('mousemove', onmousemove);
			clearTimeout(timeout);
			if (last) {
        last.classList.remove('active');
        link = null;
      }
		}

		function onmousemove(event) {
			var
			// get nearest anchor
			linkNominee = event.target.closest('li');

			// set target coords
			x0 = event.clientX;
			y0 = event.clientY;

			if (!linkNominee) {
				clearTimeout(timeout);

				if (link && !link.contains(event.target)) {
					link.classList.remove('active');
					link = null;
				}

				return;
			}

			// conditionally set triangle’s left point
			if (linkNominee === link) {

				if (!isInsideTriangle()) {
					x1 = x0;
					y1 = y0;
				}
			} else if (linkNominee !== link) {
				// end if still inside another link’s triangle
				if (link) {
					if (isInsideTriangle()) {
						clearTimeout(timeout);

						timeout = setTimeout(function () {
							if (link) {
								link.classList.remove('active');

								link = null;
							}

							onmousemove(event);
						}, 200);

						return;
					}

					link.classList.remove('active');
				}

				// set link
				link = linkNominee;
        last = link;

				var
				next = link.lastElementChild.getBoundingClientRect();

				// set triangle’s left point
				x1 = x0;
				y1 = y0;

				// set triangle’s top point
				x2 = next.left;
				y2 = next.top;

				// set triangle’s bottom point
				x3 = next.left;
				y3 = next.bottom;

				// set link state
				link.classList.add('active');
			}
		}
	});
})();

var modal = document.getElementById('id01');

// Когда пользователь щелкает в любом месте за пределами модального, закройте его
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// LOGIN VALIDATION

jQuery(function($) {
  $('#login_form').on('submit', function(event) {
    if ( validateForm() ) { // если есть ошибки возвращает true

      event.preventDefault();
      $( "send" ).effect("shake");

    }});


  $('#login_form').on('input', function (event) {
      validateLoginForm()
  });


  function validateLoginForm() {
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

    var el_p1    = $("#pass");

    var v_pass1 = !el_p1.val();

    if ( el_p1.val().length < 6 ) {
      var v_pass2 = true;
      document.getElementById('pass').style.color = "red";
      document.getElementById('log_error_password').style.color = 'black';

    }
    else {
	  document.getElementById('pass').style.color = "blue";
      document.getElementById('log_error_password').style.color = "transparent";
	}

    $("#pass").toggleClass('error', v_pass1 );

    return ( v_login || v_pass1 || v_pass2 );
  }

})

// REGISTRAION VALIDATION

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
    var el_l    = $("#login_in_reg");
    if ( el_l.val().length < 4 ) {
      var v_login = true;
      document.getElementById('login_in_reg').style.color = "red";
      document.getElementById('login_in_reg_err').style.color = 'black';
    }
    else{
        document.getElementById('login_in_reg').style.color = "blue";
        document.getElementById('login_in_reg_err').style.color = 'transparent';

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