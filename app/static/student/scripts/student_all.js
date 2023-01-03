let copy_btn = $('#copy_btn');

function copy(text) {
    // text是复制文本
    // 创建input元素
    const element = document.createElement('input');
    // 给input元素赋值需要复制的文本
    element.setAttribute('value', text);
    // 将input元素插入页面
    document.body.appendChild(element);
    // 选中input元素的文本
    element.select();
    // 复制内容到剪贴板
    document.execCommand('copy');
    // 删除input元素
    document.body.removeChild(element);
    copy_btn.text('复制成功！');
    copy_btn.addClass('text-success');
    setTimeout(()=>{
        copy_btn.text('复制学生名单');
        copy_btn.removeClass('text-success');
    }, 1000);
}

copy_btn.click(()=>{
    let students_list = $('#students_list').text();
    students_list = students_list.trim().replaceAll(' ', '').replaceAll('\n\n', '\n').split('\n')
    students_list = students_list.toString().replaceAll(',', ' ');
    copy(students_list);
});

