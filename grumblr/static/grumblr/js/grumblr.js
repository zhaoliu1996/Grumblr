function get_new_posts(){
  console.log('step info')
    $.ajax({
        type: "GET",
        url: "/grumblr/update_new_post",
        datatype: 'json',
        success: function(posts) {
            $.each(posts, function(id,post) {
                $("#new_post").prepend(
                    "<div class=\"blog-post\">"
                    +"<img src=\"/grumblr/avatar/"+post.fields.user+"\" height=\"32\" width=\"32\" align=\"left\"></img>"
                    +"<p class=\"blog-post-meta\"><a href=\"/grumblr/profile/"+post.fields.user+"\">"+post.fields.username+"</a> "+post.fields.time+"</p>"
                    +"<p>"+post.fields.content+"</p>"
                    +"</div>"
                    );
            });
        },
        error: function() {
            console.log('error');
        }
    });
}

function post_new_comment(){
    $(document).on('submit',"form.new_comment",function(event) {
        event.preventDefault();// Prevent form from being submitted
        var post_id = $(this).attr('id');
        var new_comment= $('#new_input_comment'+post_id).val();
        $.ajax({
            type: "POST",
            url: "/grumblr/add-comment/"+post_id,
            datatype: 'json',
            data: {'comment_text':new_comment},
            success: function(data) {
                $('#new_input_comment'+post_id).val('');
                var fields_value=data[0].fields;
                $('#old_comment'+post_id).append(
                    "<hr><img src=\"/grumblr/avatar/"+fields_value.comment_user+"\" height=\"20\" width=\"20\" align=\"left\" />"
                    +"<h4 style=\"text-indent: 0.5em;\" align=\"left\">"+fields_value.comment_username+"</h4>"
                    +"<h4>"+fields_value.comment_text+"</h4>"
                    +"<h5 align=\"right\">"+fields_value.comment_time+"</h5>"
                );
            },
            error: function() {
                console.log('error');
            }
        });
    });
}

$(document).ready(function () {
  console.log('step info')
  post_new_comment()
  window.setInterval(get_new_posts, 5000);
  console.log('step info')

  // CSRF set-up copied from Django docs
  function getCookie(name) {  
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});



$(document).ready(function() {  // Runs when the document is ready
  console.log('step info')
  post_new_comment()

    // CSRF set-up copied from Django docs
  function getCookie(name) {  
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});