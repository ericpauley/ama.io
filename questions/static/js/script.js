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

function setCookie(c_name,value,exdays)
{
var exdate=new Date();
exdate.setDate(exdate.getDate() + exdays);
var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
document.cookie=c_name + "=" + c_value;
}

setCookie("tzoffset",-new Date().getTimezoneOffset(), 100)
setCookie("tzname",jstz.determine().name(), 100)

function pad(value) {
    return value < 10 ? '0' + value : value;
}
function createOffset(date) {
    var sign = (date.getTimezoneOffset() > 0) ? "-" : "+";
    var offset = Math.abs(date.getTimezoneOffset());
    var hours = pad(Math.floor(offset / 60));
    var minutes = pad(offset % 60);
    return sign + hours + ":" + minutes;
}

$(function() {
    $('a[rel*=leanModal]').leanModal({closeButton: ".modal_close" });       
});

$(function() {
  $('#signup-bottom').click(function() {
    $("#signup").css('display', 'none');
  });
});

$(function() {
  $('#signin-bottom').click(function() {
    $("#signin").css('display', 'none');
  });
});