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