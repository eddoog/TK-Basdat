const signUpButton = document.getElementById('signUp');

const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () =>
    container.classList.add('right-panel-active')
);

signInButton.addEventListener('click', () =>
    container.classList.remove('right-panel-active')
);

const multiStepForm = document.querySelector('[data-multistep]');
const formSteps = [...multiStepForm.querySelectorAll('[data-step]')];
let currentStep = formSteps.findIndex((step) => {
    return step.classList.contains('active');
});

if (currentStep < 0) {
    currentStep = 0;
    showCurrentStep();
}

multiStepForm.addEventListener('click', (e) => {
    let incrementor;
    if (e.target.matches('[data-next]')) {
        incrementor = 1;
    } else if (e.target.matches('[data-previous]')) {
        incrementor = -1;
    }

    if (incrementor == null) return;

    const inputs = [...formSteps[currentStep].querySelectorAll('input')];
    const allValid = inputs.every((input) => input.reportValidity());
    if (allValid) {
        currentStep += incrementor;
        showCurrentStep();
    }
});

formSteps.forEach((step) => {
    step.addEventListener('animationend', (e) => {
        formSteps[currentStep].classList.remove('hide');
        e.target.classList.toggle(
            'hide',
            !e.target.classList.contains('active')
        );
    });
});

function showCurrentStep() {
    formSteps.forEach((step, index) => {
        step.classList.toggle('active', index === currentStep);
    });
}

const roleRadios = document.getElementsByName('role');
const jabatanInput = document.getElementsByName('jabatan')[0];

for (const radio of roleRadios) {
    radio.addEventListener('click', () => {
        if (radio.value === 'panitia' && radio.checked) {
            jabatanInput.classList.remove('hide');
            jabatanInput.setAttribute('required', true);
        } else {
            jabatanInput.classList.add('hide');
            jabatanInput.removeAttribute('required');
        }
    });
}

function showError(message) {
    $('#errorMessage').html('');
    const text = `<p class="text-danger font-bold text-center">${message}</p>`;
    $(text).appendTo('#errorMessage');
}

$(document).ready(function () {
    $('#loginSubmit').submit(function (e) {
        e.preventDefault();
        var username = $('#usernameLoginForm').val();
        var password = $('#passwordLoginForm').val();
        if (username === '' || password === '') {
            showError(
                'Data yang diisikan belum lengkap, silakan lengkapi data terlebih dahulu.'
            );
        } else {
            $.ajax({
                method: 'POST',
                url: '',
                data: {
                    username: username,
                    password: password,
                    type: 'login',
                },
                success: function (data) {
                    window.location.href = `${window.location.protocol}//${window.location.host}/dashboard/`;
                },
                error: function (error) {
                    showError('Email atau password tidak valid');
                },
            });
        }
    });

    $('#registerSubmit').submit(function (e) {
        e.preventDefault();
        var email = $('#emailRegisterForm').val();
        var username = $('#usernameRegisterForm').val();
        var password = $('#passwordRegisterForm').val();
        var namaDepan = $('#namaDepanRegisterForm').val();
        var namaBelakang = $('#namaBelakangRegisterForm').val();
        var role = $('input[name="role"]:checked').val();
        var jabatan = $('#jabatanRegisterForm').val();
        var status = $('input[name="status"]:checked')
            .serializeArray()
            .map(function (item) {
                return item.value;
            });
        var alamat = $('#alamatRegisterForm').val();
        var nomorHP = $('#nomorHPRegisterForm').val();
        if (
            email === '' ||
            username === '' ||
            password === '' ||
            namaDepan === '' ||
            namaBelakang === '' ||
            role === '' ||
            status.length === 0 ||
            alamat === '' ||
            nomorHP === ''
        ) {
            showError(
                'Data yang diisikan belum lengkap, silakan lengkapi data terlebih dahulu.'
            );
        } else {
            $.ajax({
                method: 'POST',
                url: '',
                data: {
                    username: username,
                    password: password,
                    email: email,
                    namaDepan: namaDepan,
                    namaBelakang: namaBelakang,
                    role: role,
                    jabatan: jabatan,
                    status: status,
                    alamat: alamat,
                    nomorHP: nomorHP,
                    type: 'register',
                },
                success: function (data) {
                    window.location.href = `${window.location.protocol}//${window.location.host}/dashboard/`;
                },
                error: function (xhr) {
                    var error = xhr.responseJSON.error;
                    showError(error);
                },
            });
        }
    });
});
