$("#login_form").submit(function(event) {
	event.preventDefault()
	$.ajax({
		type: "POST",
		url: "/api/v1/user/login/",
		data: $("#login_form").serialize()
	}).done(function(data) {
		location.reload()
	}).fail(function(data){
		$("#login").addClass("btn-danger")
	})
})