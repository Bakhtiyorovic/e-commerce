document.addEventListener("DOMContentLoaded", function () {
    let buttons = document.querySelectorAll(".add-cart");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            let productId = this.getAttribute("data-id");

            fetch("/add-to-cart/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({ product_id: productId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Mahsulot savatchaga qo‘shildi!");
                } else {
                    alert("Xatolik yuz berdi!");
                }
            });
        });
    });

    function getCSRFToken() {
        let csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]");
        return csrfToken ? csrfToken.value : "";
    }
});
