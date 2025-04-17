function customRefreshWithPrompt(formContext) {
    Xrm.Navigation.confirmDialog(
        "Do you want to save changes before refreshing?",
        {
            confirmButtonLabel: "Save",
            cancelButtonLabel: "Discard"
        }
    ).then(function (success) {
        if (success.confirmed) {
            // User clicked "Save"
            formContext.data.save().then(function () {
                formContext.data.refresh(false); // Refresh after save
            });
        } else {
            // User clicked "Discard"
            formContext.data.refresh(true); // Force refresh and discard changes
        }
    });
}
