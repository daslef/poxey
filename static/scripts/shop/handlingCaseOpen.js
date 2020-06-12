const handlingCaseOpen = (openCase) => {
    $.ajax({
        url: "/shop",
        method: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({"openCase": openCase})
    });
}