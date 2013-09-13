$(".form-alert").hide();
if(!Array.prototype.indexOf) {
    Array.prototype.indexOf = function(needle) {
        for(var i = 0; i < this.length; i++) {
            if(this[i] === needle) {
                return i;
            }
        }
        return -1;
    };
}

$("#createIntroLaunch").click(function(){
    $("#sessionModal").modal("show");
    setTimeout(function(){
        introJs().setOptions({group:".createIntro"}).start(); 
    },700);
});