document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("config-form");
    const toast = document.getElementById("toast");
    const resetButton = document.getElementById("reset-button");
    const saveButton = document.getElementById("save-button");
    const toastMessage = document.getElementById("toast-message");

    let originalData = new FormData(form);

    const showToast = (message, buttons = true) => {
        toastMessage.textContent = message;
        toast.classList.remove("hidden");
        resetButton.style.display = buttons ? "inline-block" : "none";
        saveButton.style.display = buttons ? "inline-block" : "none";
    };

    const hideToast = () => {
        toast.classList.add("hidden");
    };

    const hasUnsavedChanges = () => {
        const currentData = new FormData(form);
        for (let [key, value] of originalData.entries()) {
            if (currentData.get(key) !== value) {
                return true;
            }
        }
        return false;
    };

    form.addEventListener("input", () => {
        if (hasUnsavedChanges()) {
            showToast("You have unsaved changes!");
        } else {
            hideToast();
        }
    });

    resetButton.addEventListener("click", () => {
        for (let [key, value] of originalData.entries()) {
            const element = form.elements[key];
            if (element.type === "checkbox") {
                element.checked = value === "on";
            } else {
                element.value = value;
            }
        }
        hideToast();
    });

    saveButton.addEventListener("click", async () => {
        const formData = new FormData(form);
        try {
            const response = await fetch("/save-config", {
                method: "POST",
                body: formData,
            });
            if (response.ok) {
                originalData = new FormData(form); // Update original data
                showToast("Changes have been saved!", false);
                setTimeout(hideToast, 1000);
            } else {
                showToast("Failed to save changes!", false);
            }
        } catch (error) {
            showToast("An error occurred while saving changes!", false);
        }
    });
});
