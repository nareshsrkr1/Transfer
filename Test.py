var isConfirmedSave = false;

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

                // All your retrieve logic and UI control handling stays unchanged...

                // DIRTY CHECK + DIALOG LOGIC
                if (isSaveEvent && formContext.data.entity.getIsDirty() && !isConfirmedSave) {
                    eventArgs.preventDefault(); // Prevent the current save

                    var confirmStrings = {
                        title: "Unsaved Changes",
                        text: "Do you want to save changes before refreshing?",
                        confirmButtonLabel: "Save",
                        cancelButtonLabel: "Discard"
                    };

                    var confirmOptions = {
                        height: 200,
                        width: 450
                    };

                    Xrm.Navigation.openConfirmDialog(confirmStrings, confirmOptions).then(function (result) {
                        if (result.confirmed) {
                            isConfirmedSave = true;
                            formContext.data.save().then(function () {
                                // Use setTimeout to avoid re-entering the save event
                                setTimeout(function () {
                                    formContext.data.refresh(false); // false to avoid default confirmation popup
                                }, 1000);
                            });
                        } else {
                            isConfirmedSave = false;
                            setTimeout(function () {
                                formContext.data.refresh(false); // prevent Dynamics confirmation
                            }, 500);
                        }
                    });

                    return;
                }

                // Reset flag after successful save
                if (isConfirmedSave) {
                    isConfirmedSave = false;
                }
            }
        }
    } catch (err) {
        console.log("Error: " + err.message);
    }
}











var isConfirmedSave = false;

updateFieldVisibilityAndAccessibility:  function (executionContext) {
           debugger;
            try {
                var formContext = executionContext.getFormContext();
                var  eventArgs = executionContext.getEventArgs();
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
                                            formContext.getControl("bupa_carehomeunit").setVisible(true);
                                            formContext.getAttribute("bupa_carehomeunit").setRequiredLevel("none");
                                            formContext.getControl("bupa_roomnumber").setVisible(true);
                                            formContext.getAttribute("bupa_roomnumber").setRequiredLevel("none");
                                            formContext.getControl("bupa_typeoffunding").setVisible(true);
                                            formContext.getAttribute("bupa_typeoffunding").setRequiredLevel("none");
                                            formContext.getControl("bupa_agreedfee").setVisible(true);
                                            formContext.getAttribute("bupa_agreedfee").setRequiredLevel("none");
                                            formContext.getControl("bupa_residentcontribution").setVisible(true);
                                            formContext.getAttribute("bupa_residentcontribution").setRequiredLevel("none");
                                            formContext.getControl("bupa_fundednursingcarefnc").setVisible(true);
                                            formContext.getAttribute("bupa_fundednursingcarefnc").setRequiredLevel("none");
                                            formContext.getControl("bupa_thirdpartycontribution").setVisible(true);
                                            formContext.getAttribute("bupa_thirdpartycontribution").setRequiredLevel("none");
                                            formContext.getControl("bupa_localauthoritycontribution").setVisible(true);
                                            formContext.getAttribute("bupa_localauthoritycontribution").setRequiredLevel("none");
                                            formContext.getControl("bupa_continuinghealthcare").setVisible(true);
                                            formContext.getAttribute("bupa_continuinghealthcare").setRequiredLevel("none");
                                            formContext.getControl("bupa_initialmonthfee").setVisible(true);
                                            formContext.getAttribute("bupa_initialmonthfee").setRequiredLevel("none");
                                            formContext.getControl("bupa_admissionanalysis").setVisible(true);
                                            formContext.getAttribute("bupa_admissionanalysis").setRequiredLevel("none");
                                            formContext.getControl("bupa_caretype").setVisible(true);
                                            formContext.getAttribute("bupa_caretype").setRequiredLevel("none");
                                            formContext.getControl("bupa_proposedadmissiondate").setVisible(true);
                                            formContext.getAttribute("bupa_proposedadmissiondate").setRequiredLevel("none");
                                            formContext.getControl("bupa_whoissigningthecontract").setVisible(true);
                                            formContext.getAttribute("bupa_whoissigningthecontract").setRequiredLevel("none");
                                            formContext.getControl("bupa_willthefeebepaidbydirectdebit").setVisible(true);
                                            formContext.getAttribute("bupa_willthefeebepaidbydirectdebit").setRequiredLevel("none");
                                             formContext.getControl("bupa_whoissigningdd").setVisible(true);
                                            formContext.getAttribute("bupa_whoissigningdd").setRequiredLevel("none");
                                          
                                          
                                        }
                                        else if (category == 100000001) {
                                            formContext.getControl("bupa_typeoffunding").setVisible(true);
                                            formContext.getAttribute("bupa_typeoffunding").setRequiredLevel("none");
                                            formContext.getControl("bupa_agreedfee").setVisible(true);
                                            formContext.getAttribute("bupa_agreedfee").setRequiredLevel("none");
                                            formContext.getControl("bupa_residentcontribution").setVisible(true);
                                            formContext.getAttribute("bupa_residentcontribution").setRequiredLevel("none");
                                            formContext.getControl("bupa_fundednursingcarefnc").setVisible(true);
                                            formContext.getAttribute("bupa_fundednursingcarefnc").setRequiredLevel("none");
                                            formContext.getControl("bupa_thirdpartycontribution").setVisible(true);
                                            formContext.getAttribute("bupa_thirdpartycontribution").setRequiredLevel("none");
                                            formContext.getControl("bupa_localauthoritycontribution").setVisible(true);
                                            formContext.getAttribute("bupa_localauthoritycontribution").setRequiredLevel("none");
                                            formContext.getControl("bupa_continuinghealthcare").setVisible(true);
                                            formContext.getAttribute("bupa_continuinghealthcare").setRequiredLevel("none");
                                            formContext.getControl("bupa_initialmonthfee").setVisible(true);
                                            formContext.getAttribute("bupa_initialmonthfee").setRequiredLevel("none");
                                            formContext.getControl("bupa_admissionanalysis").setVisible(true);
                                            formContext.getAttribute("bupa_admissionanalysis").setRequiredLevel("none");
                                            formContext.getControl("bupa_caretype").setVisible(true);
                                            formContext.getAttribute("bupa_caretype").setRequiredLevel("none");
                                            formContext.getControl("bupa_proposedadmissiondate").setVisible(true);
                                            formContext.getAttribute("bupa_proposedadmissiondate").setRequiredLevel("none");
                                            formContext.getControl("bupa_whoissigningthecontract").setVisible(true);
                                            formContext.getAttribute("bupa_whoissigningthecontract").setRequiredLevel("none");
                                            formContext.getControl("bupa_willthefeebepaidbydirectdebit").setVisible(true);
                                            formContext.getAttribute("bupa_willthefeebepaidbydirectdebit").setRequiredLevel("none");
                                              formContext.getControl("bupa_whoissigningdd").setVisible(true);
                                            formContext.getAttribute("bupa_whoissigningdd").setRequiredLevel("none");
                                        }
                                    }
                                    else
                                        console.error("Could not fetch home category: " + error.message);



                                })
                                .catch(function error(error) {
                                    console.error("Home Category is not filled for this care home: " + error.message);
                                });
                        }
 
if (isSaveEvent && formContext.data.entity.getIsDirty()) {
            var confirmStrings = {
                title: "Unsaved Changes",
                text: "Do you want to save changes before refreshing?"
            };

            var confirmOptions = {
                height: 200,
                width: 450
            };
            if (!isConfirmedSave) {
                eventArgs.preventDefault(); // Stop the initial save

                 Xrm.Navigation.openConfirmDialog({confirmStrings,confirmOptions
                    
                }).then(function (result) {
                    if (result.confirmed) {
                        isConfirmedSave = true;
                        formContext.data.save().then(function () {
                            formContext.data.refresh();
                        });
                    } else {
                        isConfirmedSave = false;
                        formContext.data.refresh();
                    }
                });

                return;
            } else {
                isConfirmedSave = false;
            }
        }
                                  

     }
                }
            } catch (err) {
                console.log("Error" + err.message);
            }
        }
