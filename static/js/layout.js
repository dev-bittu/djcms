var login = document.querySelector('#loginBtn');
var register = document.querySelector('#registerBtn');

if (window.matchMedia("(min-width: 992px)").matches) {
    login.classList.remove("nav-link");
    login.classList.add('btn', 'btn-outline-light', 'rounded-pill', 'me-2');

    register.classList.remove("nav-link");
    register.classList.add('btn', 'btn-light', 'rounded-pill');
}
