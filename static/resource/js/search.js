// 搜索
function Search(userId){
    var key = document.getElementById('search_key').value;
    if(key == ''){
        ShowMsgAlert('警告', '搜索内容不能为空');
        return
    }
    $.ajax({
        url: "/search",
        type: "get",
        data: {key: key, userId: userId},
        success: function(arg){
            var results = jQuery.parseJSON(arg);
            ShowUserTitle(results['user'], userId, 'search_title');
            ShowGuestTitle(results['guest'], userId, 'search_title');
            ShowSearchUContentList(results['ucontent'], results['gcontent'], userId);
        }
    })
}

// 展示search content list数据
function ShowSearchUContentList(data, data1, userId){
    var div = document.getElementById('search_content');
    div.innerHTML = '';
    for(var i = 0; i<data.length; i++){
        div.innerHTML = div.innerHTML + '<div class="panel panel-default">\
        <div class="panel-heading" style="background-color: #FFE4E1;"><h3><a href="#content" role="tab" data-toggle="tab" \
        onclick="InitContentTab('+data[i][2]+', '+data[i][3]+', '+userId+')">'+data[i][0]+'</a></h3></div>\
        <div class="panel-body" style="background-color: #FFF5EE;">最后编辑时间：'+data[i][1]+'</div></div>';
    }
    for(var i = 0; i<data1.length; i++){
        div.innerHTML = div.innerHTML + '<div class="panel panel-default">\
        <div class="panel-heading" style="background-color: #FFE4E1;"><h3><a href="#content" role="tab" data-toggle="tab" \
        onclick="InitContentTab('+data1[i][2]+', '+data1[i][3]+', '+userId+')">'+data1[i][0]+'</a></h3></div>\
        <div class="panel-body" style="background-color: #FFF5EE;">最后编辑时间：'+data1[i][1]+'</div></div>';
    }
}
