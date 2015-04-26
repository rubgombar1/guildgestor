/**
 * Created by juanlu on 31/03/15.
 */

var actual_page = 1;

function change_page(group, page) {
    actual_page = page;
    $("."+group).hide();
    $("."+group+page).show();
    $(".li"+group).removeClass('active');
    $(".li"+group).show();
    $(".li"+group+page).addClass('active');
}
function next_page(group, max){
    if (actual_page < max){
        actual_page = actual_page + 1;
    }
    change_page(group, actual_page);
}
function last_page(group){
    if (actual_page >1){
        actual_page = actual_page - 1;
    }
    change_page(group, actual_page);
}