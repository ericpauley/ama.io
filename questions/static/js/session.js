$(".upvote").click(function(){
	if(GLOBALS.auth){
		var id = $(this).attr("data-question")
		if($(this).hasClass("btn-success")){
			$(this).removeClass("btn-success");
			$.post("/api/v1/question/"+id+"/vote/",
				{'vote': 0},
				function(data){
					$("#score-"+id).text(data['score'])
				}
				);
		}else{
			$(this).addClass("btn-success");
			$("#downvote-"+id).removeClass("btn-danger")
			$.post("/api/v1/question/"+id+"/vote/",
				{'vote': 1},
				function(data){
					$("#score-"+id).text(data['score'])
				}
				);
		}
	}else{
		$("#loginModal").modal()
	}
})

$(".downvote").click(function(){
	if(GLOBALS.auth){
		var id = $(this).attr("data-question")
		if($(this).hasClass("btn-danger")){
			$(this).removeClass("btn-danger");
			$.post("/api/v1/question/"+id+"/vote/",
				{'vote': 0},
				function(data){
					$("#score-"+id).text(data['score'])
				}
				);
		}else{
			$(this).addClass("btn-danger");
			$("#upvote-"+id).removeClass("btn-success")
			$.post("/api/v1/question/"+id+"/vote/",
				{'vote': -1},
				function(data){
					$("#score-"+id).text(data['score'])
				}
				);
		}
	}else{
		$("#loginModal").modal()
	}
})

$(function(){
	setInterval(function(){
		$.get("/api/v1/session/"+GLOBALS['session'],
			function(data){
				$("#session-title").text(data['data']['title'])
				$("#session-desc").html(data['data']['desc-html'])
				for(var i=0; i<data['questions'].length;i++){
					var question = data['questions'][i]
					id = question['id']
					if(!$("#question-"+id).length){
						if(question['answer'] == null){
							$("#unansweredlist").append(question['html'])
						}else{
							$("#answeredlist").append(question['html'])
						}
						return
					}
					if(question['answer'] == null){
						$("#unansweredlist").append($("#question-"+id))
					}else{
						$("#answeredlist").append($("#question-"+id))
					}
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
			})
	}, 10000)
})
