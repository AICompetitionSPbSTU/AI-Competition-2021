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



// $(document).ready(function() {
  // $('a.myLinkModal').click( function(event){
  //   event.preventDefault();
  //   $('#myOverlay').fadeIn(297, function(){
  //     $('#myModal')
  //   .css('display', 'block')
  //     .animate({opacity: 1}, 198);
  //   });
  // });

//   $('#myModal__close, #myOverlay').click( function(){
//     $('#myModal').animate({opacity: 0}, 198,
//       function(){
//         $(this).css('display', 'none');
//         $('#myOverlay').fadeOut(297);
//     });
//   });
// });









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
