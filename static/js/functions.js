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
            document.getElementById("error_message").innerHTML = "This username is already taken or is more than 20 characters";
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
function make_new_post(){
    document.getElementById("new_post_form").style.display = "none";
}
function new_post_form_close() {
    window.location.href = "/";
  }

function toggleColor(button_id) {
    const button = document.getElementById(button_id);

    if (document.getElementById("tags_pressed").value !== "") {
        let split_string = document.getElementById("tags_pressed").value.split(",");
        let split_string2 = [];

        for (let i of split_string) {
            if (i === button_id) {
                button.style.backgroundColor = '#272a3b';
                button.style.color = 'white';
                for (let k of split_string) {
                    if (k !== button_id) {
                        split_string2.push(k);
                    }
                }
                let final_str = "";
                for (let acc of split_string2) {
                    if (final_str === "") {
                        final_str = acc;
                    }
                    else {
                        final_str = final_str.concat(",");
                        final_str = final_str.concat(acc);
                    }
                }
                document.getElementById("tags_pressed").value = final_str;
                return;
            }
        }

    }

    if (document.getElementById("tags_pressed").value === "") {
        document.getElementById("tags_pressed").value += button_id;
    }
    else {
        let t = ","
        document.getElementById("tags_pressed").value += t.concat(button_id);
    }
    console.log(document.getElementById("tags_pressed").value)
    button.style.backgroundColor = 'red';
    button.style.color = 'white';
}
function custom_tag() {
    
}