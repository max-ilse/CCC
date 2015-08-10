// Submit
function submit() {
	// Get data from text field
	var text = $('#textInput').val();

	// Test input
	if (text == null || text == "") {
        alert("Das Textfeld darf nicht leer sein!");
        return false;
    } else if (!(text.match(/[0-9A-Z]/))) {
    	alert("Bitte benutze nur: 0-9, a-z, A-Z, äöüß, ÄÖÜẞ, ., ,");
        return false;
    }

	// Activate hour glass and grey out the page
	$("#overlay").css("cursor", "wait");
	$("#overlay").fadeIn(250);   

	// Simulate post and get
	setTimeout(function(){
		// Update text field
		$("#textInput").val(" DATA FROM SERVER");

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