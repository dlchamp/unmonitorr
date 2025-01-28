document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("config-form");
    const toast = document.getElementById("toast");
    const resetButton = document.getElementById("reset-button");
    const saveButton = document.getElementById("save-button");
    const toastMessage = document.getElementById("toast-message");

    // Function to store original data, ensuring checkboxes are included
    const getFormData = () => {
        const data = new FormData(form);
        form.querySelectorAll("input[type='checkbox']").forEach((checkbox) => {
            data.set(checkbox.name, checkbox.checked ? "on" : "off");
        });
        return data;
    };

    let originalData = getFormData(); // Store the form data including checkboxes

    const showToast = (message, buttons = true) => {
        toastMessage.textContent = message;
        toast.classList.remove("hidden");
        resetButton.style.display = buttons ? "inline-block" : "none";
        saveButton.style.display = buttons ? "inline-block" : "none";
    };

    const hideToast = () => {
        toast.classList.add("hidden");
    };

    // Compare current form state against original
    const hasUnsavedChanges = () => {
        const currentData = getFormData();
        for (let [key, value] of originalData.entries()) {
            if (currentData.get(key) !== value) {
                return true;
            }
        }
        return false;
    };

    // Detect changes on all input fields, including checkboxes
    form.addEventListener("input", () => {
        if (hasUnsavedChanges()) {
            showToast("You have unsaved changes!");
        } else {
            hideToast();
        }
    });

    // Ensure checkboxes trigger the toast when changed
    form.querySelectorAll("input[type='checkbox']").forEach((checkbox) => {
        checkbox.addEventListener("change", () => {
            if (hasUnsavedChanges()) {
                showToast("You have unsaved changes!");
            } else {
                hideToast();
            }
        });
    });

    resetButton.addEventListener("click", () => {
        for (let [key, value] of originalData.entries()) {
            const element = form.elements[key];
            if (element) {
                if (element.type === "checkbox") {
                    element.checked = value === "on"; // Restore checkbox state correctly
                } else {
                    element.value = value;
                }
            }
        }
        hideToast();
    });

    saveButton.addEventListener("click", async () => {
        const formData = getFormData();
        try {
            const response = await fetch("/save-config", {
                method: "POST",
                body: formData,
            });
            if (response.ok) {
                originalData = getFormData(); // Update original data after save
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
