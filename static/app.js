$(document).ready(function () {

    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function () {

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");

    });
});

$(document).on("click", "#addCollection", async function () {
    const id = $(this).attr('data-id');
    const result = await axios.post(`/api/collection/add`, { id: id });
    if (result.data == "added") {
        $(this).html("<i class='far fa-check-square'></i> <span>&nbsp;</span> Collected");
        $(this).attr("class", "button is-info");
        $(this).attr("id", "");
    } else {
        $("#collection_error").html("<p>Can't add that to your collection when not logged in</p")
    }
});
