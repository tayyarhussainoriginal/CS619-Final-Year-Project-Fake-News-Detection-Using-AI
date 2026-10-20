document.addEventListener("DOMContentLoaded", function () {

    const goButton = document.querySelector('button[name="index"]');

    if (goButton) {
        goButton.addEventListener("click", function (e) {

            const action = document.querySelector('select[name="action"]');

            if (action && action.value.includes("retrain")) {

                const confirmRun = confirm(
                    "Are you sure you want to retrain the model?\n\nThis may take some time and replace the active model."
                );

                if (!confirmRun) {
                    e.preventDefault();
                }
            }
        });
    }

});