        // JavaScript to handle row selection toggle
        function selectOrder(radio) {
            const selectedRow = radio.closest('tr');
            
            // Check if the radio button is already selected (toggle logic)
            if (selectedRow.classList.contains('selected-row')) {
                // If the row is already selected, deselect it and uncheck the radio button
                selectedRow.classList.remove('selected-row');
                radio.checked = false;
            } else {
                // Deselect all other rows first
                const rows = document.getElementById('ordersTableBody').getElementsByTagName('tr');
                for (let row of rows) {
                    row.classList.remove('selected-row');
                    const input = row.querySelector('input[type="radio"]');
                    if (input) input.checked = false; // Uncheck any previously selected radio button
                }
    
                // Select the clicked row and apply the effects
                selectedRow.classList.add('selected-row');
                radio.checked = true;
            }
        }