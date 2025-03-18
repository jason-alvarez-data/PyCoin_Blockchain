// Function to format timestamps
function formatTimestamp(timestamp) {
    // Convert nanoseconds to milliseconds and handle potential string input
    const ts = typeof timestamp === 'string' ? parseInt(timestamp) : timestamp;
    const date = new Date(ts / 1000000);
    return date.toLocaleString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// Initialize any elements that need formatting when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Format all timestamps elements
    const timestampElements = document.querySelectorAll('.timestamp');
    timestampElements.forEach(element => {
        const timestamp = parseInt(element.textContent);
        if (!isNaN(timestamp)) {
            element.textContent = formatTimestamp(timestamp);
        }
    });

    // Setup mining button if it exists
    const mineButton = document.getElementById('mine-btn');
    if (mineButton) {
        mineButton.addEventListener('click', function() {
            // Show loading state
            mineButton.textContent = 'Mining...';
            mineButton.disabled = true;

            // Call the mining endpoint
            fetch('/mine')
                .then(response => response.json())
                .then(data => {
                    alert('Block mined successfully!');
                    // Reload the page to show the new block
                    location.reload();
                })
                .catch(error => {
                    alert('Error mining block: ' + error);
                    mineButton.textContent = 'Mine New Block';
                    mineButton.disabled = false;
                });
        });
    }

    // Set up transaction form if it exists
    const transactionForm = document.getElementById('transaction-form');
    if (transactionForm) {
        transactionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const recipient = document.getElementById('recipient').value;
            const amount = document.getElementById('amount').value;
            
            fetch('/transactions/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    recipient: recipient,
                    amount: parseFloat(amount)
                })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.transaction_id) {
                    location.reload();
                }
            })
            .catch(error => {
                alert('Error creating transaction: ' + error);
            });
        });
    }
});