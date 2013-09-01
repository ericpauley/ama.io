$("[x-autoblur]").keydown(function(e) {
    if (e.keyCode == 13) {
        $(this).blur()
    }
});

$("#session-title").click(function(){
	$(this).hide();$('#session-title-edit').show().focus()
})

$("#session-title-edit").blur(function(){
	$(this).hide();$('#session-title').show().text(this.value)
	GLOBALS.lock = true
	$.ajax("/api/v1/session/"+GLOBALS['session']+"/", {
		type:"PATCH",
		data:JSON.stringify({
			title:this.value
		}),
		contentType: 'application/json; charset=utf-8',
	})
})

$("#session-subtitle").click(function(){
	$(this).hide();$('#session-subtitle-edit').show().focus()
})

$("#session-subtitle-edit").blur(function(){
	$(this).hide();$('#session-subtitle').show().text(this.value)
	GLOBALS.lock = true
	$.ajax("/api/v1/session/"+GLOBALS['session']+"/", {
		type:"PATCH",
		data:JSON.stringify({
			subtitle:this.value
		}),
		contentType: 'application/json; charset=utf-8',
	})
})

$("#session-desc").click(function(){
	$(this).hide()
	$('#session-desc-edit').show().focus()
})

$("#session-desc-edit").blur(function(){
	$(this).hide()
	$('#session-desc').show().html(markdown.toHTML($(this).val()))
	GLOBALS.lock = true
	$.ajax("/api/v1/session/"+GLOBALS['session']+"/", {
		type:"PATCH",
		data:JSON.stringify({
			desc:this.value
		}),
		contentType: 'application/json; charset=utf-8',
	})
})

function sessionClicks(){
	$(".delete").off("click")
	$(".delete").click(function(e){
		e.preventDefault()
		$.ajax("/api/v1/question/"+$(this).attr("data-question")+"/",
			{
				'type':"DELETE"
			})
	})
	$(".star").off("click")
	$(".star").click(function(e){
		e.preventDefault()
		$(this).toggleClass("btn-info")
		var id = $(this).attr("data-question")
		GLOBALS.lock = true
		$.post("/api/v1/question/"+id+"/star/",
					{'star': $(this).hasClass("btn-info")? 1: 0},
					function(data){
						
					})
	})
	$(".answer-button").off("click")
	$(".answer-button").click(function(e){
		e.preventDefault()
		$('#answer-form-'+$(this).closest(".question").attr("data-question")).toggle();
	})
}

$("#end-session").click(function(){
	$.ajax("/api/v1/session/"+GLOBALS['session']+"/", {
		type:"PATCH",
		data:JSON.stringify({
			end_time: new Date().toISOString()
		}),
		contentType: 'application/json; charset=utf-8',
	}).done(function(){
		location.reload()
	})
})

console.log(sessionClicks)
