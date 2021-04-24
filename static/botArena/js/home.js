$(document).ready(function() {
  $('a.myLinkModal').click( function(event){
    event.preventDefault();
    $('#myOverlay').fadeIn(297, function(){
      $('#myModal')
      .css('display', 'block')
      .animate({opacity: 1}, 198);
    });
  });

  $('#myModal__close, #myOverlay').click( function(){
    $('#myModal').animate({opacity: 0}, 198,
      function(){
        $(this).css('display', 'none');
        $('#myOverlay').fadeOut(297);
    });
  });
});









// var menuItemOpenedTimeout;
//
// jQuery(function($) {
//   $('#game-list > li > h3').on('mouseover', function () {
//     clearTimeout(menuItemOpenedTimeout);
//   });
// })
//
// jQuery(function($) {
//     $('#game-list > li').on('mouseleave', function() {
//         menuItemOpenedTimeout = setTimeout(function() {
//             // $('#game-list > li > h3 > ul').hide(350);
//             $(this).find('ul').hide();
//         }, 500);
//     });
//     }
// )
//
// jQuery(function($) {
// // Открытие подменю
// $('#game-list > li > h3').on('mouseover',function() {
//     // // Закрытие всех открытых подменю
//     //     menuItemOpenedTimeout = setTimeout(function () {
//     //   $(this).find('ul').hide();
//     // }, 0);
//
//     // Открытие текущего подменю
//     $(this).parent().find('ul').show(400);
// }
// )
// })



// var menuItemOpenedTimeout;
//
// jQuery(function($) {
//   $('#game-list > li').on('mouseover', function () {
//     clearTimeout(menuItemOpenedTimeout);
//   });
// })
//
// jQuery(function($) {
// $('#game-list > li > ul > li').on('mouseleave', function() {
//     menuItemOpenedTimeout = setTimeout(function() {
//         $(this).hide(450);
//     }, 300);
// });
// }
// )
//
// jQuery(function($) {
// // Открытие подменю
// $('#game-list > li > h3').hover(function() {
//     // Закрытие всех открытых подменю
//         menuItemOpenedTimeout = setTimeout(function () {
//       $(this).parent().parent().find('li ul').hide(1000);
//     }, 300);
//
//     // Открытие текущего подменю
//     $(this).parent().find('ul').show(250);
// }
// )
// })





// jQuery(function($) {
//   $('#game-list > li > h3').hover(function() {
//       // $(this).parent().find('ul').hide(150);
//
//     if ($(this).parent().find('ul').length) {
//       $(this).parent().find('ul').slideToggle(250);
//
//       return false;
//     }
//   })
// });


// // Предотвращение закрытия подменю
// $('#game-list > li > h3').on('mouseover', function() {
//     clearTimeout(menuItemOpenedTimeout);
// });
//
// // Закрытие всех подменю через 300 миллисекунд в случае покидания мышкой зоны родительского пункта меню
// $('#game-list > li > h3').on('mouseleave', function() {
//     menuItemOpenedTimeout = setTimeout(function() {
//         $('ul').hide();
//     }, 300);
// });
