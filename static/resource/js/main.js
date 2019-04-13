// 注册时判断两次密码是否输入正确，正确才可以提交
function IsPasswordCheck(){
    var p1 = document.getElementById('register_password').value;
    var p2 = document.getElementById('register_repassword').value;
    if(p1 == p2){
        document.getElementById('register_btnsub').removeAttribute('disabled');
    }else{
        document.getElementById('register_btnsub').setAttribute('disabled', true);
    }
}

// 登录
function Login(){
    var login_email = document.getElementById('login_email').value;
    var login_password = document.getElementById('login_password').value;
    $.ajax({
        url: "/",
        type: "put",
        data: {login_password: login_password, login_email: login_email, hidden: 'login'},
        success: function(arg){
            var reselts = jQuery.parseJSON(arg);
            if(reselts[0] == '1'){
                ShowMsgAlert('警告', '账号密码输入错误');
            }else{
                window.location.reload();
            }
        }
    })
}

// 注销
function CancelLogin(){
    $.ajax({
        url: "/",
        type: "delete",
        data: {},
        success: function(arg){
            window.location.reload();
        }
    })
}

// 修改用户信息时判断两次密码输入是否一致
function IsInfoPasswordCheck(){
    var p1 = document.getElementById('info_password').value;
    var p2 = document.getElementById('info_repassword').value;
    if(p1 == p2){
        document.getElementById('info_btnsub').removeAttribute('disabled');
    }else{
        document.getElementById('info_btnsub').setAttribute('disabled', true);
    }
}

// 操作成功警告框弹出
function ShowSeccussAlert(){
    $('#success_alert').modal('show');
}

// 操作失败警告框弹出
function ShowFailAlert(){
    $('#fail_alert').modal('show');
}

// 提示信息模态框
function ShowMsgAlert(header, boby){
    document.getElementById('msg_header').innerHTML = header;
    document.getElementById('msg_body').innerHTML = boby;
    $('#msg_alert').modal('show');
}

// 添加更新记录
function Update(){
    var version = document.getElementById('version').value;
    var content = document.getElementById('update_content').value;
    if(version=='' || content==''){
        ShowMsgAlert('警告', '输入框不能为空啊');
        return
    }
    $.ajax({
        url: "/update",
        type: "post",
        data: {version: version, content: content},
        success: function(arg){
            InitUpdateList();
        }
    })
}

// 更新列表更新
function InitUpdateList(){
    $.ajax({
        url: "/update",
        type: "get",
        data: {},
        success: function(arg){
            ShowUpdateList(jQuery.parseJSON(arg));
        }
    })
}

// 展示更新列表
function ShowUpdateList(data){
    var div = version = document.getElementById('update_list');
    div.innerHTML = '<div class="panel panel-default"><div class="panel-heading" style="background-color: #FFE4E1;">\
                        <h3>更新内容</h3></div></div>';
    for(var i = 0; i<data.length; i++){
        div.innerHTML = div.innerHTML + '<div class="panel panel-default"><div class="panel-heading" style="background-color: #FFE4E1;">\
                      <table width="100%"><tr><td width="80%"><h3>'+data[i][0]+'</h3></td><td>更新时间：'+data[i][2]+'</td></tr></table></div>\
                      <div class="panel-body" style="background-color: #FFF5EE;">'+data[i][1]+'</div></div>';
    }
}

// 更换背景图片
function Bg(){
    var bg = document.getElementById('bg_file');
    if(bg.value == ''){
        ShowMsgAlert('警告', '图片不能为空啊');
        return
    }
    var d = new FormData();
    d.append('bg', bg.files[0]);
    $.ajax({
        url: "/update",
        type: "put",
        data: d,
        processData: false,
        contentType: false,
        async: false,
        cache: false,
        success: function(arg){
            ShowSeccussAlert();
            window.location.reload();
        }
    })
}

// 更新公告
function Notice(){
    var content = document.getElementById('notice_content').value;
    if(content == ''){
        ShowMsgAlert('警告', '内容不能为空啊');
        return
    }
    $.ajax({
        url: "/update",
        type: "delete",
        data: {type: '2', content: content},
        success: function(arg){
            ShowSeccussAlert();
            ShowNotice();
        }
    })
}

// 展示公告
function ShowNotice(){
    $.ajax({
        url: "/update",
        type: "delete",
        data: {type: '1'},
        success: function(arg){
            document.getElementById('notice').innerHTML = jQuery.parseJSON(arg)[0];
        }
    })
}

