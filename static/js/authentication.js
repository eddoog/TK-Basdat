const signUpButton = document.getElementById('signUp');

const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () =>
    container.classList.add('right-panel-active')
);

signInButton.addEventListener('click', () =>
    container.classList.remove('right-panel-active')
);

const loginForm = document.querySelector('[data-login]');

console.log(loginForm);

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    console.log(e);

    const formData = new FormData(loginForm);

    const data = {};
    for (const [name, value] of formData) {
        data[name] = value;
        console.log(`Name: ${name}, Value: ${value}`);
    }

    console.log(data);
});

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
        if (radio.value === 'Panitia' && radio.checked) {
            jabatanInput.classList.remove('hide');
            jabatanInput.setAttribute('required', true);
        } else {
            jabatanInput.classList.add('hide');
            jabatanInput.removeAttribute('required');
        }
    });
}

multiStepForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(multiStepForm);
    const data = {};
    for (const [name, value] of formData) {
        if (
            name === 'jabatan' &&
            document.querySelector('input[name="role"]:checked').value !==
                'Panitia'
        ) {
            continue;
        }
        data[name] = value;
    }
    console.log(data);
});
