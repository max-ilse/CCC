// Submit
function submit() {
	// Get data from text field
	var text = $("#textInput").val();

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
		url: "/getpoem",
		type:"POST",
		data: JSON.stringify({'primetext':text}),
		contentType:"application/json; charset=utf-8",
		dataType:"json",
		timeout: 10000,
		success: function(data){
			// Update text field
			$("#textInput").val(data.poem);

			// No more waiting
			$("#overlay").css("cursor", "default");
			$("#overlay").fadeOut(10);
		},
		error: function(status){
			alert("Timeout!");
		}
	})
}

// Main
$(document).ready(function(){
});
