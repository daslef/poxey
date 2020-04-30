const form = document.getElementById('form');
const username = document.getElementById('username');
const password = document.getElementById('password');

function showError(input, msg) {
    const formControl = input.parentElement;
    const small = formControl.querySelector('small');
    formControl.className = 'form-control error';
    small.innerText = msg;
}

function showSuccess(input) {
    const formControl = input.parentElement;
    formControl.className = 'form-control success';
}

function checkRequired(inputArray) {
    let isValid = true;
    inputArray.forEach(input => {
        if (input.value.trim() === "") {
            showError(input, `Данное поле обязательно`);
            isValid = false;
        }
        else {
            showSuccess(input);
        } 
    });
    return isValid;
}

function checkLength(input, min, max) {
    if (input.value.length < min) {
        showError(input, `Поле должно состоять хотя бы из ${min} символов`);
        return false;
    }
    else if (input.value.length > max) {
        showError(input, `Поле должно состоять из меньше ${max} символов`);
        return false;
    }
    else {
        showSuccess(input);
        return true;
    }
}

function getFieldName(input) {
    return input.id.charAt(0).toUpperCase() + input.id.slice(1); 
}

form.addEventListener('submit', function(e) {
    let isValid = checkRequired([username, password]);
    let isValidNameLength = checkLength(username, 4, 15);
    let isValidPasswordLength = checkLength(password, 6, 25);
    
    if(isValid && isValidNameLength && isValidPasswordLength) {
        form.submit();
    }
    else {
        e.preventDefault();
    }
});