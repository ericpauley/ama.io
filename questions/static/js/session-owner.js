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
