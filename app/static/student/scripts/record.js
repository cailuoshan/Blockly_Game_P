let record_btn = $('#record_btn');
let student_name_input = $('#student_name');

let student_name = localStorage.getItem('student_name');
if(student_name !== null){
    student_name_input.val(student_name);
}

record_btn.click(()=>{
    $.ajax({
        url: '/study/record_one',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'student_name': student_name_input.val()}),
        success: (result)=>{
            record_btn.text(result);
            record_btn.addClass('text-success');
        }
    });
    localStorage.setItem('student_name', student_name_input.val());
});