$(function() {
  $("#smooth_button").click(function() {
    $("#smooth_button").addClass("onclic");
    setTimeout(function() {
      $("#smooth_button").removeClass("onclic");
      $("#smooth_button").addClass("validate");
    }, 2250);
    setTimeout(function() {
      $("#smooth_button").removeClass("validate");
    }, 3500);
  });
});

document.querySelector("html").classList.add('js');

var fileInput  = document.querySelector( ".input-file" ),
    button     = document.querySelector( ".input-file-trigger" ),
    the_return = document.querySelector(".file-return");

button.addEventListener( "keydown", function( event ) {
    if ( event.keyCode == 13 || event.keyCode == 32 ) {
        fileInput.focus();
    }
});
button.addEventListener( "click", function( event ) {
   fileInput.focus();
   return false;
});
fileInput.addEventListener( "change", function( event ) {
    the_return.innerHTML = document.getElementById("my-file").files[0].name;
});
