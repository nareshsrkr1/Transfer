validatePeriodOfStay: function (executionContext) {
    try {
        var formContext = executionContext.getFormContext();
        var periodOfStay = formContext.getAttribute("bupa_periodofstaydays");
        var periodControl = formContext.getControl("bupa_periodofstaydays");
        var hmDecision = formContext.getAttribute("bupa_hmdecision");

        var periodValue = periodOfStay ? periodOfStay.getValue() : null;
        var isWritable = periodControl && !periodControl.getDisabled();

        // Check and show error if value is out of range
        if (periodValue > 31) {
            formContext.ui.setFormNotification("Please enter a value between 1 to 30", "ERROR", "bupa_periodofstaydays");

            if (isWritable) {
                periodOfStay.setValue(null);  // Avoid system read-only error
            }

            periodControl.setFocus();
        } else {
            formContext.ui.clearFormNotification("bupa_periodofstaydays");
        }

        // Independent logic for HM Decision
        if (hmDecision && hmDecision.getValue() !== 100000000) {
            formContext.ui.clearFormNotification("bupa_periodofstaydays");
        }

    } catch (err) {
        console.log("Error: " + err.message);
    }
}
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
    

















validatePeriodOfStay: function (executionContext) {
    try {
        var formContext = executionContext.getFormContext();
        var periodOfStay = formContext.getAttribute("bupa_periodofstaydays");
        var periodControl = formContext.getControl("bupa_periodofstaydays");
        var hmDecision = formContext.getAttribute("bupa_hmdecision");

        var periodValue = periodOfStay ? periodOfStay.getValue() : null;
        var isWritable = periodControl && !periodControl.getDisabled();

        // Check and show error if value is out of range
        if (periodValue > 31) {
            formContext.ui.setFormNotification("Please enter a value between 1 to 30", "ERROR", "bupa_periodofstaydays");

            if (isWritable) {
                periodOfStay.setValue(null);  // Avoid system read-only error
            }

            periodControl.setFocus();
        } else {
            formContext.ui.clearFormNotification("bupa_periodofstaydays");
        }

        // Independent logic for HM Decision
        if (hmDecision && hmDecision.getValue() !== 100000000) {
            formContext.ui.clearFormNotification("bupa_periodofstaydays");
        }

    } catch (err) {
        console.log("Error: " + err.message);
    }
}
