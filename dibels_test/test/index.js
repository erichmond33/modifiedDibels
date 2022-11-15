document.addEventListener('DOMContentLoaded', function () {




    reponsiveElements()
    activateToasts()
});



/* --- #testArea Window Size --- */
function reponsiveElements() {
    // init
    if (window.innerWidth < 1200) {

        document.querySelector("#testArea").style.width = `${window.innerWidth}px`;
        document.querySelector("#testArea").style.height = `${window.innerHeight}px`;

        document.querySelector("#offcanvasExample").style.visibility = "visible";

        document.querySelector("#navButton").style.display = "block";
        document.querySelector("#navClose").style.display = "block";
    }
    else {

        document.querySelector("#testArea").style.width = `${window.innerWidth - 280}px`;
        document.querySelector("#testArea").style.height = `${window.innerHeight}px`;

        document.querySelector("#offcanvasExample").classList.toggle("show");
        document.querySelector("#offcanvasExample").style.visibility = "visible";

        document.querySelector("#navButton").style.display = "none";
        document.querySelector("#navClose").style.display = "none";

    }
    // constant
    window.addEventListener('resize', () => {

        if (window.innerWidth < 1200) {

            if (document.querySelector("#offcanvasExample").classList.contains("show") == true) {
                document.querySelector("#offcanvasExample").classList.toggle("show");
            };

            document.querySelector("#testArea").style.width = `${window.innerWidth}px`;
            document.querySelector("#testArea").style.height = `${window.innerHeight}px`;

            document.querySelector("#navButton").style.display = "block";
            document.querySelector("#navClose").style.display = "block";

        }
        else {

            if (document.querySelector("#offcanvasExample").classList.contains("show") == false) {
                document.querySelector("#offcanvasExample").classList.toggle("show");
            };

            document.querySelector("#testArea").style.width = `${window.innerWidth - 280}px`;
            document.querySelector("#testArea").style.height = `${window.innerHeight}px`;

            document.querySelector("#navButton").style.display = "none";
            document.querySelector("#navClose").style.display = "none";

        }
    });
    // Buttons Listener
    document.querySelector("#navButton").addEventListener('click', () => {
        document.querySelector("#offcanvasExample").classList.toggle("show");
    });
    document.querySelector("#navClose").addEventListener('click', () => {
        document.querySelector("#offcanvasExample").classList.toggle("show");
    });
}

function activateToasts() {

    var toastLiveExample = document.querySelectorAll('#my-toast');
    for (var x = 0; x < toastLiveExample.length; x++) {
        new bootstrap.Toast(toastLiveExample[x]).show();
    }
}