document.addEventListener('DOMContentLoaded', () => {
    'use strict';

    (function () {
        const forms = document.querySelectorAll('.needs-validation');
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    })();

    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 6000);
    });

    const cardInput = document.querySelector('input[placeholder="4242 4242 4242 4242"]');
    if (cardInput) {
        cardInput.addEventListener('input', e => {
            let val = e.target.value.replace(/\s/g, '').replace(/\D/g, '');
            val = val.match(/.{1,4}/g)?.join(' ') || val;
            e.target.value = val.substring(0, 19);
        });
    }

    const expiryInput = document.querySelector('input[placeholder="MM/YY"]');
    if (expiryInput) {
        expiryInput.addEventListener('input', e => {
            let val = e.target.value.replace(/\D/g, '');
            if (val.length > 2) val = val.substring(0, 2) + '/' + val.substring(2, 4);
            e.target.value = val;
        });
    }

    const cvvInput = document.querySelector('input[placeholder="***"]');
    if (cvvInput) {
        cvvInput.addEventListener('input', e => {
            e.target.value = e.target.value.replace(/\D/g, '').substring(0, 4);
        });
    }

    const phoneInput = document.querySelector('input[type="tel"]');
    if (phoneInput) {
        phoneInput.addEventListener('input', e => {
            let val = e.target.value.replace(/[^\d+\-]/g, '');
            e.target.value = val.substring(0, 20);
        });
    }

    document.querySelectorAll('a[data-confirm]').forEach(link => {
        link.addEventListener('click', e => {
            if (!confirm(link.dataset.confirm)) e.preventDefault();
        });
    });
});
