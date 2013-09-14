$("[x-autoblur]").keydown(function(e) {
    if (e.keyCode == 13) {
        $(this).blur();
    }
});

$("#session-title").click(function(){
	$(this).hide();$('#session-title-edit').show().focus();
});

$("#session-title-edit").blur(function(){
	$(this).hide();$('#session-title').show().text(this.value);
	GLOBALS.lock = true;
	$.ajax("/api/v1/session/"+GLOBALS['session']+"/", {
		type:"PATCH",
		data:JSON.stringify({
			title:this.value
		}),
		contentType: 'application/json; charset=utf-8'
	});
});

$("#session-img").click(function(){
	$("#image-form-file").click();
});

$("#add-image").click(function(){
	$("#image-form-file").click();
});

$("#image-form-file").change(function(){
	if($(this).val()){
		$(".form-alert").hide();
		$("#image-form").submit()
	}
});

$("#image-form-iframe").load(function(){
	var resp = eval("("+$("#image-form-iframe").contents().text()+")");
		if(resp['success']){
			if (resp['thumbnail']){
				$("#session-img-inner").prop("src", resp['thumbnail']).show();
				$("#remove-image").show()
				$("#add-image").hide()
			}else{
				$("#session-img").hide()
				$("#remove-image").hide()
				$("#add-image").show()
			}
			
			GLOBALS.lock = true;
		}else{
			$("#"+resp.reason).show();
		}
});

$("#remove-image").click(function(){
	$.post("/api/v1/session/"+GLOBALS['session']+"/image/")
	$("#session-img-inner").hide();
	$("#add-image").show();
	$("#remove-image").hide();
	GLOBALS.lock = true;
});

$("#session-subtitle").click(function(){
	$(this).hide();$('#session-subtitle-edit').show().focus();
});

$("#session-subtitle-edit").blur(function(){
	$(this).hide();$('#session-subtitle').show().text(this.value);
	GLOBALS.lock = true;
	$.ajax("/api/v1/session/"+GLOBALS['session']+"/", {
		type:"PATCH",
		data:JSON.stringify({
			subtitle:this.value
		}),
		contentType: 'application/json; charset=utf-8'
	});
});

$("#session-desc").click(function(){
	$(this).hide();
	$('#session-desc-edit').show().focus();
});

$("#session-desc-edit").blur(function(){
	$(this).hide();
	$('#session-desc').show().html(markdown.toHTML($(this).val()));
	GLOBALS.lock = true;
	$.ajax("/api/v1/session/"+GLOBALS['session']+"/", {
	    type:"PATCH",
	    data:JSON.stringify({
		    desc:this.value
	    }),
	    contentType: 'application/json; charset=utf-8'
	});
});

function sessionClicksOwner(){
	$(".delete").off("click");
	$(".delete").click(function(e){
		del = this
		e.preventDefault();
		confirm("Are you sure you want to delete this question?", function(){
		    $.ajax("/api/v1/question/"+$(del).attr("data-question")+"/",
		        {
		    	'type':"DELETE"
		    });
		    $(del).closest(".question").hide().addClass("deleted");
		});
	});
	$(".star").off("click");
	$(".star").click(function(e){
	    e.preventDefault();
	    $(this).toggleClass("btn-info")
	    var id = $(this).attr("data-question")
	    GLOBALS.lock = true
	    $.post("/api/v1/question/"+id+"/star/",
					{'star': $(this).hasClass("btn-info")? 1: 0},
					function(data){
						
					});
	})
	$(".answer-button").off("click");
	$(".answer-button").click(function(e){
		e.preventDefault();
		$('#answer-form-'+$(this).closest(".question").attr("data-question")).toggle();
	});
}

$("#end-session").click(function(){
	confirm("Are you sure you want to end your AMA session?", function(){
		$.ajax("/api/v1/session/"+GLOBALS['session']+"/", {
			type:"PATCH",
			data:JSON.stringify({
				end_time: new Date().toISOString()
			}),
			contentType: 'application/json; charset=utf-8'
		}).done(function(){
			location.reload();
		});
	});
});

$("#delete-session").click(function(){
	confirm("Are you sure you want to delete your AMA session? This CANNOT be undone.", function(){
		$.ajax("/api/v1/session/"+GLOBALS['session']+"/", {
			type:"DELETE"
		}).done(function(){
			document.location = "/";
		});
	});
});

console.log(sessionClicks);
