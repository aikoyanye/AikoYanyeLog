// 初始化富文本编辑器
window.onload=function (){
    var E = window.wangEditor;
    editor = new E('#rich_editor_toolbar', '#rich_editor_text');
    editor.create();
    editor1 = new E('#rerich_editor_toolbar', '#rerich_editor_text');
    editor1.create();
    // 更新首页更新列表
    InitUpdateList();
}

// 初始化添加content tab页
function InitAddContentTab(userId){
    $.ajax({
        url: "/title",
        type: "get",
        data: {userId: userId, type: '2'},
        success: function(arg){
            editor.txt.clear();
            var results = jQuery.parseJSON(arg);
            var select = document.getElementById('add_content_title');
            select.innerHTML = '';
            for(var i = 0; i<results.length; i++){
                select.innerHTML = select.innerHTML + '<option value="'+results[i][0]+'">'+results[i][1]+'</option>';
            }
        },error: function(arg){
            ShowFailAlert();
        }
    })
}

// 上传图片
function UploadPic(username){
    var pic = document.getElementById('add_content_pic');
    if(pic.value == ''){
        ShowMsgAlert('警告', '你都没选择图片');
        return
    }
    var d = new FormData();
    d.append('pic', document.getElementById('add_content_pic').files[0]);
    d.append('type', '1');
    d.append('username', username);
    $.ajax({
        url: "/content",
        type: "post",
        data: d,
        processData: false,
        contentType: false,
        async: false,
        cache: false,
        success: function(arg){
            var results = jQuery.parseJSON(arg);
            editor.txt.append('<img src="'+results+'" alt="图片失效了" />')
        },error: function(arg){
            ShowFailAlert();
        }
    })
}

// 修改content时上传图片
function UploadRePic(userId){
    var pic = document.getElementById('re_content_pic');
    if(pic.value == ''){
        ShowMsgAlert('警告', '你都没选择图片');
        return
    }
    var d = new FormData();
    d.append('pic', document.getElementById('re_content_pic').files[0]);
    d.append('type', '1');
    d.append('username', String(userId)+'_');
    $.ajax({
        url: "/content",
        type: "post",
        data: d,
        processData: false,
        contentType: false,
        async: false,
        cache: false,
        success: function(arg){
            ShowSeccussAlert();
            var results = jQuery.parseJSON(arg);
            editor1.txt.append('<img src="'+results+'" alt="图片失效了" />');
            document.getElementById('re_content_pic').value = '';
        },error: function(arg){
            ShowFailAlert();
        }
    })
}

// 添加文章
function AddContent(userId){
    var head = document.getElementById('add_content_head').value;
    if(head == ''){
        ShowMsgAlert('警告', '记得输入文章标题啊');
        return
    }
    $.ajax({
        url: "/content",
        type: "post",
        data: {type: '2', titleId: document.getElementById('add_content_title').value, content: editor.txt.html(),
                head: head, hidden: document.getElementById('add_content_hidden').value},
        success: function(arg){
            ShowSeccussAlert();
            InitContentListTab(document.getElementById('add_content_title').value, userId);
            document.getElementById('goto_tab_content_list').click();
        },error: function(arg){
            ShowFailAlert();
        }
    })
}

// 初始化content list tab
function InitContentListTab(titleId, userId){
    $.ajax({
        url: "/content",
        type: "get",
        data: {type: '1', titleId: titleId, userId: userId},
        success: function(arg){
            ShowContentList(jQuery.parseJSON(arg), titleId, userId);
        },error: function(arg){
            ShowFailAlert();
        }
    })
}

// 展示content list数据
function ShowContentList(data, titleId, userId){
    var div = document.getElementById('content_list_tab');
    div.innerHTML = '<button type="button" class="btn btn-warning" href="#title_tab" role="tab" \
                        data-toggle="tab" style="margin-bottom: 10px;width: 100%;">返回分类列表</button>';
    for(var i = 0; i<data.length; i++){
        div.innerHTML = div.innerHTML + '<div class="panel panel-default">\
        <div class="panel-heading" style="background-color: #FFE4E1;"><h3><a href="#content" role="tab" data-toggle="tab" \
        onclick="InitContentTab('+data[i][2]+', '+titleId+', '+userId+')">'+data[i][0]+'</a></h3></div>\
        <div class="panel-body" style="background-color: #FFF5EE;">最后编辑时间：'+data[i][1]+'</div></div>';
    }
}

// 初始化content tab
function InitContentTab(contentId, titleId, userId){
    $.ajax({
        url: "/content",
        type: "get",
        data: {type: '2', contentId: contentId},
        success: function(arg){
            Comment(contentId, userId);
            var data = jQuery.parseJSON(arg);
            document.getElementById('comment_btnsub').innerHTML = '<button type="button" class="btn btn-primary \
            glyphicon glyphicon-send" style="margin-top: 10px;width: 100%;" onclick="AddComment('+contentId+', '+userId+')"></button>';
            document.getElementById('content_head').innerHTML = '<h3>'+data[0]+'</h3>';
            document.getElementById('content_title').innerHTML = '<h4>分类：'+data[3]+'</h4>';
            document.getElementById('content_created').innerHTML = '<h4>最后编辑时间：'+data[2]+'</h4>';
            editor1.txt.html(data[1]);
            editor1.$textElem.attr('contenteditable', false);
            if(String(data[4]) == String(userId)){
                document.getElementById('content_edit').innerHTML = '<button type="button" class="btn btn-info" \
                onclick="EditContent(\''+data[0]+'\', '+userId+')">编辑</button>';
                document.getElementById('content_submit').innerHTML = '<button type="button" class="btn btn-primary" \
                onclick="SubmitEditContent('+contentId+')" id="content_btn_sub" disabled>修改</button>';
                document.getElementById('content_delete').innerHTML = '<button type="button" class="btn btn-danger" \
                                            onclick="InitDeleteContent('+contentId+', '+titleId+', '+userId+')" \
                                            data-toggle="modal" data-target="#content_delete_modal">删除</button>';
            }
        },error: function(arg){
            ShowFailAlert();
        }
    })
}

// 编辑content
function EditContent(head, userId){
    $.ajax({
        url: "/title",
        type: "get",
        data: {userId: userId, type: '2'},
        success: function(arg){
            editor1.$textElem.attr('contenteditable', true);
            document.getElementById('content_created').innerHTML = '<select class="form-control" id="re_hidden" style="margin-left: 5px;">\
                                                    <option value="1">是</option><option value="0">否</option></select>';
            document.getElementById('content_head').innerHTML = '<input class="form-control" type="text" id="re_head" value="'+head+'">';
            document.getElementById('content_btn_sub').removeAttribute('disabled');
            document.getElementById('content_title').innerHTML = '<select class="form-control" id="re_title"></select>';
            document.getElementById('content_pic_sub').innerHTML = '<button type="button" class="btn btn-default" \
                                    onclick="UploadRePic('+userId+')" style="margin-left: 5px;">上传图片</button>';
            document.getElementById('content_pic').innerHTML = '<input type="file" accept="image/*" id="re_content_pic">'
            var results = jQuery.parseJSON(arg);
            var select = document.getElementById('re_title');
            for(var i = 0; i<results.length; i++){
                select.innerHTML = select.innerHTML + '<option value="'+results[i][0]+'">'+results[i][1]+'</option>';
            }
        },error: function(arg){
            ShowFailAlert();
        }
    })
}

// 提交编辑content
function SubmitEditContent(contentId){
    var head = document.getElementById('re_head').value;
    if(head == ''){
        ShowMsgAlert('警告', '标题不能为空啊');
        return
    }
    $.ajax({
        url: "/content",
        type: "put",
        data: {contentId: contentId, head: head, titleId: document.getElementById('re_title').value,
                        content: editor1.txt.html(), hidden: document.getElementById('re_hidden').value},
        success: function(arg){
            ShowSeccussAlert();
            var data = jQuery.parseJSON(arg);
            editor1.$textElem.attr('contenteditable', false);
            document.getElementById('content_head').innerHTML = '<h3>'+head+'</h3>';
            document.getElementById('content_title').innerHTML = data[0];
            document.getElementById('content_created').innerHTML = data[1];
            document.getElementById('content_btn_sub').setAttribute('disabled', true);
            ShowSeccussAlert();
        },error: function(arg){
            ShowFailAlert();
        }
    })
}

// 初始化删除content模态框
function InitDeleteContent(contentId, titleId, userId){
    document.getElementById('content_delete_footer').innerHTML = '<button type="button" class="btn btn-danger" \
               onclick="DeleteContent('+contentId+', '+titleId+', '+userId+')" data-dismiss="modal">删除</button>'
}

// 删除content
function DeleteContent(contentId, titleId, userId){
    $.ajax({
        url: "/content",
        type: "delete",
        data: {contentId: contentId},
        success: function(arg){
            ShowSeccussAlert();
            InitContentListTab(titleId, userId);
            document.getElementById('goto_tab_content_list').click();
        },error: function(arg){
            ShowFailAlert();
        }
    })
}