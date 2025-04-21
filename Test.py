Test.py

if (eventArgs && typeof eventArgs.getSaveMode === "function") {
        var saveMode = eventArgs.getSaveMode();

        // Trigger refresh only after actual save (Save, Save & Close, Save & New)
        if (saveMode === 1 || saveMode === 59 || saveMode === 70) {
            setTimeout(function () {
                formContext.data.refresh(true); // Refresh after save, no popup
            }, 100); // Optional delay to ensure save completes
        }
    }



function handleFormEvents(executionContext) {
    var formContext = executionContext.getFormContext();
    var eventArgs = executionContext.getEventArgs();

    // -------------------------------
    // OnSave Event: Refresh after save
    // -------------------------------
    if (eventArgs && eventArgs.getSaveMode) {
        var saveMode = eventArgs.getSaveMode();
        
        if (saveMode === 1 || saveMode === 59 || saveMode === 70) {  // Save, Save and Close, etc.
            setTimeout(function () {
                formContext.data.refresh(false); // Refresh after save
            }, 1000); // Adjust delay as needed
        }
    }

    // -------------------------------
    // OnLoad Event: No refresh needed
    // -------------------------------
    if (eventArgs && eventArgs.getEventName && eventArgs.getEventName() === "onload") {
        return;
    }

    // -------------------------------
    // OnChange Event: No refresh needed for change events
    // -------------------------------
    if (eventArgs && eventArgs.getEventName && eventArgs.getEventName() === "onchange") {
        return;
    }

    // -------------------------------
    // Handle Discard (manually trigger refresh)
    // -------------------------------
    if (formContext.data.entity.getIsDirty()) {
        // If the form is dirty (has unsaved changes)
        // Force a refresh to discard changes
        setTimeout(function () {
            formContext.data.refresh(true); // Force refresh and discard changes
        }, 1000);  // Delay the refresh slightly to allow Dynamics internal state to settle
    }
}




if (typeof (SDK) == "undefined") { SDK = { __namespace: true } }
if (typeof (SDK.Bupa) == "undefined") { SDK.Bupa = { __namespace: true } }
if (typeof (SDK.Bupa.Sales) == "undefined") { SDK.Bupa.Sales = { __namespace: true } }
if (typeofs.RDT) == "undefined") { SDK.Bupa.Sales.RDT = { __namespace: true } }
if (typeof (SDK.Bupa.Sales.RDT.PAA2) == "undefined") { SDK.Bupa.Sales.RDT.PAA2 = { __namespace: true } }
if (typeof (SDK.Bupa.Sales.RDT.PAA2.Form) == "undefined") {
    SDK.Bupa.Sales.RDT.PAA2.Form = {

        PopulateRateCardFee: async function (executionContext) {

            var formContext = executionContext.getFormContext();
            var banding = formContext.getAttribute('bupa_banding19').getValue();
            var fundingType = formContext.getAttribute('bupa_typeoffunding').getValue();
            var careHomeId = formContext.getAttribute('bupa_bupacarehome').getValue()[0].id;
            var RDTTrained = await Xrm.WebApi.retrieveRecord('bupa_bupacarehome', careHomeId, '?$select=bupa_rdttrained').then(
                function success(result) {
                    return result.bupa_rdttrained;
                },
                function (error) {
                    console.log(error.message);
                }
            );
            var proposedFee = formContext.getAttribute('bupa_proposedfee').getValue();
            if (fundingType == 100000000 || fundingType == 100000005) {
                var careCategory = formContext.getAttribute('bupa_carecategory').getValue();
                var rateCardFundingType = 100000000
                if (careCategory == 100000000) {
                    rateCardFundingType = 100000001
                };
                var room = formContext.getAttribute('bupa_roomnumber').getValue();
                var unit = formContext.getAttribute('bupa_carehomeunit').getValue();
                var rateCardFee=formContext.getAttribute('bupa_ratecardfee').getValue();
                if (unit !== null && unit !== undefined && room !== null && room !== undefined) {
                    var unitId = unit[0].id;
                    var roomId = room[0].id;
                    var careNeed = formContext.getAttribute('bupa_careneed').getValue();
                    var careType = await Xrm.WebApi.retrieveRecord('bupa_carehomeresidents', unitId, '?$select=bupa_caretype').then(
                        function success(result) {
                            return result.bupa_caretype;
                        },
                        function (error) {
                            console.log(error.message);
                        }
                    );
                    var isResidential;
                    if (careType.includes(100000000) || careType.includes(100000008)) {
                        isResidential = true
                    }
                    else {
                        isResidential = false
                    };
                    var isNursing;
                    if (careType.includes(100000001) || careType.includes(100000002) || careType.includes(100000003) || careType.includes(100000004) || careType.includes(100000005) || careType.includes(100000006) || careType.includes(100000007)) {
                        isNursing = true
                    }
                    else {
                        isNursing = false
                    };
                    var careMatch;
                    if ((careNeed == 100000000 && isResidential == true) || (careNeed == 100000001 && isNursing == true)) {
                        careMatch = true
                    }
                    else {
                        careMatch = false
                    }
                    if (RDTTrained == true && proposedFee == null && careMatch == true) {
                        formContext.getControl("bupa_ratecardfee").setVisible(true);
                        var roomType = await Xrm.WebApi.retrieveRecord('bupa_carehomeresident', roomId, '?$select=bupa_category').then(
                            function success(result) {
                                return result.bupa_category;
                            },
                            function (error) {
                                console.log(error.message);
                            }
                        );
                        var roomName = "";
                        switch (roomType) {
                            case 100000000:
                                roomName = "bupa_deluxe";
                                break;
                            case 100000001:
                                roomName = "bupa_classic";
                                break;
                            case 100000002:
                                roomName = "bupa_superior";
                                break;
                            case 100000003:
                                roomName = "bupa_jnrsuite";
                                break;
                        };
                        var fetchXml = "?fetchXml=<fetch version='1.0' output-format='xml-platform' mapping='logical' distinct='false'>"
                            + "<entity name = 'bupa_ratecard'>"
                            + "<attribute name='bupa_classic' />"
                            + "<attribute name='bupa_deluxe' />"
                            + "<attribute name='bupa_superior' />"
                            + "<attribute name='bupa_jnrsuite' />"
                            + "<filter type='and'>"
                            + "<condition attribute='bupa_carehomeunitid' operator='eq' value='" + unitId + "'/>"
                            + "<condition attribute='bupa_fundingtype' operator='eq' value='" + rateCardFundingType + "'/>"
                            + "<condition attribute='bupa_bcsbanding' operator='eq' value='" + banding + "'/>"
                            + "<condition attribute='statecode' operator='eq' value='0'/>"
                            + "</filter>"
                            + "</entity>"
                            + "</fetch >";
                        var rateValue = await Xrm.WebApi.retrieveMultipleRecords('bupa_ratecard', fetchXml).then(
                            function success(result) {
                                return result.entities[0][roomName];
                            },
                            function (error) {
                                console.log(error.message);
                            }
                        );
                        formContext.getAttribute('bupa_ratecardfee').setValue(rateValue);
                        let saveOptions = {
                            saveMode: 1,
                            useSchedulingEngine: false
                        };

                        formContext.data.save(saveOptions).then(
                            function success() {
                                return;
                            },
                            function (error) {
                                console.log(error.message);
                            }
                        );
                    }
                    else if (careMatch == false) {
                        var warningMessage = "The resident's care need does not match the selected unit. Are you sure you want to admit them to this unit?";
                        var confirmStrings = { text: warningMessage, title: "Warning", cancelButtonLabel: "No", confirmButtonLabel: "Yes" };
                        var confirmOptions = { height: 200, width: 450 };
                        Xrm.Navigation.openConfirmDialog(confirmStrings, confirmOptions).then(
                            function (success) {
                                if (success.confirmed) {
                                    console.log("Success!");
                                    formContext.getControl("bupa_ratecardfee").setVisible(false);
                                }
                                else {
                                    formContext.getAttribute("bupa_carehomeunit").setValue(null);
                                    formContext.getAttribute("bupa_roomnumber").setValue(null);
                                    formContext.getAttribute('bupa_ratecardfee').setValue(null);
                                    return;
                                }
                            }
                        )
                    }
                }
                else if(rateCardFee !=null) {
                    formContext.getAttribute('bupa_ratecardfee').setValue(null);
                    let saveOptions = {
                        saveMode: 1,
                        useSchedulingEngine: false
                    };

                    formContext.data.save(saveOptions).then(
                        function success() {
                            return;
                        },
                        function (error) {
                            console.log(error.message);
                        }
                    );
                };
            }
        },
        RequestCommercialReview: async function (primaryControl) {
            var formContext = primaryControl;
            var PAAGUID = formContext.getAttribute("bupa_paa").getValue()[0].id;
            var PAAData = { "statuscode": 100000008 }
            await Xrm.WebApi.updateRecord('bupa_carehomepreadmissionassessmentform', PAAGUID, PAAData).then(
                function success(result) {
                    formContext.data.refresh(false);
                    let alertStrings = { confirmButtonLabel: 'OK', title: 'Fee review started', text: 'Thank you.\n\nThis PAA has been sent to the Commercial team to calculate a fee for this resident.\n\nYour Home Manager will be notified when the fee has been added and the PAA is ready for their approval.\n\nYou can now close this window.' };
                    let alertOptions = { height: 350, width: 260 };
                    Xrm.Navigation.openAlertDialog(alertStrings, alertOptions).then(
                        function success() { },
                        function (error) {
                            console.log(error.message);
                            // handle error conditions
                        }
                    );
                    console.log('Success!')
                },
                function (error) {
                    console.log(error.message);
                }
            );
        },
        OverrideRejection: async function (primaryControl) {
            var formContext = primaryControl;
            //var PAAGUID = formContext.getAttribute("bupa_paa").getValue()[0].id;
            //var PAAData = {"statuscode":100000005};
            var RDTeam = await Xrm.WebApi.retrieveMultipleRecords('team', "?$filter=(name eq 'BCS - Regional Directors')");
            var MDTeam = await Xrm.WebApi.retrieveMultipleRecords('team', "?$filter=(name eq 'BCS - Managing Directors')");
            var RDTeamId = RDTeam.entities[0].teamid;
            var MDTeamId = MDTeam.entities[0].teamid;
            var globalContext = Xrm.Utility.getGlobalContext();
            var userId = globalContext.userSettings.userId;
            var userName = globalContext.userSettings.userName;
            var userLookup = [
                {
                    id: userId,
                    name: userName,
                    entityType: "systemuser"
                }
            ];
            var results = await Xrm.WebApi.retrieveMultipleRecords("teammembership", "?$filter=((teamid eq '" + RDTeamId + "' or teamid eq '" + MDTeamId + "') and systemuserid eq '" + userId + "')");
            if (results !== null && results.entities.length !== 0) {
                let alertStrings = { confirmButtonLabel: 'OK', title: 'Please add comments', text: 'Thank you.\n\nPlease add your comments then click \'Save\'.' };
                let alertOptions = { height: 300, width: 260 };
                Xrm.Navigation.openAlertDialog(alertStrings, alertOptions).then(
                    function success() {
                        formContext.getAttribute("bupa_approvaloverrideby").setValue(userLookup);
                        formContext.getControl('bupa_approvaloverrideby').setVisible(true);
                        formContext.getControl('bupa_approvaloverridecomments').setVisible(true);
                        formContext.getAttribute('bupa_approvaloverridecomments').setRequiredLevel('required');
                        formContext.getControl('bupa_approvaloverridecomments').setFocus();
                    },
                    function (error) {
                        console.log(error.message);
                        // handle error conditions
                    }
                )
            }
            else {
                let alertStrings = { confirmButtonLabel: 'OK', title: 'Access Denied.', text: 'A rejected PAA can only be overriden by an RD/RSM or above.' };
                let alertOptions = { height: 300, width: 260 };
                Xrm.Navigation.openAlertDialog(alertStrings, alertOptions).then(
                    function success() { },
                    function (error) {
                        console.log(error.message);
                        // handle error conditions
                    }
                );
            };
        },
        filterTitle: function (executionContext) {
            var formContext = executionContext.getFormContext();
            var titleOptions = [108550000, 108550006, 108550007, 108550001, 100000043, 108550002, 108550004, 100000036, 100000025, 100000023, 100000013, 100000014, 100000019, 100000042, 100000018, 100000009, 100000010, 100000041, 100000027, 108550003, 100000007, 100000038, 100000011]
            var currentTitleOptions = formContext.getControl('bupa_residentcontacttitle').getOptions();
            for (let i = 0; i < currentTitleOptions.length; i++) {
                if (!titleOptions.includes(currentTitleOptions[i].value)) {
                    formContext.getControl('bupa_residentcontacttitle').removeOption(currentTitleOptions[i].value);
                }
            }
        },
        calculateTotalFee: function (executionContext) {
            var formContext = executionContext.getFormContext();

            // Get the values of the fields
            var residentContribution = formContext.getAttribute("bupa_residentcontribution").getValue() || 0;
            var fundedNursingCare = formContext.getAttribute("bupa_fundednursingcarefnc").getValue() || 0;
            var thirdPartyContribution = formContext.getAttribute("bupa_thirdpartycontribution").getValue() || 0;
            var localAuthorityContribution = formContext.getAttribute("bupa_localauthoritycontribution").getValue() || 0;
            var continuingHealthcare = formContext.getAttribute("bupa_continuinghealthcare").getValue() || 0;


            // Calculate the total
            var calculatedTotal = residentContribution + fundedNursingCare + thirdPartyContribution + localAuthorityContribution + continuingHealthcare;

            // Get the agreed fee value
            var agreedFee = formContext.getAttribute("bupa_agreedfee").getValue() || 0;

            // Compare the calculated total with the agreed fee if other fields contain data
            if (calculatedTotal !== agreedFee) {
                // Display an error message
                formContext.ui.setFormNotification("Total fee is different from the sum of fee breakdown figures. Please review and update.", "ERROR", "total_mismatch");
                return false;
            } else {
                // Clear the error message if the values match
                formContext.ui.clearFormNotification("total_mismatch");
                return true;
            }
        },
        //retrieving Opportunity record from PAA
        //Retrieving Resident Agreement Details record to copy fee breakdown
        copyFeeBreakDowntoResidentAgreement: async function (executionContext) {
            try {
                var formContext = executionContext.getFormContext();
                var PAA2Id = formContext.getAttribute("bupa_paa")?.getValue()[0].id;

                if (!PAA2Id) {
                    console.error("PAA2Id is null or undefined.");
                    return;
                }

                var preAdmissionResult = await Xrm.WebApi.retrieveRecord("bupa_carehomepreadmissionassessmentform", PAA2Id, "?$select=_bupa_opportunityid_value");
                var bupa_opportunityid = preAdmissionResult["_bupa_opportunityid_value"];

                if (!bupa_opportunityid) {
                    console.error("bupa_opportunityid is null or undefined.");
                    return;
                }

                var opportunityResult = await Xrm.WebApi.retrieveRecord("opportunity", bupa_opportunityid, "?$select=_bupa_residentagreementdetails_value");
                var bupa_residentagreementdetails = opportunityResult["_bupa_residentagreementdetails_value"];

                if (!bupa_residentagreementdetails) {
                    console.error("bupa_residentagreementdetails is null or undefined.");
                    return;
                }

                var record = {
                    bupa_residentcontribution: formContext.getAttribute("bupa_residentcontribution")?.getValue(),
                    bupa_fundednursingcarefnc: formContext.getAttribute("bupa_fundednursingcarefnc")?.getValue(),
                    bupa_thirdpartycontribution: formContext.getAttribute("bupa_thirdpartycontribution")?.getValue(),
                    bupa_localauthoritycontribution: formContext.getAttribute("bupa_localauthoritycontribution")?.getValue(),
                    bupa_continuinghealthcarechc: formContext.getAttribute("bupa_continuinghealthcare")?.getValue(),
                    bupa_initialmonthfee: formContext.getAttribute("bupa_initialmonthfee")?.getValue()
                };

                var updateResult = await Xrm.WebApi.updateRecord("bupa_residentagreementdetails", bupa_residentagreementdetails, record);
                console.log(updateResult.id);
            } catch (error) {
                console.error("Error in copyFeeBreakDowntoResidentAgreement: ", error.message);
            }
        },
        updateFieldVisibilityAndAccessibility: function (executionContext) {
           debugger;
            try {
                var formContext = executionContext.getFormContext();
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
                }
            } catch (err) {
                console.log("Error" + err.message);
            }
        },
        // Register the function on the OnChange event of the fields
        registerOnChangeEvents: function (executionContext) {
            var formContext = executionContext.getFormContext();

            formContext.getAttribute("bupa_residentcontribution").addOnChange(SDK.Bupa.Sales.RDT.PAA2.Form.calculateTotalFee);
            formContext.getAttribute("bupa_fundednursingcarefnc").addOnChange(SDK.Bupa.Sales.RDT.PAA2.Form.calculateTotalFee);
            formContext.getAttribute("bupa_thirdpartycontribution").addOnChange(SDK.Bupa.Sales.RDT.PAA2.Form.calculateTotalFee);
            formContext.getAttribute("bupa_localauthoritycontribution").addOnChange(SDK.Bupa.Sales.RDT.PAA2.Form.calculateTotalFee);
            formContext.getAttribute("bupa_continuinghealthcare").addOnChange(SDK.Bupa.Sales.RDT.PAA2.Form.calculateTotalFee);
            formContext.getAttribute("bupa_agreedfee").addOnChange(function (executionContext) {
                // Only validate if other fields contain data
                var formContext = executionContext.getFormContext();
                var otherFieldsContainData = formContext.getAttribute("bupa_residentcontribution").getValue() != null ||
                    formContext.getAttribute("bupa_fundednursingcarefnc").getValue() != null ||
                    formContext.getAttribute("bupa_thirdpartycontribution").getValue() != null ||
                    formContext.getAttribute("bupa_localauthoritycontribution").getValue() != null ||
                    formContext.getAttribute("bupa_continuinghealthcare").getValue() != null
                if (otherFieldsContainData) {
                    SDK.Bupa.Sales.RDT.PAA2.Form.calculateTotalFee(executionContext);
                }
            });
        },
        // Validate on save
        validateOnSave: function (executionContext) {
            if (!SDK.Bupa.Sales.RDT.PAA2.Form.calculateTotalFee(executionContext)) {
                // Prevent the form from saving
                executionContext.getEventArgs().preventDefault();
            }
            else {
                SDK.Bupa.Sales.RDT.PAA2.Form.copyFeeBreakDowntoResidentAgreement(executionContext);
            }
        },
        // This method set the default day care home unit and room, when admission analysis is set as Day Care
        setDayCareUnitAndRoomForResident1: async function (executionContext) {

            let formContext = executionContext.getFormContext();
            
            var careHomeUnitValue = formContext.getAttribute("bupa_carehomeunit")?.getValue();
            var roomNumberValue = formContext.getAttribute("bupa_roomnumber")?.getValue();

            let bupaCareHome;
            if (formContext.getAttribute("bupa_bupacarehome") != null
                && formContext.getAttribute("bupa_bupacarehome").getValue() != null)
                bupaCareHome = formContext.getAttribute("bupa_bupacarehome").getValue()[0].id;

            //var valueFetchXml;
            //if (bupaCareHomeAdmittedToResident1 != undefined)
            //    valueFetchXml = "<value uitype='bupa_bupacarehome'>" + bupaCareHomeAdmittedToResident1 + "</value>";

            let admissionanalysisforresident1 = formContext.getAttribute("bupa_admissionanalysis")?.getValue();
            if (bupaCareHome != null && (admissionanalysisforresident1 == 100000006 || admissionanalysisforresident1 == 100000002 || admissionanalysisforresident1 == 100000004 ||
                admissionanalysisforresident1 == 100000011 || admissionanalysisforresident1 == 100000014 || admissionanalysisforresident1 == 100000016)) {
                var fetchXml = "<fetch version='1.0' output-format='xml-platform' mapping='logical' distinct='false'>"
                    + "<entity name = 'bupa_carehomeresident'>"
                    + "<attribute name='bupa_carehomeresidentid' />"
                    + "<attribute name='bupa_carehomeunitdonotdelete' />"
                    + "<attribute name='bupa_roomnumberincheers' />"
                    + "<filter type='and'>"
                    + "<condition attribute='bupa_bupacarehome' operator='eq' uitype='bupa_bupacarehome' value='" + bupaCareHome
                    + "'/>"
                    + "<condition attribute='bupa_roomnumberincheers' operator='like' value='%999%'/>"
                    + "</filter>"
                    + "</entity>"
                    + "</fetch >";

                var escapedFetchXML = encodeURIComponent(fetchXml);
                var careHomeUnitLookup = [];
                var careHomeResidentLookup = [];
                await Xrm.WebApi.retrieveMultipleRecords("bupa_carehomeresident", "?fetchXml=" + escapedFetchXML).then(
                    function (results) {

                        if (results.entities.length == 1) {
                            careHomeUnitLookup[0] = {};
                            careHomeUnitLookup[0].id = results.entities[0]._bupa_carehomeunitdonotdelete_value;
                            careHomeUnitLookup[0].entityType = results.entities[0]['_bupa_carehomeunitdonotdelete_value@Microsoft.Dynamics.CRM.lookuplogicalname'];
                            careHomeUnitLookup[0].name = results.entities[0]['_bupa_carehomeunitdonotdelete_value@OData.Community.Display.V1.FormattedValue'];
                            careHomeResidentLookup[0] = {};
                            careHomeResidentLookup[0].id = results.entities[0].bupa_carehomeresidentid;
                            careHomeResidentLookup[0].entityType = "bupa_carehomeresident";
                            careHomeResidentLookup[0].name = results.entities[0].bupa_roomnumberincheers;
                        }
                    },
                    function (err) { throw err; });

                formContext.getControl("bupa_carehomeunit").setDisabled(true);
                formContext.getControl("bupa_roomnumber").setDisabled(true);
                formContext.getControl("bupa_roomnumber").setVisible(true);
                formContext.getAttribute("bupa_carehomeunit").setValue(careHomeUnitLookup);
                formContext.getAttribute("bupa_roomnumber").setValue(careHomeResidentLookup);
            }
            else {
                if (careHomeUnitValue != null && roomNumberValue != null) {
                    if ((careHomeUnitValue[0].name).indexOf("Admin") > -1 && (roomNumberValue[0].name).indexOf("999") > -1) {
                        formContext.getControl("bupa_carehomeunit").setDisabled(false);
                        formContext.getControl("bupa_roomnumber").setDisabled(false);
                        // formContext.getControl("bupa_carehomeresident").setVisible(false);
                        formContext.getAttribute("bupa_carehomeunit").setValue(null);
                        formContext.getAttribute("bupa_roomnumber").setValue(null);
                    }
                }
                //else {
                //    formContext.getControl("bupa_carehomeunit").setDisabled(false);
                //    formContext.getControl("bupa_roomnumber").setDisabled(false);
                //    // formContext.getControl("bupa_carehomeresident").setVisible(false);
                //    formContext.getAttribute("bupa_carehomeunit").setValue(null);
                //    formContext.getAttribute("bupa_roomnumber").setValue(null);
                //}
            }

        },
    }
}
