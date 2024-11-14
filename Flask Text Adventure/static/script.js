document.addEventListener("DOMContentLoaded", () => {
    console.log("script.js is loaded and running.");
    const actionForm = document.getElementById('action-form');
    const messageDiv = document.getElementById('message');
    const locationName = document.getElementById('location-name');
    const locationDescription = document.getElementById('location-description');
    const locationItems = document.getElementById('location-items');
    function updateDirectionButtons(directions) {
        const buttons = {
            'Go North': document.querySelector('[data-action="Go North"]'),
            'Go South': document.querySelector('[data-action="Go South"]'),
            'Go East': document.querySelector('[data-action="Go East"]'),
            'Go West': document.querySelector('[data-action="Go West"]')
        };
        for (const [action, button] of Object.entries(buttons)) {
            const direction = action.split(" ")[1].toLowerCase();
            button.disabled = !directions[direction];
        }
    }
    if (actionForm) {
        actionForm.addEventListener('click', (event) => {
            if (event.target.tagName === 'BUTTON') {
                const action = event.target.getAttribute('data-action');
                console.log(`Button clicked: ${action}`);
                // Check if action is "Get" and retrieve the item name
                const data = { action };
                if (action === "get") {
                    const item = prompt("Enter the item you want to pick up:");
                    if (item) {
                        data.item = item;  // Add item to data for 'get' action
                    }
                }
                fetch('/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Response data:', data);
                    messageDiv.textContent = data.message || '';
                    if (data.current_location) {
                        locationName.textContent = data.name;
                        locationDescription.textContent = data.description;
                        locationItems.innerHTML = '';
                        if (data.items && data.items.length > 0) {
                            data.items.forEach(item => {
                                const li = document.createElement('li');
                                li.textContent = item;
                                locationItems.appendChild(li);
                            });
                        } else {
                            locationItems.innerHTML = '<li>No items here</li>';
                        }
                        updateDirectionButtons(data.directions);
                    }
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                })
                .catch(error => {
                    console.error('Error in fetch response:', error);
                    messageDiv.textContent = 'An error occurred while processing the action.';
                });
            }
        });
    } else {
        console.error("actionForm element not found, try again.");
    }
});