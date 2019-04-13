// 添加分类
function AddTitle(userId){
    var title = document.getElementById('add_title_name').value;
    if(title == ''){
        ShowMsgAlert('警告', '分类名不能为空啊');
        return
    }
    $.ajax({
        url: "/title",
        type: "post",
        data: {title: title, hidden: document.getElementById('add_title_hidden').value, userId: userId},
        success: function(arg){
            ShowSeccussAlert();
            InitTitleTab(userId);
        }
    })
}

// title_tab标签初始化
function InitTitleTab(userId){
    $.ajax({
        url: "/title",
        type: "get",
        data: {userId: userId, type: '1'},
        success: function(arg){
            var results = jQuery.parseJSON(arg);
            ShowUserTitle(results['user'], userId);
            ShowGuestTitle(results['guest'], userId);
        }
    })
}

// 将用户分类数据展示到title_tab中，可操作
function ShowUserTitle(data, userId){
    var div = document.getElementById('title_tab');
    div.innerHTML = '';
    for(var i = 0; i<data.length; i++){
        div.innerHTML = div.innerHTML + '<div class="panel panel-default">\
                    <div class="panel-heading" style="background-color: #FFE4E1;"><table width="100%"><tr><td width="95%">\
                    <h3><a href="#content_list_tab" role="tab" data-toggle="tab" onclick="InitContentListTab('+data[i][3]+', '+userId+')">'+data[i][0]+'</a></h3></td>\
                    <td><a href="#" data-toggle="modal" data-target="#edit_title" onclick="InitEditTitle('+data[i][3]+', '+userId+', \''+data[i][0]+'\')">编辑</a></td></tr></table>\
                    </div><div class="panel-body" style="background-color: #FFF5EE;">\
                    <table width="100%"><tr><td width="80%">创建人：'+data[i][2]+'</td><td>创建时间：'+data[i][1]+'</td></tr></div></div>';
    }
}

// 将用户分类数据展示到title_tab中，不可操作
function ShowGuestTitle(data, userId){
    var div = document.getElementById('title_tab');
    for(var i = 0; i<data.length; i++){
        div.innerHTML = div.innerHTML + '<div class="panel panel-default">\
                    <div class="panel-heading" style="background-color: #FFE4E1;"><h3>\
                    <a href="#content_list_tab" role="tab" data-toggle="tab" onclick="InitContentListTab('+data[i][3]+', '+userId+')">'+data[i][0]+'</a></h3>\
                    </div><div class="panel-body" style="background-color: #FFF5EE;">\
                    <table width="100%"><tr><td width="80%">创建人：'+data[i][2]+'</td><td>创建时间：'+data[i][1]+'</td></tr></div></div>';
    }
}

// 编辑标题模态框初始化
function InitEditTitle(titleId, userId, title){
    document.getElementById('edit_title_name').value = title;
    document.getElementById('edit_title_footer').innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>\
                    <button type="submit" class="btn btn-danger" data-dismiss="modal" onclick="DeleteTitle('+titleId+', '+userId+')">删除</button>\
               <button type="submit" class="btn btn-primary" data-dismiss="modal" onclick="EditTitle('+titleId+', '+userId+')">提交</button>'
}

// 删除标题
function DeleteTitle(titleId, userId){
    $.ajax({
        url: "/title",
        type: "delete",
        data: {titleId: titleId},
        success: function(arg){
            InitTitleTab(userId);
            ShowSeccussAlert();
        },error: function(arg){
            ShowFailAlert();
        }
    })
}

// 编辑标题
function EditTitle(titleId, userId){
    var title = document.getElementById('edit_title_name').value;
    if(title == ''){
        ShowMsgAlert('警告', '标题不能为空啊');
        return
    }
    $.ajax({
        url: "/title",
        type: "put",
        data: {titleId: titleId, title: title, hidden: document.getElementById('edit_title_hidden').value},
        success: function(arg){
            InitTitleTab(userId);
            ShowSeccussAlert();
        },error: function(arg){
            ShowFailAlert();
        }
    })
}