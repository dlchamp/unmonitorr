
async function testRadarr() {
    const uri = document.getElementById("radarr-uri").value;
    const apiKey = document.getElementById("radarr-api-key").value;
    const resultElement = document.getElementById("radarr-test-result");
    const buttonElement = document.getElementById('radarr-test-button')

    const buttonText = buttonElement.querySelector('.button-text')
    const iconClose = buttonElement.querySelector('.close');
    const iconCheck = buttonElement.querySelector('.check');
    const iconSpinner = buttonElement.querySelector('.testing');

    buttonElement.setAttribute('disabled', true);
    buttonText.style.display = "none"
    iconSpinner.style.display = "inline-block";

    try {
        const response = await fetch(
            '/test-arr', {
            method: 'POST', body: JSON.stringify(
                { 'uri': uri, 'api_key': apiKey, 'client': 'Radarr' }
            )
        }
        );
        iconSpinner.style.display = "none";
        if (response.ok) {
            buttonText.style.display = "none";
            resultElement.textContent = "";
            iconCheck.style.display = "inline-block";
        } else {
            const error = await response.text();
            resultElement.textContent = `${error}`;
            buttonText.style.display = "none";
            iconClose.style.display = "inline-block";
        }
    } catch (err) {
        resultElement.textContent = `${err.message}`;
        buttonText.style.display = "none";
        iconClose.style.display = "inline-block";
    } finally {
        setTimeout(() => {
            buttonText.style.display = "inline-block";
            iconCheck.style.display = "none";
            iconClose.style.display = "none";
            buttonElement.removeAttribute('disabled');

        }, 2000);
    }
}

async function testSonarr() {
    const uri = document.getElementById("sonarr-uri").value;
    const apiKey = document.getElementById("sonarr-api-key").value;
    const resultElement = document.getElementById("sonarr-test-result");
    const buttonElement = document.getElementById('sonarr-test-button')

    const buttonText = buttonElement.querySelector('.button-text')
    const iconClose = buttonElement.querySelector('.close');
    const iconCheck = buttonElement.querySelector('.check');

    const iconSpinner = buttonElement.querySelector('.testing');

    buttonElement.setAttribute('disabled', true);
    buttonText.style.display = "none"
    iconSpinner.style.display = "inline-block";

    try {
        const response = await fetch(
            '/test-arr', {
            method: 'POST', body: JSON.stringify(
                { 'uri': uri, 'api_key': apiKey, 'client': 'Sonarr' }
            )
        }
        );
        iconSpinner.style.display = "none";
        if (response.ok) {
            buttonText.style.display = "none";
            resultElement.textContent = "";
            iconCheck.style.display = "inline-block";
        } else {
            const error = await response.text();
            resultElement.textContent = `${error}`;
            buttonText.style.display = "none";
            iconClose.style.display = "inline-block";
        }
    } catch (err) {
        resultElement.textContent = `${err.message}`;
        buttonText.style.display = "none";
        iconClose.style.display = "inline-block";
    } finally {
        setTimeout(() => {
            buttonText.style.display = "inline-block";
            iconCheck.style.display = "none";
            iconClose.style.display = "none";
            buttonElement.removeAttribute('disabled');
        }, 2000);
    }
}
// Reset button appearance when input fields change
document.querySelectorAll("#radarr-uri, #radarr-api-key, #sonarr-uri, #sonarr-api-key").forEach((input) => {
    input.addEventListener("input", (event) => {
        const testButton = document.getElementById(`test-${event.target.id.split("-")[0]}`);
        const resultElement = document.getElementById(`${event.target.id.split("-")[0]}-test-result`);
        testButton.style.backgroundColor = "#9D4EDD";
        testButton.textContent = "Test";
        resultElement.textContent = "";
    });
});
