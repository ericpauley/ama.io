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
		$("#reg_"+err.reason).show();
	});
});

$("#reg_submit").click(function(){
	$("#reg_form").submit();
})

function sessionSubmit(event){
	$(this).off("submit");
	$(this).submit(function(event) {
        event.preventDefault();
    });
    var th = this;
	$(".form-alert").hide();
	$("#session-upload-iframe").off("load");
	$("#session-upload-iframe").load(function(){
		$(th).off("submit");
		$(th).submit(sessionSubmit);
		//var resp = eval("("+$("#session-upload-iframe").contents().text()+")");
		var resp = jQuery.parseJSON(""+$("#session-upload-iframe").contents().text());
		if(resp['success']){
			document.location="/s/"+resp.slug;
		}else{
			$("#"+resp.reason).show();
		}
	});
}

$("#create-session-form").submit(sessionSubmit);

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
