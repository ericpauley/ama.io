GLOBALS.lock = false

$.fn.smartText = function(val){
	if(this.text() != val){
		this.text(val)
	}
}

$.fn.smartHtml = function(val){
	if(this.html() != val){
		this.html(val)
	}
}

function sessionClicks(){
	$(".upvote").off("click")
	$(".upvote").click(function(){
		if(GLOBALS.auth){
			var id = $(this).attr("data-question")
			GLOBALS.lock = true
			if($(this).hasClass("btn-success")){
				$(this).removeClass("btn-success");
				$.post("/api/v1/question/"+id+"/vote/",
					{'vote': 0},
					function(data){
						$("#score-"+id).text(data['score'])
					})
			}else{
				$(this).addClass("btn-success");
				$("#downvote-"+id).removeClass("btn-danger")
				$.post("/api/v1/question/"+id+"/vote/",
					{'vote': 1},
					function(data){
						$("#score-"+id).text(data['score'])
					})
			}
		}else{
			$("#loginModal").modal()
		}
	})

	$(".downvote").off("click")
	$(".downvote").click(function(){
		if(GLOBALS.auth){
			var id = $(this).attr("data-question")
			GLOBALS.lock = true
			if($(this).hasClass("btn-danger")){
				$(this).removeClass("btn-danger");
				$.post("/api/v1/question/"+id+"/vote/",
					{'vote': 0},
					function(data){
						$("#score-"+id).text(data['score'])
					})
			}else{
				$(this).addClass("btn-danger");
				$("#upvote-"+id).removeClass("btn-success")
				$.post("/api/v1/question/"+id+"/vote/",
					{'vote': -1},
					function(data){
						$("#score-"+id).text(data['score'])
					})
			}
		}else{
			$("#loginModal").modal()
		}
	})

	$(".delete").off("click")
	$(".delete").click(function(){
		$.ajax("/api/v1/question/"+$(this).attr("data-question")+"/",
			{
				'type':"DELETE"
			})
	})
	$(".star").off("click")
	$(".star").click(function(){
		$(this).toggleClass("btn-info")
		var id = $(this).attr("data-question")
		GLOBALS.lock = true
		$.post("/api/v1/question/"+id+"/star/",
					{'star': $(this).hasClass("btn-info")? 1: 0},
					function(data){
						
					})
	})
}

sessionClicks()

function answer(id){
	text = $("#answer-textarea-"+id).val()
	$.post("/api/v1/question/"+id+"/answer/",
		{'answer': text})
	$("#answer-form-"+id).hide()
}

$("#ask-submit").click(function(){
	$.post("/api/v1/session/"+GLOBALS['session']+"/ask/",
		{'question': $("#ask-question").val(), 'desc': $("#ask-desc").val()},
		function(){
			$("#askModal").modal("hide")
		})
})

$.ajax("/api/v1/session/"+GLOBALS['session']+"/", {
	type:"PATCH",
})

function check(){
	GLOBALS.lock = false
	$.ajax("/api/v1/session/"+GLOBALS['session']+"/", {
		type:"GET",
	}).done(
		function(data){
			if(GLOBALS.lock){
				return
			}
			$("#session-title").smartText(data['title'])
			$("#session-subtitle").smartText(data['subtitle'])
			$("#session-desc").smartText(data['desc'])
			$("#session-desc").smartHtml(markdown.toHTML(data['desc']))
			$("#current-viewers").smartText(data['num_viewers']+" people currently viewing this AMA.")
			$("#session-title-edit:hidden").val(data['title'])
			$("#session-subtitle-edit:hidden").val(data['subtitle'])
			$("#session-desc-edit:hidden").val(data['desc'])
			var ids = []
			$(".question").css("display", "none")
			for(var i=0; i<data['questions'].length;i++){
				var question = data['questions'][i]
				var id = question['id']
				ids.push(id)
				$("#question-"+id).css("display", "block")
				if(!$("#question-"+id).length){
					if(question['answer'] == null){
						$("#unansweredlist").append(question['html'])
					}else{
						$("#answeredlist").append(question['html'])
					}
					return
				}
				if(question['answer'] == null){
					if($("#unansweredlist").has("#question-"+id).length == 0){
						$("#unansweredlist").append($("#question-"+id))
					}
					$("#answer-"+id).hide()
				}else{
					if($("#answeredlist").has("#question-"+id).length == 0){
						$("#answeredlist").append($("#question-"+id))
					}
					$("#answer-"+id).show()
					$("#answer-text-"+id).html(markdown.toHTML(question['answer']['response']))
					$("#answer-textarea-"+id).text(question['answer']['response'])
				}
				if(!$("#question-"+id).hasClass("lock")){
					$("#score-"+id).text(question['score'])
					/*if(question['vote'] == 1){
						$("#upvote-"+id).addClass("btn-success")
					}else{
						$("#upvote-"+id).removeClass("btn-success")
					}
					if(question['vote'] == -1){
						$("#downvote-"+id).addClass("btn-danger")
					}else{
						$("#downvote-"+id).removeClass("btn-danger")
					}*/
					if(question['starred'] == 1){
						$("#star-"+id).addClass("btn-info")
					}else{
						$("#star-"+id).removeClass("btn-info")
					}
				}
			}
			sessionClicks()
		}).fail(function(a,b,c){
			d = a
		})
}

$(function(){
	setInterval(check, 1000)
})

$(".show-comments").click(function(){
	question = $(this).attr("data-question")
	if($("#comment-wrapper-"+question).is(":visible")){
		$("#comments-"+question).html("")
		$("#comment-wrapper-"+question).hide()
	}else{
		$("#comment-wrapper-"+question).show()
		$.get("http://localhost:8000/api/v1/comment?question=1").done(function(data){
		$.each(data.objects, function(i, val){
			val.content = markdown.toHTML(val.comment)
			$("#comments-"+question).append(Mustache.template("comment").render(val))
		})
	})
	}
	
})

$(".add-comment").click(function(){
	var question = $(this).closest("[data-question]").attr("data-question")
	var contents = $("#comment-form-"+question).val()
	$.ajax({
		type: "POST",
		url: "/api/v1/comment/", 
		data: JSON.stringify({
		"question": "/api/v1/question/"+question+"/",
		"comment":contents,
		}),
		contentType: "application/json; charset=utf-8",
	}).done(function(data, text, jqXHR){
		$("#comment-form-"+question).val("")
		$.ajax({
			type: "GET",
			url: jqXHR.getResponseHeader("location")
		}).done(function(val){
			val.content = markdown.toHTML(val.comment)
			$("#comments-"+question).prepend(Mustache.template("comment").render(val))
		})
	})

})
