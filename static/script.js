
dt = null;

$(document).ready ( function(){
    $.ajax({
	url : "/program",
	dataType: "text",
	success : function (data) {
	    $("#prog_text").text(data);
	}
    });
});

function loadNowPlaying(){
    $.ajax({
	url : "/serial",
	dataType: "text",
	success : function (data) {
	    $("#sdata").text(data);
	    $('#sdata').scrollTop(9999999);
	}
    });
    //console.log($('#sdata')[0].scrollHeight);
    //$('#sdata').scrollHeight = 500;
    //$('#sdata').scrollHeight = 500;
    //$('#sdata').setScrollPosition(0);//$('#sdata')[0].scrollHeight);
    $('#sdata').scrollTop($('#sdata').scrollHeight);
}


setInterval(function(){loadNowPlaying()}, 1000);
