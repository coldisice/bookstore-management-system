document.addEventListener("DOMContentLoaded", function () {

    function recalculateOrder() {
        let total = 0;

        document.querySelectorAll("tr.form-row").forEach(row => {
            const priceInput = row.querySelector('input[name$="-price"]');
            const quantityInput = row.querySelector('input[name$="-quantity"]');

            if (!priceInput || !quantityInput) {
                return;
            }

            const price = parseFloat(priceInput.value) || 0;
            const quantity = parseInt(quantityInput.value) || 0;

            total += price * quantity;
        });

        const totalInput = document.querySelector("#id_total_price");

        if (totalInput) {
            totalInput.value = total.toFixed(2);
        }
    }

    function bindRow(row) {

        const bookSelect = row.querySelector('select[name$="-book"]');
        const priceInput = row.querySelector('input[name$="-price"]');
        const quantityInput = row.querySelector('input[name$="-quantity"]');

        if (bookSelect) {

            bookSelect.addEventListener("change", function () {

                if (!this.value) {
                    return;
                }

                fetch(`/admin/orders/order/book-price/${this.value}/`)
                    .then(response => response.json())
                    .then(data => {

                        if (priceInput) {
                            priceInput.value = data.price;
                        }

                        recalculateOrder();

                    });

            });

        }

        if (quantityInput) {

            quantityInput.addEventListener("input", recalculateOrder);
            quantityInput.addEventListener("change", recalculateOrder);

        }

        if (priceInput) {

            priceInput.addEventListener("input", recalculateOrder);

        }

    }

    function init() {

        document.querySelectorAll("tr.form-row").forEach(bindRow);

        recalculateOrder();

    }

    init();

    document.addEventListener("formset:added", function (event) {

        bindRow(event.target);

    });

});