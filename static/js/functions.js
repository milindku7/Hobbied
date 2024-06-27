function signup_serve() {
    window.location.href = "/signup"
}
async function signup_form_submit() {
    const email = document.getElementById("email").value.toLowerCase();
    const password = document.getElementById("password").value;

    const JSON_message = {
        "email": email,
        "password": password
    };

    const URL_curr = window.location.href;
    const concated = URL_curr.concat("/signup_details");
    console.log(concated)
    const res = await fetch(concated,{
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(JSON_message)
    });
    console.log(res)
    const data = await res.json();
    const message = data.message;
    console.log(message)
    if (message === "Username")
        {
            document.getElementById("error_message").innerHTML += "This username is already taken";
        }
    if (message === "Password")
        {
            document.getElementById("error_message").innerHTML += "The password is not strong";
        }
    if (message === "Allright")
        {
            windows.location.href = "/login";
        }
    if (message === "email")
        {
            document.getElementById("error_message").innerHTML += "This email is not valid";
        }
    
    // request.open("POST","/signup_details");
    // request.setRequestHeader("Content-Type","application/json");
    // request.send(JSON.stringify(JSON_message));
}

