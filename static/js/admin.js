document.addEventListener('DOMContentLoaded', function () {
    const productSelect = document.querySelector('#id_product');
    const productEntrySelect = document.querySelector('#id_product_entry');

    productSelect.addEventListener('change', function () {
        const productId = this.value;
        fetch(`/admin/get_product_entries/${productId}/`)
            .then(response => response.json())
            .then(data => {
                productEntrySelect.innerHTML = '';  // Clear existing options
                data.entries.forEach(entry => {
                    const option = document.createElement('option');
                    option.value = entry.id;
                    option.textContent = entry.quantity + ' of ' + entry.product.name;
                    productEntrySelect.appendChild(option);
                });
            });
    });
});
