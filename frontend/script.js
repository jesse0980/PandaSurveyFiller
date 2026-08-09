const API_URL =
    "https://mxo48732xl.execute-api.us-east-1.amazonaws.com/prod/start";

let surveyUrl = null;

const statusEl = document.getElementById("status");
const surveyUrlEl = document.getElementById("surveyUrl");
const readerEl = document.getElementById("reader");

function onScanSuccess(decodedText) {

    surveyUrl = decodedText;

    surveyUrlEl.textContent = decodedText;

    // statusEl.style.color = "green";
    statusEl.textContent =
        "✓ QR code scanned! Press Submit to continue.";

    html5QrCode.stop().then(() => {
        readerEl.style.display = "none";
    });
}

const html5QrCode = new Html5Qrcode("reader");

// Try to use the rear camera first
html5QrCode.start(
    { facingMode: "environment" },
    {
        fps: 10,
        qrbox: 250
    },
    onScanSuccess
).catch(() => {

    // Fallback to first available camera
    Html5Qrcode.getCameras()
        .then(cameras => {

            if (cameras.length) {

                return html5QrCode.start(
                    cameras[0].id,
                    {
                        fps: 10,
                        qrbox: 250
                    },
                    onScanSuccess
                );

            } else {

                statusEl.textContent =
                    "No cameras found.";

            }

        })
        .catch(err => {

            console.error(err);

            statusEl.textContent =
                "Camera error: " + err;

        });

});

document
    .getElementById("submitBtn")
    .addEventListener("click", async () => {

        const email =
            document.getElementById("email").value.trim();

        if (!email) {
            alert("Please enter an email.");
            return;
        }

        if (!surveyUrl) {
            alert("Please scan a QR code.");
            return;
        }

        statusEl.textContent = "Submitting survey...";

        try {

            const response = await fetch(
                API_URL,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email: email,
                        link: surveyUrl
                    })
                }
            );

            const result = await response.json();

            console.log(result);

            if (response.ok) {

                statusEl.textContent =
                    "✓ Survey submitted successfully! You may now close this page.";
                statusEl.style.color = "green";


            } else {

                statusEl.textContent =
                    "Submission failed.";
                statusEl.style.color = "red";


            }

        } catch (error) {

            console.error(error);

            statusEl.textContent =
                "Network error. Check browser console.";
            statusEl.style.color = "red";


        }

    });