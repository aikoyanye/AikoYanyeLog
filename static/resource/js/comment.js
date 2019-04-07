// 添加评论
function AddComment(contentId, userId){
    var email = document.getElementById('comment_email').value;
    var comment = document.getElementById('comment_content').value;
    if(email == '' || comment == ''){
        ShowMsgAlert('警告', '记得输入内容啊');
        return
    }
    $.ajax({
        url: "/comment",
        type: "post",
        data: {email: email, comment: comment, contentId: contentId},
        success: function(arg){
            ShowSeccussAlert();
            Comment(contentId, userId);
        },error: function(arg){
            ShowFailAlert();
        }
    })
}

// 获取评论列表
function Comment(contentId, userId){
    $.ajax({
        url: "/comment",
        type: "get",
        data: {contentId: contentId},
        success: function(arg){
            ShowComment(jQuery.parseJSON(arg), userId);
        },error: function(arg){
            ShowFailAlert();
        }
    })
}

// 刷新评论列表
function ShowComment(data, userId){
    var div = document.getElementById('comment');
    div.innerHTML = '';
    for(var i = 0; i<data.length; i++){
        if(String(data[i][3]) == String(userId)){
            var de = '<button type="button" class="btn btn-danger" onclick="DeleteComment('+data[i][4]+', '+data[i][5]+', '+userId+')" >删除</button>';
        }else{
            var de = '';
        }
        div.innerHTML = div.innerHTML + '<div class="panel panel-default">\
        <div class="panel-heading" style="background-color: #FFE4E1;">'+data[i][1]+'\
        </div><div class="panel-body" style="background-color: #FFF5EE;">\
        <table width="100%"><tr><td>'+data[i][0]+'</td><td>'+data[i][2]+'</td><td>'+de+'</td></tr></table></div></div>';
    }
}

// 删除评论
function DeleteComment(commentId, contentId, userId){
    $.ajax({
        url: "/comment",
        type: "delete",
        data: {commentId: commentId},
        success: function(arg){
            ShowSeccussAlert();
            Comment(contentId, userId);
        },error: function(arg){
            ShowFailAlert();
        }
    })
}