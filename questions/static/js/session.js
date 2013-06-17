$(".upvote").click(function(){
	if(GLOBALS.auth){
		id = $(this).attr("data-question")
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
		id = $(this).attr("data-question")
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
