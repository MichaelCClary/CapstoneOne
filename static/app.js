$(document).ready(function () {

    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function () {

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");

    });
});

async function toggleCollection(id) {
    return await axios.post(`/api/collection/toggle`, { id: id }).then(res => res.data);
}

function toggleCollectionButtons(res, id) {
    if (res == "added") {
        $(`#${id}`).html("<i class='far fa-check-square'></i> <span>&nbsp;</span> Collected");
        $(`#${id}`).attr("class", "button is-info toggleCollection");
    } else if (res == "removed") {
        $(`#${id}`).html("Add to Collection");
        $(`#${id}`).attr("class", "button is-success toggleCollection");
    }
}

function removeFromCollection(res, id) {
    if (res == "removed") {
        $(`#${id}-tile`).remove();
    }
}

$(document).on("click", ".toggleCollection", function () {
    const id = $(this).attr('id');
    toggleCollection(id)
        .then(res => toggleCollectionButtons(res, id))
});


$(document).on("click", ".deleteFromCollection", function () {
    const id = $(this).attr('id');
    toggleCollection(id)
        .then(res => removeFromCollection(res, id))
});

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

function keepSearchParams() {
    const urlParams = new URLSearchParams(window.location.search);
    let searchby = urlParams.get('searchby')
    if (searchby == null) {
        searchby = 'name'
    }
    $(`#${searchby}`).parent().parent().show()
}



hideFields()
keepSearchParams()