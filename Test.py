function validatePeriodOfStayDays(executionContext) {
    var formContext = executionContext.getFormContext();
    var periodOfStayField = formContext.getAttribute("bupa_periodofstaydays");
    var periodValue = periodOfStayField.getValue();

    // Clear any existing notification first
    formContext.ui.clearFormNotification("validation_period");

    // Validate the value
    if (periodValue > 31) {
        var control = formContext.getControl("bupa_periodofstaydays");

        // Only set value and focus if field is visible and not disabled (i.e., not read-only)
        if (control && control.getVisible() && !periodOfStayField.getDisabled()) {
            periodOfStayField.setValue(null);
            control.setFocus();
        }

        formContext.ui.setFormNotification("Please enter a value between 1 to 30", "ERROR", "validation_period");
    }
            }
