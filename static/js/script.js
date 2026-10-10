// Interactive scripts for eCommerce store

document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss alert notifications after 4 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });

    // Quantity selectors in product detail page
    const qtyInputs = document.querySelectorAll('.qty-input');
    qtyInputs.forEach(input => {
        const decreaseBtn = input.parentElement.querySelector('.btn-decrease');
        const increaseBtn = input.parentElement.querySelector('.btn-increase');

        if (decreaseBtn) {
            decreaseBtn.addEventListener('click', (e) => {
                e.preventDefault();
                let val = parseInt(input.value) || 1;
                if (val > 1) {
                    input.value = val - 1;
                }
            });
        }

        if (increaseBtn) {
            increaseBtn.addEventListener('click', (e) => {
                e.preventDefault();
                let val = parseInt(input.value) || 1;
                input.value = val + 1;
            });
        }
    });

    // Confirmation on item removal
    const deleteForms = document.querySelectorAll('.delete-item-btn');
    deleteForms.forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (!confirm('Are you sure you want to remove this item from your cart?')) {
                e.preventDefault();
            }
        });
    });
});
