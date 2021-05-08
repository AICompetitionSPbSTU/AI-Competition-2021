jQuery(function($) {
  $('#form').on('input', function (event) {
      validateForm()
  });

  // $('#form').on('submit', function (event) {
  //     if(validateForm()){
  //         event.preventDefault();
  //     }
  // });

    function validateForm() {
    $(".text-error").remove();
    var el_l = $("#sub");
    const files = document.getElementById('file-input').files;
    const file = files[0];
      if(!file){
        return true;
      }
      else if(!file.name.endsWith(".py")){
        el_l.after('<br class="text-error for-login"> <span class="text-error for-login"> It is not .py file! </span>');
        return true
      }
    return false

  // $('#login_form').on('submit', function(event) {
  //   if ( validateForm() ) { // если есть ошибки возвращает true
  //     event.preventDefault();
  //     $( ".send" ).after('<br class="text-error for-login"> <span class="text-error for-login"> Username is too short </span>');
  //
  //   }});



}})