// 网盘tab初始化
function InitPanTab(user){
    document.getElementById('path').value = 'static\\pan\\' + user;
    GetFolder(document.getElementById('path').value);
}

// 访问指定的文件夹
function GetFolder(path){
    $.ajax({
        url: "/pan",
        type: "get",
        data: {path: path},
        success: function(arg){
            ShowPan(jQuery.parseJSON(arg));
        }
    })
}

// 展示网盘内容
function ShowPan(data){
    var table = document.getElementById('pan_table');
    document.getElementById('path').value = data['current'];
    table.innerHTML = '<tr><td><h4>当前文件夹：'+data['current']+'</h4></td></tr>';
    table.innerHTML = table.innerHTML + '<tr><td><a href="#" onclick="GetFolder(\''+data['last']+'\')" \
                                        class="glyphicon glyphicon-arrow-left">&nbsp;上一层目录</a></td></tr>';
    for(var i = 0; i<data['folders'].length; i++){
        table.innerHTML = table.innerHTML + '<tr><td><a href="#" onclick="GetFolder(\''+data['folders'][i]+'\')" \
                                class="glyphicon glyphicon-folder-open">&nbsp;'+data['folders'][i]+'</a></td></tr>';
    }
    for(var i = 0; i<data['files'].length; i++){
        var filename = data['files'][i].split('/').pop();
        table.innerHTML = table.innerHTML + '<tr><td><a href="'+data['files'][i]+'" download="'+filename+'" \
                                class="glyphicon glyphicon-file">&nbsp;'+data['files'][i]+'</a></td></tr>';
    }
}

// 添加文件夹
function AddFolder(){
    var folder = document.getElementById('folder_name').value;
    var current = document.getElementById('path').value;
    if(folder == ''){
        ShowMsgAlert('警告', '文件名不能为空哦');
        return
    }
    $.ajax({
        url: "/pan",
        type: "put",
        data: {folder: folder, current: current},
        success: function(arg){
            GetFolder(current);
        }
    })
}

// 上传文件
function AddFile(){
    var file = document.getElementById('file');
    var current = document.getElementById('path').value;
    if(file.value == ''){
        ShowMsgAlert('警告', '你都没选择文件');
        return
    }
    ShowMsgAlert('警告', '正在上传文件，别乱点好吗');
    var d = new FormData();
    d.append('file', file.files[0]);
    d.append('filename', file.value);
    d.append('current', current);
    $.ajax({
        url: "/pan",
        type: "post",
        processData: false,
        contentType: false,
        async: false,
        cache: false,
        data: d,
        success: function(arg){
            $('#upload_file').modal('hide');
            ShowSeccussAlert();
            GetFolder(current);
        }
    })
}