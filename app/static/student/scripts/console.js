let init_btn = $('#init_btn');

init_btn.click(() => {
    $.ajax({
        url: '/study/init_students',
        type: 'GET',
        success: (result) => {
            alert(result);
        }
    })
});

$('.auto_btn').click((e) => {
    let target_btn = $(e.target);
    let student_name = target_btn.text();
    $.ajax({
        url: '/study/change_auto',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'student_name': student_name}),
        success: (result) => {
            if (result === 'False') {
                target_btn.removeClass('btn-primary').addClass('btn-light');
            } else if (result === 'True') {
                target_btn.removeClass('btn-light').addClass('btn-primary');
            }
        }
    });
});