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

$("#reg_confirm").change(function() {
	if($("#reg_confirm").val() === $("#reg_password").val()){
		$("#reg_confirm_group").removeClass("error")
	}else{
		$("#reg_confirm_group").addClass("error")
	}
})

$("#reg_terms").click(function(){
	if($("#reg_terms").prop('checked')){
		$("#reg_submit").prop("disabled", false)
	}else{
		$("#reg_submit").prop("disabled", true)
	}
})