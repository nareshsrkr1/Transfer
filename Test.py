 updateFieldVisibilityAndAccessibility: function (executionContext) {
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
 
if (executionContext.getEventArgs() && executionContext.getEventArgs().getSaveMode() === 1) { // Save mode
            formContext.data.refresh(false).then(
                function success() {
                    console.log("Form refreshed successfully.");
                },
                function error(error) {
                    console.error("Error refreshing the form: " + error.message);
                }
            );
        }
                                  

     }
                }
            } catch (err) {
                console.log("Error" + err.message);
            }
        }
