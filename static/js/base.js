// =========================
// LOGOUT BUTTON
// =========================

document.addEventListener("DOMContentLoaded", function(){

    const logoutButton = document.getElementById("logout-button");

    if(logoutButton){

        logoutButton.addEventListener("click", function(e){

            e.preventDefault();

            document.getElementById("logout-form").submit();

        });

    }

});