let form = document.querySelector('form');

form.onsubmit = (event) => {
  event.preventDefault();

  var password1 = document.getElementById("password1").value;
  var password2 = document.getElementById("password2").value;

  if (password1 === password2) {
    form.submit();
  } else {
    msgbox = document.getElementById("msg-box");
    msgbox.innerHTML += `<div class="alert alert-warning alert-dismissible fade show" role="alert"><strong>WARNING</strong> Passwords not match<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`
    document.getElementById("password2").focus();
  }
}


function handleAgree() {
  var checkbox = document.getElementById('agreeCheckbox');
  checkbox.checked = true;
  const modal = bootstrap.Modal.getInstance(document.getElementById('termsModal'));
  modal.hide();
}

