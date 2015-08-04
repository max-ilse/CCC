// Submit
function submit() {
	// Get data from text field
	var text = $('#textInput').val();

	// Activate hour glass and grey out the page
	$("#overlay").css("cursor", "wait");
	$("#overlay").fadeIn(250);

	$.ajax({
		url: "/getpoem",
		type:"POST",
		data: JSON.stringify({'primetext':text}),
		contentType:"application/json; charset=utf-8",
		dataType:"json",
		success: function(data){
			// Update text field
			$("#textInput").val(data.poem);

			// No more waiting
			$("#overlay").css("cursor", "default");
			$("#overlay").fadeOut(10);
		}
	})
}

// Main
$(document).ready(function(){
});
