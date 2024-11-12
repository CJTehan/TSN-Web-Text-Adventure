JavaScript:
const messageDiv = document.getElementById('message');
const actionForm = document.getElementById('action-form');
const locationName = document.getElementById('location-name');
const locationDescription = document.getElementById('location-description');
const locationItems = document.getElementById('location-items');
const currentLocationInput = document.getElementById('current-location');
actionForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(actionForm);
    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Update the message div with the response
        messageDiv.textContent = data.message;
        // Update location information
        if(data.name)
        {
            locationName.textContent = data.name;
            locationDescription.value = data.description;
            currentLocationInput.value = data.current_location;
            // Update location items
            locationItems.innerHTML = ''; // Clear previous items
            if (data.items)
            {
                data.items.forEach(element => {
                    const li = document.createElement('li');
                    li.textContent = item;
                    locationItems.appendChild(li);
                });
            }
        }
    })
    .catch(error => {
        console.error('Error', error);
        messageDiv.textContent = 'An error occured.';
    })
})