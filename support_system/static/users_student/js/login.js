$(document).ready(function(){

    $('#submit').on('click', function(){

        var email = document.getElementById("email").value;
        var password = document.getElementById("pwd").value;

        if( email.length != 0 && password.length != 0){

            var but = document.getElementById('submit');
            but.type = "submit";
            document.getElementById('form').submit();
        }
        else{

            alert("All fields are required");

        }

    }
    )


})