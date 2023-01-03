//动态导入jQuery
var jquery = document.createElement('script');
jquery.src = 'https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js';
document.getElementsByTagName('head')[0].appendChild(jquery);

document.onreadystatechange = function () {
    if (document.readyState === 'complete') {
        record();
        setTimeout(show_scores, 100);
    }

}

function record() {
    let key_list = []
    for (let i = 0; i < localStorage.length; i++) {
        let key = localStorage.key(i);
        if (key.indexOf('BlockLibrary') === -1) {
            key_list.push(key);
        }
    }

    $.ajax({
        url: '/record',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'key_list': key_list}),
        success: function (result) {
            console.log(result);
        }
    });
}

function show_scores() {
    $('.farSide').eq(0).prepend("<button id='show_scores'>排行榜</button>");
    $('#show_scores').click(() => {
        let appName = location.pathname.match(/\/([-\w]+)(\.html)?$/);
        appName = appName ? appName[1].replace('-', '/') : 'index';
        window.location = '/show_scores?game=' + appName;
    });
}

