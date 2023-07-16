// Executed after the entire web page is loaded
$(function () {
    bindEmailCaptchaClick();
});

function bindEmailCaptchaClick() {
    // '$' represents jQuery
    $("#captcha-btn").click(function (event) {
        // $this：Represents the jquery object of the current button
        const $this = $(this);
        // Prevent default events, such as submitting all form data to the server
        event.preventDefault();

        const email = $("input[name='email']").val();   // can be obtained by id as well
        $.ajax({
            // address: http://127.0.0.1:5000
            // for example: /auth/captcha/email?email=xx@mail.com
            url: "/auth/captcha/email?email=" + email,
            method: "GET",
            // result: the response from the backend, is JSON object in this case
            success: function (result) {
                const code = result['code'];
                if (code == 200) {
                    let countdown = 5;
                    // Before the countdown starts, cancel the click event of the button
                    $this.off("click");
                    const timer = setInterval(function () {
                        $this.text(countdown);
                        countdown -= 1;
                        // Executed when the countdown ends
                        if (countdown <= 0) {
                            // clear timer
                            clearInterval(timer);
                            // Change the text of the button back
                            $this.text("Get Verification Code");
                            // Rebind the click event
                            bindEmailCaptchaClick();
                        }
                    }, 1000);
                    // alert("Email verification code sent successfully！");
                } else {
                    alert(result['message']);
                }
            },
            fail: function (error) {
                console.log(error);
            }
        })
    });
}


