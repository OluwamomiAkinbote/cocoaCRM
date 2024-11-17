function fetchProductEntries(productId) {
    const url = $('#ajax-endpoint').data('url');  // Get the URL from the data attribute
    if (productId) {
        $.ajax({
            url: url,  // Use the URL from the data attribute
            type: "GET",
            data: {
                'product_id': productId
            },
            success: function(data) {
                $('#product_entry').empty().append('<option value="">-- Select a product entry --</option>');
                $.each(data, function(index, entry) {
                    $('#product_entry').append('<option value="' + entry.id + '">' + entry.quantity + ' of ' + entry.product_name + ' at ' + entry.selling_price + '</option>');
                });
            },
            error: function(xhr, status, error) {
                console.error("AJAX Error:", status, error);
            }
        });
    } else {
        $('#product_entry').empty().append('<option value="">-- Select a product entry --</option>');
    }
}


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('country').addEventListener('change', function () {
        var countryId = this.value; // Get the selected country ID

        // Proceed only if a country is selected
        if (countryId) {
            fetch(`/states/?country_id=${countryId}`) // Use country_id for fetching states
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    var stateSelect = document.getElementById('state_or_region');
                    stateSelect.innerHTML = '<option value="">-- Select a state/region --</option>';
                    if (data.length) { // Check if there are states returned
                        data.forEach(function (state) {
                            var option = document.createElement('option');
                            option.value = state.id; // Use state ID for the option value
                            option.textContent = state.name; // Display state name
                            stateSelect.appendChild(option);
                        });
                    }
                })
                .catch(error => {
                    console.error("Error fetching states:", error);
                });
        } else {
            // Clear the state selection if no country is selected
            var stateSelect = document.getElementById('state_or_region');
            stateSelect.innerHTML = '<option value="">-- Select a state/region --</option>';
        }
    });
});