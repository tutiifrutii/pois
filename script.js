form = document.getElementById("form");
input = document.getElementById("input");

const sendRequest = async (e, searchText) => {
    e.preventDefault();
    const response = await fetch(`/search?${searchText}`, {
        method: "POST",
    });
    if (response) {
        location.reload()
        return await response.text()
    }
}

form.addEventListener("submit", (e) => {
    sendRequest(e, input.value)
        .then(r => { console.log(r) });
});
