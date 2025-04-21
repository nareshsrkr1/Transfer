updateFieldVisibilityAndAccessibility: function (executionContext) {
    try {
        var formContext = executionContext.getFormContext();
        var eventArgs = executionContext.getEventArgs();
        var isSaveEvent = eventArgs && typeof eventArgs.getSaveMode === "function";

        var statusPAA2 = formContext.getAttribute("statuscode").getValue();
        var hmDecision = formContext.getAttribute("bupa_hmdecision").getValue();

        if (statusPAA2 == 100000004 && hmDecision == null) {
            var careHomeLookup = formContext.getAttribute("bupa_bupacarehome").getValue();

            if (careHomeLookup && careHomeLookup.length > 0) {
                var careHomeID = careHomeLookup[0].id.replace("{", "").replace("}", "");
                if (careHomeID != null) {
                    Xrm.WebApi.retrieveRecord("bupa_bupacarehome", careHomeID, "?$select=bupa_homecategory")
                        .then(function success(result) {
                            var category = result.bupa_homecategory;
                            if (category != null) {
                                if (category == 100000000) {
                                    var controlsToShow = [
                                        "bupa_carehomeunit", "bupa_roomnumber", "bupa_typeoffunding", "bupa_agreedfee",
                                        "bupa_residentcontribution", "bupa_fundednursingcarefnc", "bupa_thirdpartycontribution",
                                        "bupa_localauthoritycontribution", "bupa_continuinghealthcare", "bupa_initialmonthfee",
                                        "bupa_admissionanalysis", "bupa_caretype", "bupa_proposedadmissiondate",
                                        "bupa_whoissigningthecontract", "bupa_willthefeebepaidbydirectdebit", "bupa_whoissigningdd"
                                    ];
                                    controlsToShow.forEach(function (fieldName) {
                                        formContext.getControl(fieldName).setVisible(true);
                                        formContext.getAttribute(fieldName).setRequiredLevel("none");
                                    });
                                } else if (category == 100000001) {
                                    var controlsToShow = [
                                        "bupa_typeoffunding", "bupa_agreedfee", "bupa_residentcontribution",
                                        "bupa_fundednursingcarefnc", "bupa_thirdpartycontribution", "bupa_localauthoritycontribution",
                                        "bupa_continuinghealthcare", "bupa_initialmonthfee", "bupa_admissionanalysis",
                                        "bupa_caretype", "bupa_proposedadmissiondate", "bupa_whoissigningthecontract",
                                        "bupa_willthefeebepaidbydirectdebit", "bupa_whoissigningdd"
                                    ];
                                    controlsToShow.forEach(function (fieldName) {
                                        formContext.getControl(fieldName).setVisible(true);
                                        formContext.getAttribute(fieldName).setRequiredLevel("none");
                                    });
                                }
                            }

                            // Show confirm dialog only on save
                            if (isSaveEvent) {
                                var confirmStrings = {
                                    title: "Unsaved Changes",
                                    text: "Do you want to save changes before refreshing?"
                                };

                                var confirmOptions = {
                                    height: 200,
                                    width: 450
                                };

                                Xrm.Navigation.confirmDialog(confirmStrings, confirmOptions)
                                    .then(function (success) {
                                        if (success.confirmed) {
                                            formContext.data.save().then(function () {
                                                formContext.data.refresh(false); // Refresh after save
                                            });
                                        } else {
                                            formContext.data.refresh(true); // Discard and refresh
                                        }
                                    });
                            }

                        })
                        .catch(function (error) {
                            console.error("Home Category fetch error: " + error.message);
                        });
                }
            }
        }

    } catch (err) {
        console.log("Error: " + err.message);
    }
}
