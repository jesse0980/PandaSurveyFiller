let surveyUrl = null;

const statusEl = document.getElementById("status");
const surveyUrlEl = document.getElementById("surveyUrl");

function onScanSuccess(decodedText) {
    surveyUrl = decodedText;

    surveyUrlEl.textContent = decodedText;

    statusEl.textContent = "QR code scanned successfully.";

    html5QrCode.stop();
}

const html5QrCode = new Html5Qrcode("reader");

Html5Qrcode.getCameras()
    .then(cameras => {
        if (cameras.length) {
            html5QrCode.start(
                cameras[0].id,
                {
                    fps: 10,
                    qrbox: 250
                },
                onScanSuccess
            );
        }
    })
    .catch(err => {
        statusEl.textContent = err;
    });

document
    .getElementById("submitBtn")
    .addEventListener("click", async () => {

        const email =
            document.getElementById("email").value;

        if (!email) {
            alert("Please enter an email.");
            return;
        }

        if (!surveyUrl) {
            alert("Please scan a QR code.");
            return;
        }

        statusEl.textContent = "Submitting...";

        try {

            const response = await fetch(
                "YOUR_LAMBDA_FUNCTION_URL",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email,
                        survey_url: surveyUrl
                    })
                }
            );

            const result = await response.json();

            statusEl.textContent =
                "Survey submitted successfully.";

            console.log(result);

        } catch (error) {

            console.error(error);

            statusEl.textContent =
                "Failed to submit survey.";
        }
    });