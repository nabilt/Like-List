/*
    Copyright 2012 Nabil Tewolde

    This file is part of Like List.
    
    Like List is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

var WookmarkOptions;
var gElementCount = 0;

function updateClickEvents()
{
    function htmlDecode(input){
        var e = document.createElement('div');
        e.innerHTML = input;
        return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
    }

    $('.embed-content').on('shown', function (event) {
        var modal_div = $('.modal-body', $(this));
        console.log("SHOWING", modal_div);
        if ( modal_div !== null )
        {
            var iframe_data = modal_div.html();
            modal_div.html(htmlDecode( iframe_data ));
        }
        console.log("SHOWING", htmlDecode(modal_div.html()));
    });
    
    $('.embed-content').on('hidden', function (event) {
        var modal_div = $('.modal-body', $(this));
        if ( modal_div !== null )
        {
            var iframe_data = modal_div.html();
            modal_div.text(( iframe_data ));
        }
        
    });
}

function show_alert( title, msg, type )
{
    $('#tiles').css('opacity', '0').empty();
    var alert_div = '<div class="fade in alert alert-' + type + '">\
       <a class="close" data-dismiss="alert">&times;</a>\
       <strong>' + title + '</strong>  ' + msg + '</div>';
    $("#alert-messages").append(alert_div);
    $("#alert-messages").alert();
}

function create_page()
{
    var twitter_name = $("#twitter-search").attr("value");
    var youtube_name = $("#youtube-search").attr("value");
    var vimeo_name = $("#vimeo-search").attr("value");
    var page_name = $("#Page-Name").Attr("Value");

    console.log(twitter_name, page_name);
    var data = {
        'name': page_name,
        't': twitter_name,
        'yt': youtube_name,
        'v': vimeo_name
    };

    $.ajax({
        type: 'POST',
        url: "/page",
        data: data,
        success: function(data, textStatus, jqXHR){
            console.log(data, textStatus, jqXHR);
            show_alert("Success!", "Page created", "success");
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(jqXHR, textStatus, errorThrown);
            show_alert("Error!", jqXHR.responseText, "error");
        },
        dataType: "json"
    });
}

function removeSearchHelp()
{
    $(function () {
        $("#search-boxes .control-group").removeClass("error warning success", 100);
        $("#search-boxes .help-block").animate({opacity: 0}, {duration: 100, queue: false });
    });
}


function draw_layout(feed_data)
{
    console.log(feed_data);
    var html = "";
    var i = 0;
    var images = [];
    for ( i in feed_data )
    {
        var e = feed_data[i];
        var embed_html = "";
        var thumbnail = "";
        var provider_name = "";
        
        if (e.media.length > 0)
        {
            if (e.media[0].type === 'photo')
            {
                thumbnail = '<div class="photo-thumbnail"><img src="' + e.media[0].thumbnail_url + '" height="360" width="480" /></div>';
            }
            if (e.media[0].type === 'video' || e.media[0].type == 'html')
            {
                var video_div_id = "video_" + gElementCount;
                thumbnail =
                '\
                <div class="video-thumbnail">\
                  <a data-toggle="modal" href="#' + video_div_id + '" >\
                    <div class="circle-play-icon"></div>\
                  </a>\
                  <div style="display: none" id="' + video_div_id + '" class="modal fade embed-content">\
                    <div class="modal-header">\
                      <a class="close" data-dismiss="modal">x</a>' +
                      e.title +
                    '</div>\
                    <div class="modal-body center">' +
                      $('<div/>').text(e.media[0].html).html() + 
                    '</div>\
                    <div class="modal-footer">\
                    </div>\
                  </div>\
                  <img src="' + e.media[0].thumbnail_url + '" height="360" width="480"/>\
                </div>';
                embed_html = e.media[0].html;
            }
            else if (e.media[0].type == 'html')
            {
                thumbnail = e.media[0].html;
            }
            provider_name = e.media[0].provider_name + "<br />";
            images.push(e.media[0].thumbnail_url);
        }

        var screen_name = '<a href="' + e.user_url + '" rel="nofollow" target="_blank">' + e.screen_name + '</a>';
        var title = screen_name + '<br />' + e.title;
        html += '<li>' + thumbnail + '<p>' + title + '</p></li>';
        gElementCount = gElementCount + 1;
    }

    $('#tiles').html(html);

    var index = 0;
    $('#tiles').waitForImages({
        finished: function() {            
            console.log('All images are loaded.');
            $("#main-separator").fadeIn(1000);
            $('#tiles li').wookmark(WookmarkOptions);
	    $('#tiles').animate({opacity: 1}, 1000);
        },
        each: function() {
            
        },
        waitForAll: true
    });
    updateClickEvents();
    
}

function search()
{
    var twitter_name = $.trim($("#twitter-search").attr("value"));
    var youtube_name = $.trim($("#youtube-search").attr("value"));
    var vimeo_name = $.trim($("#vimeo-search").attr("value"));

    removeSearchHelp();

    if ( twitter_name === "" && youtube_name === "" && vimeo_name === "")
    {
        $(function () {
            $("#search-boxes .control-group").addClass("warning", 150);
            $("#search-boxes .help-block").animate({opacity: 1}, {duration: 150, queue: false });
            $("#search-boxes .help-block").html("You must enter at least 1 username");
        });
        return;
    }

    function ajax_search() {
	$.ajax({
            url: "/search?t=" + twitter_name + "&yt=" + youtube_name + "&v=" + vimeo_name,
            success: function(data, textStatus, jqXHR){
		//console.log(JSON.parse(data));
		console.log('finish');
		$("#main-progress-bar").fadeOut(300);
		
		var dict = JSON.parse(data);
		if ( dict.length === 0 )
		{		
                    show_alert("Oops", "No likes, favorites or shares exist for this user", "info");		
		    return;
		}
		draw_layout(dict);
		//$("#share-controls").fadeIn(1000);
		//$(this).addClass("done");
            },
            error: function(jqXHR, textStatus, errorThrown){
		console.log(jqXHR, textStatus, errorThrown);
		$("#main-progress-bar").fadeOut(300);
		if (jqXHR.status === 400)
		{
                    $("#search-boxes .help-block").html(jqXHR.responseText);
                    $(function () {
			$("#search-boxes .control-group").addClass("error", 150);
			$("#search-boxes .help-block").animate({opacity: 1}, {duration: 150, queue: false });
                    });
		}
		else
		{
                    show_alert("Error!", "Something went wrong", "error");
		}
            }
	});
    }    

    $("#controls-row").animate({top: 0}, 1000, 'easeOutExpo', function() {});

    $('#tiles').animate({opacity: 0}, 300, function(){ 
	$(".alert").alert('close');
	$("#main-progress-bar").fadeIn(300);	
	ajax_search();
    });
}

$(document).load(new function() {

    var start_search = false;
    $("#search-boxes input[type='text']").each(function(index, element){
        if ( $(this).attr("value").length !== 0 )
        {
            start_search = true;
        }

        if ( index === $("#search-boxes input[type='text']").size() - 1 )
        {
            if ( start_search )
            {
                search();
            }
        }
    });
});


$(document).ready(function() {

    gElementCount = 0;
    // Prepare layout options.
    WookmarkOptions = {
        autoResize: true, // This will auto-update the layout when the browser window is resized.
        container: $('#tile-container'), // Optional, used for some extra CSS styling
        offset: 10 // Optional, the distance between grid items
    };
    updateClickEvents();


    $("#search-boxes input[type='text']").keypress(function(e){
	if(e.which === 13){
	    search();
	}
    });

    $("#search-boxes input[type='text']").keyup(function(e) {
	if(e.which != 13){
            removeSearchHelp();
        }
    });

});
