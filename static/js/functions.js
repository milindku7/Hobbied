function signup_serve() {
    window.location.href = "/signup"
}
async function signup_form_submit() {
    const email = document.getElementById("email").value.toLowerCase();
    const password = document.getElementById("password").value;
    const username = document.getElementById("username").value;
    const JSON_message = {
        "email": encodeURIComponent(email),
        "password": encodeURIComponent(password),
        "username": encodeURIComponent(username)
    };

    const URL_curr = window.location.href;
    const concated = URL_curr.concat("/signup_details");
    const res = await fetch(concated,{
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(JSON_message)
    });
    const data = await res.json();
    const message = data.message;
    if (message === "username")
        {
            document.getElementById("error_message").innerHTML = "This username is already taken";
        }
    if (message === "password")
        {
            document.getElementById("error_message").innerHTML = "The password is not strong";
        }
    if (message === "allright")
        {
            window.location.href = "/login";
        }
    if (message === "email")
        {
            document.getElementById("error_message").innerHTML = "This email is not valid";
        }
}
async function login_process() {
    const username = document.getElementById("username").value.toLowerCase();
    const password = document.getElementById("password").value;
    const JSON_message = {
        "username": encodeURIComponent(username),
        "password": encodeURIComponent(password)
    };

    const URL_curr = window.location.href;
    const concated = URL_curr.concat("/login_details");
    const res = await fetch(concated,{
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(JSON_message)
    });
    const data = await res.json();
    const message = data.message;
    if (message === "notright")
        {
            document.getElementById("error_message").innerHTML = "Please check the username and password again";
        }
    if (message === "allright")
        {
            window.location.href = "/";
        }
}
function serve_login_page() {
    window.location.href = "/login";
}
async function make_new_post(){
    const title = document.getElementById("new_post_title");
    const description = document.getElementById("new_post_description");
    const picture = document.getElementById("post_picture");
    const xsrf = document.getElementById("xsrf_token")
    console.log(typeof picture);
    if (title == undefined || title === "" || title === null) {
        document.getElementById("need_title") = "Please provide a title";
    }
    if (description == undefined || description === "" || description === null) {
        document.getElementById("need_desc") = "Please provide a description";
    }
    const JSON_message = {
        "title": title,
        "description": description,
        "picture": picture,
        "XSRF": xsrf
    };
    const URL_curr = window.location.href;
    const concated = URL_curr.concat("/new_post");
    const res = await fetch(concated,{
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(JSON_message)
    });
    const data = await res.json();
    window.location.href = "/";
}