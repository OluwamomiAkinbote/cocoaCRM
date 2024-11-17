function copyOrderDetails(orderId) {
    // Get each detail by the order ID and store in variables
    var orderIdElement = document.getElementById("order-id-" + orderId).textContent;
    var customerName = document.getElementById("customer-name-" + orderId).textContent;
    var whatsappNumber = document.getElementById("whatsapp-number-" + orderId).textContent;
    var phoneNumber = document.getElementById("phone-number-" + orderId).textContent;
    var email = document.getElementById("email-" + orderId).textContent;
    var address = document.getElementById("address-" + orderId).textContent;
    var productName = document.getElementById("product-name-" + orderId).textContent;
    var quantity = document.getElementById("quantity-" + orderId).textContent;
    var totalPrice = document.getElementById("total-price-" + orderId).textContent;
    var state = document.getElementById("state-" + orderId).textContent;

    // Concatenate order details
    var orderDetails = `Order ID: ${orderIdElement}\nCustomer: ${customerName}\nWhatsApp Number: ${whatsappNumber}\nPhone: ${phoneNumber}\nEmail: ${email}\nAddress: ${address}\nState: ${state}\nQuantity: ${quantity}\nTotal Price: ${totalPrice}\nProduct: ${productName}`;

    // Create a temporary input element to hold the text to copy
    var tempInput = document.createElement("textarea");
    document.body.appendChild(tempInput);
    tempInput.value = orderDetails; // Set the value to the order details
    tempInput.select();  // Select the text content
    document.execCommand("copy");  // Copy to clipboard
    document.body.removeChild(tempInput);  // Remove the temporary input

    // Provide visual feedback on the copy action
    var copyButton = document.querySelector(`#copy-button-${orderId}`);
    copyButton.innerHTML = '<i class="fa fa-check"></i>';  // Change to check icon
    copyButton.style.color = 'green';

    // Revert the icon and color after 2 seconds
    setTimeout(function() {
        copyButton.innerHTML = '<i class="fa fa-copy text-xs text-gray-600"></i>';  // Restore copy icon
        copyButton.style.color = ''; 
    }, 2000);
}

