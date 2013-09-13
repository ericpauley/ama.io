$("#login-form").submit(function(event) {
	event.preventDefault();
	if($("#username").val() || $("#password").val()){
		$("#login-modal-username").val($("#username").val());
		$("#login-modal-password").val($("#password").val());
		$("#login-modal-form").submit();
	} else {
		$("#loginModal").modal();
	}
	
});

$("#login-modal-form").submit(function(event) {
	event.preventDefault();
	$(".form-alert").hide();
	$.ajax({
		type: "POST",
		url: "/api/v1/user/login/",
		data: $("#login-modal-form").serialize()
	}).done(function(data) {
		location.reload();
	}).fail(function(xhr){
		$("#loginModal").modal();
		var err = eval("(" + xhr.responseText + ")");
		$("#login-"+err.reason).show();
	});
});

$('input').keydown(function(e) {
    if (e.keyCode == 13 && !$(this).closest('form').find(":submit").length) {
        $(this).closest('form').submit();
    }
});

$("#login-modal-submit").click(function(){
	$("#login-modal-form").submit();
});

$("#reg_confirm").change(function() {
	if($("#reg_confirm").val() === $("#reg_password").val()){
		$("#reg_confirm_group").removeClass("error");
	}else{
		$("#reg_confirm_group").addClass("error");
	}
});

$("#reg_form").submit(function(event){
	event.preventDefault();
	$(".form-alert").hide();
	$.ajax({
		type: "POST",
		url: "/api/v1/user/register/",
		data: $("#reg_form").serialize()
	}).done(function(data) {
		location.reload();
	}).fail(function(xhr){
		var err = eval("(" + xhr.responseText + ")");
		if(err.reason == "exists"){
			$("#reg_exists").show();
		}else if(err.reason == "reserved"){
			$("#reg_reserved").show();
		}else if(err.reason == "pass_match"){
			$("#reg_passmatch").show();
		}else if(err.reason == "bad_username"){
			$("#bad_username").show();
		}else if(err.reason == "bad_email"){
			$("#bad_email").show();
		}else if(err.reason == "bad_password"){
			$("#bad_password").show();
		}
	});
});

$("#reg_submit").click(function(){
	$("#reg_form").submit();
})

$("#create-session-form").submit(function(event){
    $(this).submit(function() {
        return false;
    });
	$(".form-alert").hide();
	$("#session-upload-iframe").off("load");
	$("#session-upload-iframe").load(function(){
		var resp = eval("("+$("#session-upload-iframe").contents().text()+")");
		if(resp['success']){
			document.location="/s/"+resp.slug;
		}else{
			$("#"+resp.reason).show();
		}
	});
});

$("#request-form").submit(function(event){
	event.preventDefault();
	$(".form-alert").hide();
	$.ajax({
		type: "POST",
		url: "/api/v1/request/create/",
		data: $("#request-form").serialize()
	}).done(function(data) {
		if(data['tweet_url'] && $("#request-send-tweet").prop("checked")){
			document.location = data['tweet_url'];
		}else{
			location.reload();
		}

	}).fail(function(xhr){
		var err = eval("(" + xhr.responseText + ")");
		$("#req_"+err.reason).show();
	});
});

$(".tweet-button").click(function(){
	$.post("/api/v1/request/"+$(this).attr("data-id")+"/vote/");
});

function confirm(div, callback){
	$('#confirm-body').html(div);
	$("#confirm-submit").off("click").click(function(){
		callback();
	})
	$("#confirmModal").modal();
}
