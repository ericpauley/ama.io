function sessionClicks(){
	$(".upvote").off("click")
	$(".upvote").click(function(){
		if(GLOBALS.auth){
			var id = $(this).attr("data-question")
			$("#question-"+id).addClass("lock")
			if($(this).hasClass("btn-success")){
				$(this).removeClass("btn-success");
				$.post("/api/v1/question/"+id+"/vote/",
					{'vote': 0},
					function(data){
						$("#score-"+id).text(data['score'])
					})
					setTimeout(function(){
						$("#question-"+id).removeClass("lock")
					}, 1000)
			}else{
				$(this).addClass("btn-success");
				$("#downvote-"+id).removeClass("btn-danger")
				$.post("/api/v1/question/"+id+"/vote/",
					{'vote': 1},
					function(data){
						$("#score-"+id).text(data['score'])
					})
					setTimeout(function(){
						$("#question-"+id).removeClass("lock")
					}, 1000)
			}
		}else{
			$("#loginModal").modal()
		}
	})

	$(".downvote").off("click")
	$(".downvote").click(function(){
		if(GLOBALS.auth){
			var id = $(this).attr("data-question")
			$("#question-"+id).addClass("lock")
			if($(this).hasClass("btn-danger")){
				$(this).removeClass("btn-danger");
				$.post("/api/v1/question/"+id+"/vote/",
					{'vote': 0},
					function(data){
						$("#score-"+id).text(data['score'])
					})
					setTimeout(function(){
						$("#question-"+id).removeClass("lock")
					}, 1000)
			}else{
				$(this).addClass("btn-danger");
				$("#upvote-"+id).removeClass("btn-success")
				$.post("/api/v1/question/"+id+"/vote/",
					{'vote': -1},
					function(data){
						$("#score-"+id).text(data['score'])
					})
					setTimeout(function(){
						$("#question-"+id).removeClass("lock")
					}, 1000)
			}
		}else{
			var id = $(this).attr("data-question")
			$("#loginModal").modal()
			$.post("/api/v1/question/"+id+"/vote/",
					{'vote': -1},
					function(data){
						$("#score-"+id).text(data['score'])
					})
					setTimeout(function(){
						$("#question-"+id).removeClass("lock")
					}, 1000)
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
		$("#question-"+id).addClass("lock")
		$.post("/api/v1/question/"+id+"/star/",
					{'star': $(this).hasClass("btn-info")? 1: 0},
					function(data){
						
					})
					setTimeout(function(){
						$("#question-"+id).removeClass("lock")
					}, 1000)
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

function check(){
	$.ajax({
		type:"GET",
		url:"/api/v1/session/"+GLOBALS['session']+"/"
	}).done(
		function(data){
			$("#session-title").text(data['title'])
			$("#session-desc").html(markdown.toHTML(data['desc']))
			$("#current-viewers").text(data['num_viewers']+" people currently viewing this AMA.")
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
					if(question['vote'] == 1){
						$("#upvote-"+id).addClass("btn-success")
					}else{
						$("#upvote-"+id).removeClass("btn-success")
					}
					if(question['vote'] == -1){
						$("#downvote-"+id).addClass("btn-danger")
					}else{
						$("#downvote-"+id).removeClass("btn-danger")
					}
					if(question['starred'] == 1){
						$("#star-"+id).addClass("btn-info")
					}else{
						$("#star-"+id).removeClass("btn-info")
					}
				}
			}
			sessionClicks()
		})
	$(".comment-frame").each(function(){
		$(this).height($(this).contents().height())
	})
}

$(function(){
	setInterval(check, 1000)
})
