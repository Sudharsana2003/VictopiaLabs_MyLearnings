// js_client/client.js

// 1. Define the API endpoint base
const BASE_ENDPOINT = "http://localhost:8000/api";

// 2. Get the form element by its ID
const loginForm = document.getElementById('login-form');

// 3. Define the function to handle the login event
const handleLogin = (event) => {
    // PREVENT the default form submission (which caused the 501 error)
    event.preventDefault(); 
    
    // Convert the form element into a FormData object
    let loginFormData = new FormData(loginForm);
    
    // Convert FormData into a simple JavaScript object (key-value pairs)
    let loginObjectData = Object.fromEntries(loginFormData.entries());
    
    // Convert the JS object into a JSON string for the request body
    let bodyString = JSON.stringify(loginObjectData);

    console.log("Attempting POST with data:", loginObjectData);
    
    // --- Fetch Request Setup ---
    const url = `${BASE_ENDPOINT}/token/`;
    
    const options = {
        method: 'POST',
        headers: {
            // Tell the API we are sending JSON data
            'Content-Type': 'application/json' 
        },
        body: bodyString // The serialized JSON string
    };

    // Execute the fetch request (sends the login data)
    fetch(url, options)
        .then(response => {
            // Check the response status/content (This line returns the promise for JSON data)
            // console.log("Response:", response); 
            return response.json();
        })
        .then(data => {
            // Handle the JSON data (e.g., the access and refresh tokens)
            console.log("Success (JSON Data):", data); 
        })
        .catch(error => {
            // This is where the CORS error will appear initially!
            console.error("Fetch Error:", error);
        });

}

// 4. Attach the event listener if the form exists
if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
}