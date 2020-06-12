const handlingCaseOpen = (openCase) => {

    fetch('/shop', {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({openCase})
    })
    .then(response => response.json())
    .then(data => {
        // console.log(data)
        document.querySelector('.shop--drop--content').innerHTML = JSON.stringify(data)
    })
    .catch(err => console.log(err));

}