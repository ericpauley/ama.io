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
				}, 500)
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
				}, 500)
		}
	}else{
		$("#loginModal").modal()
	}
})

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
				}, 500)
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
				}, 500)
		}
	}else{
		$("#loginModal").modal()
	}
})

$("#ask-submit").click(function(){
	$.post("/api/v1/session/"+GLOBALS['session']+"/ask/",
		{'question': $("#ask-question").val()},
		function(){
			$("#askModal").modal("hide")
		})
})

$(function(){
	setInterval(function(){
		$.get("/api/v1/session/"+GLOBALS['session'],
			function(data){
				$("#session-title").text(data['data']['title'])
				$("#session-desc").html(data['data']['desc-html'])
				var ids = []
				for(var i=0; i<data['questions'].length;i++){
					var question = data['questions'][i]
					var id = question['id']
					ids.push(id)
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
						$("#answer-text-"+id).text(question['answer']['response'])
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
					}
				}
				$(".question").each(function(){
					if(ids.indexOf(parseInt($(this).attr('data-question'))) == -1){
						$(this).remove()
					}
				})
			})
	}, 1000)
})
