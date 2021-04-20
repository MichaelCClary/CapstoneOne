$(document).ready(function () {

    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function () {

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");

    });
});

$(document).on("click", ".addCollection", function () {
    const id = $(this).attr('id');
    console.log(id)
    addToCollection(id)
});


async function addToCollection(id) {
    const result = await axios.post(`/api/collection/add`, { id: id });
    if (result.data == "added") {
        $(`#${id}`).html("<i class='far fa-check-square'></i> <span>&nbsp;</span> Collected");
        $(`#${id}`).attr("class", "button is-info");
    } else {
        $(`#${id}_collection_error`).html("<p>Can't add that to your collection when not logged in</p")
    }
}

$(document).on("change", "#searchby", function () {
    const val = $(this).val();
    hideFields();
    $(`#${val}`).parent().parent().show()
});

function hideFields() {
    const elementsArr = [
        $('#mechanics'),
        $('#name'),
        $('#categories'),
        $('#min_players'),
        $('#max_players'),
    ];
    elementsArr.forEach($elem => $elem.parent().parent().hide());
}

hideFields()