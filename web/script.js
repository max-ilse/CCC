// Submit
function submit() {
	// Get data from text field
	var text = $('#textInput').val();

	// Activate hour glass and grey out the page
	$("#overlay").css("cursor", "wait");
	$("#overlay").fadeIn(250);   

	// Simulate post and get
	setTimeout(function(){
		// Update text field
		$("#textInput").val(text + " DATA FROM SERVER");

		// No more waiting
		$("#overlay").css("cursor", "default");
		$("#overlay").fadeOut(10);  
	},
	3000
	);	
}

// Main
$(document).ready(function(){
});