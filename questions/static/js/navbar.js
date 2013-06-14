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

$("#reg_form").submit(function(event){
	event.preventDefault()
	$(".form-alert").hide()
	$.ajax({
		type: "POST",
		url: "/api/v1/user/register/",
		data: $("#reg_form").serialize()
	}).done(function(data) {
		location.reload()
	}).fail(function(xhr){
		var err = eval("(" + xhr.responseText + ")")
		if(err.reason == "exists"){
			$("#reg_exists").show()
		}else if(err.reason == "pass_match"){
			$("#reg_passmatch").show()
		}
	})
})

$("#reg_submit").click(function(){
	$("#reg_form").submit()
})
