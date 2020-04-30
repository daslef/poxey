const form = document.getElementById('form');
const username = document.getElementById('username');
const email = document.getElementById('email');
const password = document.getElementById('password');
const password2 = document.getElementById('password2');

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

function checkEmail(input) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    
    if (re.test(input.value.trim())) {
        showSuccess(input);
        return true;
    }
    else {
        showError(input, "E-Mail некорректный");
        return false;
    }
}

function checkRequired(inputArr) {
    let isValid = true;
    inputArr.forEach(function(input) {
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

function checkPasswordsMatch(input1, input2) {
    if (input1.value !== input2.value) {
        showError(input2, "Пароли не совпадают");
        return false;
    }
    else {
        return true;
    }
}

function getFieldName(input) {
    return input.id.charAt(0).toUpperCase() + input.id.slice(1); 
}

form.addEventListener('submit', function(e) {
    
    let isValidRequired = checkRequired([username, email, password, password2]);
    let isValidNameLength = checkLength(username, 4, 15);
    let isValidPasswordLength = checkLength(password, 6, 25);
    let isValidEmail = checkEmail(email);
    let isPasswordMatches = checkPasswordsMatch(password, password2);
    
    if(isValidRequired && isValidNameLength && isValidPasswordLength && isValidEmail && isPasswordMatches) {
        form.submit();
    }
    else {
        e.preventDefault();
    }
});