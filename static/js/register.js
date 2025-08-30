document.addEventListener("DOMContentLoaded", function () {
    const usernameField = document.querySelector("#id_username");
    const feedbackField = document.querySelector("#username-feedback");
    const submitBtn = document.querySelector("#submitbtn");
    const emailField = document.querySelector("#id_email");
    const emailFeedback = document.querySelector("#email-feedback");
    const passwordField = document.querySelector("#id_password1");
    const password2Field = document.querySelector("#id_password2");
    const password1Feedback = document.querySelector("#password1-feedback");
    const password2Feedback = document.querySelector("#password2-feedback");
    const phoneField = document.querySelector("#id_phone");
    const phoneFeedback = document.querySelector("#phone-feedback");
    const passwordhelp = document.querySelector('#id_password1_helptext');
    passwordhelp.style.display = 'none';
    const div_pass = document.querySelector('#div_id_password1')
    const node = document.createElement('small')
    node.textContent = "Password must be 8+ chars with upper, lower, number, special,number";
    node.classList.add("form-text")
    node.classList.add('text-muted')
    
    div_pass.append(node);

    


    let usernameValid = false;
    let emailValid = false;
    let password1Valid = false;
    let password2Valid = false;
    let phoneValid = false;

    submitBtn.disabled = false;

    function toggleSubmit() {
        submitBtn.disabled = !(usernameValid && emailValid && password1Valid && password2Valid && phoneValid);
        console.log(usernameValid, emailValid, password1Valid, password2Valid, phoneValid,'hai');
        console.log(submitBtn.disabled);

    }

    usernameField.addEventListener("input", function () {
        const username = usernameField.value;

        if (username.length > 0) {
            fetch("/accounts/validateusername/",{
                method: "POST",
                body: new URLSearchParams({ username: username })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.is_taken) {
                        usernameField.style.border = "2px solid red";
                        feedbackField.style.color = "red";
                        feedbackField.textContent = data.error_message;
                        
                        usernameValid = false;
                        toggleSubmit();
                    } else {
                        usernameField.style.border = "2px solid green";
                        feedbackField.style.color = "green";
                        feedbackField.textContent = data.success_message;
                        
                        usernameValid = true;
                        toggleSubmit();
                    }
                    toggleSubmit();
                })
        } else {
            usernameField.style.border = "";
            feedbackField.textContent = "";
            toggleSubmit();
        }
    });

    emailField.addEventListener("keyup", function () {
        const email = emailField.value.trim();
        console.log(email);
        if (email.length > 0) {
            fetch("/accounts/validateemail/", {
                method: "POST",
                body: new URLSearchParams({ email: email})
            })
            .then(res => res.json())
            .then(data => {
                if (data.is_taken) {
                    emailField.style.border = "2px solid red";
                    emailFeedback.style.color = "red";
                    emailFeedback.textContent = data.error_message;
                    console.log(data);
                    emailValid = false;
                }
                else if (data.invalid_format) {
                    emailField.style.border = "2px solid red";
                    emailFeedback.style.color = "red";
                    emailFeedback.textContent = data.error_message;
                    console.log(data);
                    emailValid = false;
                }
                else {
                    emailField.style.border = "2px solid green";
                    emailFeedback.style.color = "green";
                    emailFeedback.textContent = data.success_message;
                    console.log(data);
                    emailValid = true;
                }
                toggleSubmit();
            })
        } else {
            emailField.style.border = "";
            emailFeedback.textContent = "";
            emailValid = false;
            toggleSubmit();
        }
    });

    passwordField.addEventListener("keyup", function () {
        const password1 = passwordField.value; 
        const password2Val = password2Field.value; 
        if (password1.length > 0) {
            fetch("/accounts/validatepassword/", {
                method: "POST",
                body: new URLSearchParams({ password1: password1 })
            }).then(res => res.json())
            .then(data => { 
                if (data.is_valid) {
                    passwordField.style.border = "2px solid green";
                    password1Feedback.style.color = "green";
                    password1Feedback.textContent = data.success_message;
                    password1Valid = true;
                    toggleSubmit();
                } else {
                    if (password2Val.length > 0 ) {
                        passwordField.style.border = "2px solid red";
                        password1Feedback.style.color = "red";
                    }
                    passwordField.style.border = "2px solid red";
                    password1Feedback.style.color = "red";
                    password1Feedback.textContent = data.error_message; 
                    password1Valid = false;
                    toggleSubmit();

                }
            })
        } else {
            passwordField.style.border = "";
            password1Feedback.textContent = "";
            passwordField.style.border = "2px solid ";
            toggleSubmit();
        }


    }); 


    password2Field.addEventListener("keyup", function () {
        const password2 = password2Field.value;  
        const password1 = passwordField.value;
        if (password2.length > 0) {
            fetch("/accounts/validatepassword2/", {
                method: "POST",
                body: new URLSearchParams({ password1:password1,
                    password2: password2 })
            }).then(res => res.json())
            .then(data => { 
                if (password1Valid==false) {
                    password2Field.style.border = "2px solid red";
                    password2Feedback.style.color = "red";
                    password2Valid = false;
                    toggleSubmit();

                }
                else if (data.is_valid) {
                    password2Field.style.border = "2px solid green";
                    password2Feedback.style.color = "green";
                    password2Feedback.textContent = data.success_message;
                    password2Valid = true;
                    toggleSubmit();
                
                } else {
                    password2Field.style.border = "2px solid red";
                    password2Feedback.style.color = "red";
                    password2Feedback.textContent = data.error_message; 
                    password2Valid = false;
                    toggleSubmit();

                }
            })
        } else {
            password2Field.style.border = "";
            password2Feedback.textContent = "";
            toggleSubmit();
        }


    }); 

    phoneField.addEventListener("input", function () {
        const phone = phoneField.value;  
        if (phone.length > 0) {
            fetch("/accounts/validatephone/", {
                method: "POST",
                body: new URLSearchParams({ phone: phone })
            }).then(res => res.json())
            .then(data => { 
                if (data.is_taken || data.invalid_format) {
                    phoneField.style.border = "2px solid red";
                    phoneFeedback.style.color = "red";
                    phoneFeedback.textContent = data.error_message;
                    phoneValid = false;
                    toggleSubmit();
                } else {
                    phoneField.style.border = "2px solid green";
                    phoneFeedback.style.color = "green";
                    phoneFeedback.textContent = 'valid'; 
                    phoneValid = true;
                    toggleSubmit();

                }
            })
        } else {
            phoneField.style.border = "";
            phoneFeedback.textContent = "";
            toggleSubmit();
            p
        }


    }); 















});