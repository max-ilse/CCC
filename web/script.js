// Submit
function submit() {
  // Get data from text field
  var text = $("#textInput").val();

  // Destroy tweet button always
  $("#tweetButton").remove();
  $("#buttons").append('<a href="http://twitter.com/share" class="twitter-share-button" id="tweetButton" data-text="" data-count="none" data-size="large">Tweet</a>');
  $('a[data-text]').each(function(){
      $(this).attr('data-text', text + " #vbbzb #ccc2015");
  });
  $.getScript('http://platform.twitter.com/widgets.js');

  // Remove info text after first submit
  $("textarea").removeAttr('placeholder');

  // Looking for input errors
  if (text == null || text == "") { // Empty input
        alert("Das Textfeld darf nicht leer sein!");
        return false;
  } else if (/[a-zA-Z0-9\\., \\ä\\ü\\ö\\ß\\Ä\\Ü\\Ö]{1,75}$/.test(text) == false) { // Special Characters
      alert("Bitte benutze nur 0-9a-zA-ZäöüßÄÖÜ .,");
      return false;
  } else if (text.length > 75) { // Input is too long
      alert("Fasse dich bitte etwas kürzer!");
      return false;
  }
  
  // Activate hour glass and grey out the page
  $("#overlay").css("cursor", "wait");
  $("#overlay").fadeIn(250);

  $.ajax({
    url: "/rnnpoetry/getpoem",
    type:"POST",
    data: JSON.stringify({'primetext':text}),
    contentType:"application/json; charset=utf-8",
    dataType:"json",
    timeout: 10000,
    success: function(data){
      // Update text field
      $("#textInput").val(data.poem);

      // Update Twitter
      $('a[data-text]').each(function(){
          $(this).attr('data-text', data.poem + "#vbbzb #ccc2015");
      });
      $.getScript('http://platform.twitter.com/widgets.js');

      // No more waiting
      $("#overlay").css("cursor", "default");
      $("#overlay").fadeOut(10);
    },
    error: function(status){
      // No more waiting
      $("#overlay").css("cursor", "default");
      $("#overlay").fadeOut(10);
      alert("Versuch es bitte noch einmal!");
    }
  })
};

// Main
$(document).ready(function(){
});