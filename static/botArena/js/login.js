/* Изначально форма не заполнена и по этому считаем что все возможные ошибки есть  */
var errorNull = true, errorMail = true, errorPass = true;

/* Для удобства и уменьшения размера кода выносим функцию проверки поля на null в отдельную переменную */
var checkNull = function(){
  $(this).val($(this).val().trim());
  if ($(this).val() =="") {
    /* Выводим сообщение об ошибке под элементом.
       This в данном случае это элемент, который инициировал вызов функции */
    $(this).notify("Поле нужно заполнить", "error");
    $(this).addClass("errtextbox");
    errorNull = true;
  } else {
    errorNull = false;
    $(this).removeClass("errtextbox");
  }
};

/* Проверяем значения полей Имя и Информация на null в момент когда они теряют фокус */
$("#username").focusout(checkNull);

/* Проверка поля Имя на соответствие длинны */
$("#username").keyup(function(){
  var value = $(this).val();
  if (value.length > 24){
    $(this).notify("Максимум 25 символов", "info");
    $(this).val(value.slice(0,24));
  }
});

/* Проверяем корректность E-mail */
$("#mail").focusout(function(){
  var value = $(this).val().trim();
/* Для этого используем регулярное выражение  */
  if (value.search(/^[a-z0-9]{3,}@mail\.com$/i) != 0) {
    $(this).notify("E-mail введён не корректно", "error");
    $(this).addClass("errtextbox");
    errorMail = true;
  } else {
    $(this).removeClass("errtextbox");
    errorMail = false;
  }
});

/* Проверяем длину пароля */
$("#password").focusout(function(){
  var value = $(this).val();
  if (value.length <= 4) {
    $(this).notify("Минимум 5 символов", "error");
    $(this).addClass("errtextbox");
    errorPass = true;
  } else {
    if (value.length > 9) {
      $(this).notify("Миксимум 10 символов", "error");
      $(this).addClass("errtextbox");
      errorPass = true;
    } else {
      errorPass = false;
      $(this).removeClass("errtextbox");
    }
  }
});


/* В результате клика по кнопке отправить если ошибок заполнения нет то форма отправляется иначе получаем сообщение об ошибке */
$("#submit").click(function(){
  if (!(errorNull || errorMail || errorPass)) {
    $("#login").submit();
  } else {
    $(this).notify("Форма пустая или заполнена не корректно", "error");
  }
});


// $('form[id="login"]').validate({
//   rules: {
//     fname: 'required',
//     lname: 'required',
//     user_email: {
//       required: true,
//       email: true,
//     },
//     psword: {
//       required: true,
//       minlength: 8,
//     }
//   },
//   messages: {
//     fname: 'This field is required',
//     lname: 'This field is required',
//     user_email: 'Enter a valid email',
//     psword: {
//       minlength: 'Password must be at least 8 characters long'
//     }
//   },
//   submitHandler: function(form) {
//     form.submit();
//   }
// });