document.addEventListener('DOMContentLoaded', function () {

    console.log("Made it")

    correct();
});

function correct() {

    var toastLiveExample = document.querySelectorAll('#my-toast');
    for (var x = 0; x < toastLiveExample.length; x++) {
        new bootstrap.Toast(toastLiveExample[x]).show();
    }
}
