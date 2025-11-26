FIDIC_RED_BOOK_STRUCTURE = {
    "PART_1_GENERAL": {
        "clauses": {
            "1": {
                "title": "General Provisions",
                "subclauses": {
                    "1.1": "Definitions",
                    "1.2": "Interpretation",
                    "1.3": "Communications",
                    "1.4": "Law and Language",
                    "1.5": "Priority of Documents",
                    "1.6": "Contract Agreement",
                    "1.7": "Assignment",
                    "1.8": "Delays Caused by Authorities",
                    "1.9": "Delayed Drawings or Instructions",
                    "1.10": "Employer's Use of Contractor's Documents",
                    "1.11": "Contractor's Use of Employer's Documents",
                    "1.12": "Confidentiality",
                    "1.13": "Compliance with Laws",
                    "1.14": "Joint and Several Liability"
                },
                "critical_for": ["legal_framework", "document_hierarchy"],
                "turkish_considerations": [
                    "Governing law often Turkish Law",
                    "Language: Turkish + English bilingual",
                    "Priority of documents must be clear"
                ]
            },

            "2": {
                "title": "The Employer",
                "subclauses": {
                    "2.1": "Right of Access to the Site",
                    "2.2": "Permits, Licences and Approvals",
                    "2.3": "Employer's Personnel",
                    "2.4": "Employer's Financial Arrangements",
                    "2.5": "Employer's Claims"
                },
                "critical_for": ["site_access", "permits", "employer_obligations"]
            },

            "3": {
                "title": "The Engineer",
                "subclauses": {
                    "3.1": "Engineer's Duties and Authority",
                    "3.2": "Delegation by the Engineer",
                    "3.3": "Instructions of the Engineer",
                    "3.4": "Replacement of the Engineer",
                    "3.5": "Determinations",
                    "3.7": "Agreement or Determination"
                },
                "critical_for": ["contract_administration", "determinations"],
                "key_difference_from_vob": "Engineer has significant authority (not in VOB)",
                "turkish_context": "Engineer role often controversial - local practice varies"
            },

            "4": {
                "title": "The Contractor",
                "subclauses": {
                    "4.1": "Contractor's General Obligations",
                    "4.2": "Performance Security",
                    "4.3": "Contractor's Representative",
                    "4.4": "Subcontractors",
                    "4.5": "Assignment of Benefit of Subcontract",
                    "4.6": "Co-operation",
                    "4.7": "Setting Out",
                    "4.8": "Safety Procedures",
                    "4.9": "Quality Assurance",
                    "4.10": "Site Data",
                    "4.11": "Sufficiency of the Accepted Contract Amount",
                    "4.12": "Unforeseeable Physical Conditions",
                    "4.13": "Rights of Way and Facilities",
                    "4.14": "Avoidance of Interference",
                    "4.15": "Access Route",
                    "4.16": "Transport of Goods",
                    "4.17": "Contractor's Equipment",
                    "4.18": "Protection of the Environment",
                    "4.19": "Electricity, Water and Gas",
                    "4.20": "Employer's Equipment and Free-Issue Material",
                    "4.21": "Progress Reports",
                    "4.22": "Security of the Site",
                    "4.23": "Contractor's Operations on Site",
                    "4.24": "Fossils"
                },
                "critical_for": ["contractor_obligations", "unforeseen_conditions"],
                "most_disputed_clauses": [
                    "4.11 - Sufficiency of Contract Amount",
                    "4.12 - Unforeseeable Physical Conditions"
                ],
                "turkish_specific": "4.12 heavily negotiated - ground conditions disputes common"
            }
        }
    },

    "PART_2_TIME": {
        "clauses": {
            "5": {
                "title": "Nominated Subcontractors",
                "subclauses": {
                    "5.1": "Definition of Nominated Subcontractor",
                    "5.2": "Objection to Nomination",
                    "5.3": "Payments to Nominated Subcontractors",
                    "5.4": "Evidence of Payments"
                },
                "critical_for": ["subcontractor_management"]
            },

            "6": {
                "title": "Staff and Labour",
                "subclauses": {
                    "6.1": "Engagement of Staff and Labour",
                    "6.2": "Rates of Wages and Conditions of Labour",
                    "6.3": "Persons in the Service of Employer",
                    "6.4": "Labour Laws",
                    "6.5": "Working Hours",
                    "6.6": "Facilities for Staff and Labour",
                    "6.7": "Health and Safety",
                    "6.8": "Contractor's Superintendence",
                    "6.9": "Contractor's Personnel",
                    "6.10": "Records of Contractor's Personnel and Equipment",
                    "6.11": "Disorderly Conduct",
                    "6.12": "Foreign Personnel",
                    "6.13": "Supply of Foodstuffs",
                    "6.14": "Supply of Water",
                    "6.15": "Measures against Insect and Pest Nuisance",
                    "6.16": "Alcoholic Liquor or Drugs",
                    "6.17": "Arms and Ammunition",
                    "6.18": "Festival and Religious Customs",
                    "6.19": "Funeral Arrangements",
                    "6.20": "Prohibition of Forced or Compulsory Labour",
                    "6.21": "Prohibition of Harmful Child Labour",
                    "6.22": "Employment Records of Workers"
                },
                "critical_for": ["labor_compliance", "HSE"],
                "turkish_critical": [
                    "6.4 - İş Kanunu compliance",
                    "6.12 - Work permits for foreign personnel",
                    "6.7 - İş Sağlığı ve Güvenliği requirements"
                ]
            },

            "7": {
                "title": "Plant, Materials and Workmanship",
                "subclauses": {
                    "7.1": "Manner of Execution",
                    "7.2": "Samples",
                    "7.3": "Inspection",
                    "7.4": "Testing",
                    "7.5": "Rejection",
                    "7.6": "Remedial Work",
                    "7.7": "Ownership of Plant and Materials",
                    "7.8": "Royalties"
                },
                "critical_for": ["quality_control", "testing"]
            },

            "8": {
                "title": "Commencement, Delays and Suspension",
                "subclauses": {
                    "8.1": "Commencement of Works",
                    "8.2": "Time for Completion",
                    "8.3": "Programme",
                    "8.4": "Extension of Time for Completion",
                    "8.5": "Delays Caused by Authorities",
                    "8.6": "Rate of Progress",
                    "8.7": "Delay Damages",
                    "8.8": "Suspension of Work",
                    "8.9": "Consequences of Suspension",
                    "8.10": "Payment for Plant and Materials in Event of Suspension",
                    "8.11": "Prolonged Suspension",
                    "8.12": "Resumption of Work"
                },
                "critical_for": ["schedule_management", "delay_claims", "EOT"],
                "most_critical_clauses": [
                    "8.4 - Extension of Time (EOT procedure)",
                    "8.7 - Delay Damages (liquidated damages)"
                ],
                "procedural_requirements": {
                    "8.4_EOT_claim": "Notice within 28 days of cause",
                    "8.7_LD_cap": "Usually 10% of Contract Price"
                },
                "turkish_considerations": [
                    "Force majeure provisions heavily negotiated",
                    "Weather delays - reference to historical data",
                    "Government delay provisions critical for PPP projects"
                ]
            },

            "9": {
                "title": "Tests on Completion",
                "subclauses": {
                    "9.1": "Contractor's Obligations",
                    "9.2": "Delayed Tests",
                    "9.3": "Retesting",
                    "9.4": "Failure to Pass Tests on Completion"
                },
                "critical_for": ["completion", "performance_testing"]
            },

            "10": {
                "title": "Employer's Taking Over",
                "subclauses": {
                    "10.1": "Taking Over of the Works and Sections",
                    "10.2": "Taking Over of Parts of the Works",
                    "10.3": "Interference with Tests on Completion",
                    "10.4": "Surfaces Requiring Reinstatement"
                },
                "critical_for": ["handover", "warranty_start"],
                "legal_significance": [
                    "Triggers warranty period (Clause 11)",
                    "Transfers risk to Employer",
                    "Triggers performance securities release (partial)"
                ],
                "document_output": "Taking Over Certificate"
            },

            "11": {
                "title": "Defects Liability",
                "subclauses": {
                    "11.1": "Completion of Outstanding Work and Remedying Defects",
                    "11.2": "Cost of Remedying Defects",
                    "11.3": "Extension of Defects Notification Period",
                    "11.4": "Failure to Remedy Defects",
                    "11.5": "Removal of Defective Work",
                    "11.6": "Further Tests",
                    "11.7": "Right of Access",
                    "11.8": "Contractor to Search",
                    "11.9": "Performance Certificate",
                    "11.10": "Unfulfilled Obligations",
                    "11.11": "Clearance of Site"
                },
                "critical_for": ["warranty", "defects_management"],
                "defects_notification_period": "Usually 12 months (can be longer)",
                "comparison_to_vob": "Shorter than VOB/B (12 months vs. 2-4 years)",
                "turkish_practice": "Often extended to 24 months in practice"
            }
        }
    },

    "PART_3_MONEY": {
        "clauses": {
            "12": {
                "title": "Tests after Completion",
                "subclauses": {
                    "12.1": "Procedure for Tests after Completion",
                    "12.2": "Delayed Tests",
                    "12.3": "Retesting",
                    "12.4": "Failure to Pass Tests after Completion"
                },
                "critical_for": ["performance_guarantees"]
            },

            "13": {
                "title": "Variations and Adjustments",
                "subclauses": {
                    "13.1": "Right to Vary",
                    "13.2": "Value Engineering",
                    "13.3": "Variation Procedure",
                    "13.4": "Payment in Applicable Currencies",
                    "13.5": "Provisional Sums",
                    "13.6": "Daywork",
                    "13.7": "Adjustments for Changes in Legislation",
                    "13.8": "Adjustments for Changes in Cost"
                },
                "critical_for": ["change_orders", "variations", "cost_adjustments"],
                "most_negotiated": [
                    "13.3 - Variation valuation method",
                    "13.8 - Price escalation formula"
                ],
                "turkish_specific": "13.7 critical due to frequent legislative changes",
                "valuation_hierarchy": [
                    "1. Bill of Quantities rates",
                    "2. Agreed rates",
                    "3. Engineer's determination"
                ]
            },

            "14": {
                "title": "Contract Price and Payment",
                "subclauses": {
                    "14.1": "The Contract Price",
                    "14.2": "Advance Payment",
                    "14.3": "Application for Interim Payment Certificates",
                    "14.4": "Schedule of Payments",
                    "14.5": "Plant and Materials intended for the Works",
                    "14.6": "Issue of Interim Payment Certificates",
                    "14.7": "Payment",
                    "14.8": "Delayed Payment",
                    "14.9": "Payment of Retention Money",
                    "14.10": "Statement at Completion",
                    "14.11": "Application for Final Payment Certificate",
                    "14.12": "Discharge",
                    "14.13": "Issue of Final Payment Certificate",
                    "14.14": "Cessation of Employer's Liability",
                    "14.15": "Currencies of Payment"
                },
                "critical_for": ["payment_cycle", "cash_flow", "final_account"],
                "payment_timeline": {
                    "interim_payment_period": "Monthly",
                    "engineer_certification": "28 days from application",
                    "employer_payment": "56 days from application",
                    "retention": "5-10% (50% released at Taking Over, 50% at end of DNP)",
                    "advance_payment": "Often 10-20% with bank guarantee"
                },
                "turkish_banking": "Payment in TRY or EUR/USD depending on contract",
                "default_interest": "Prevailing bank rate + margin"
            },

            "15": {
                "title": "Termination by Employer",
                "subclauses": {
                    "15.1": "Notice to Correct",
                    "15.2": "Termination by Employer",
                    "15.3": "Valuation at Date of Termination",
                    "15.4": "Payment after Termination",
                    "15.5": "Employer's Entitlement to Termination for Convenience"
                },
                "critical_for": ["termination_rights", "exit_costs"],
                "grounds_for_termination": [
                    "Contractor abandonment",
                    "Contractor insolvency",
                    "Failure to commence works",
                    "Suspension > 84 days",
                    "Assignment without consent",
                    "Bribery/corruption"
                ],
                "termination_for_convenience": "Employer can terminate without cause (15.5)",
                "financial_consequences": "Payment for work done + reasonable profit on unexecuted work (15.5)"
            },

            "16": {
                "title": "Suspension and Termination by Contractor",
                "subclauses": {
                    "16.1": "Contractor's Entitlement to Suspend Work",
                    "16.2": "Termination by Contractor",
                    "16.3": "Cessation of Work and Removal of Contractor's Equipment",
                    "16.4": "Payment on Termination"
                },
                "critical_for": ["contractor_protection", "payment_security"],
                "grounds_for_termination": [
                    "Non-payment > 56 days after due date",
                    "Prolonged suspension > 84 days",
                    "Force majeure > 140 days",
                    "Engineer fails to issue certificates",
                    "Employer's insolvency"
                ],
                "financial_consequences": "Full payment for work done + cost of repatriation + reasonable profit"
            },

            "17": {
                "title": "Risk and Responsibility",
                "subclauses": {
                    "17.1": "Indemnities",
                    "17.2": "Contractor's Care of the Works",
                    "17.3": "Employer's Risks",
                    "17.4": "Consequences of Employer's Risks",
                    "17.5": "Intellectual and Industrial Property Rights",
                    "17.6": "Limitation of Liability",
                    "17.7": "Use of Employer's Accommodation/Facilities"
                },
                "critical_for": ["risk_allocation", "liability", "insurance"],
                "employer_risks": [
                    "War, hostilities, invasion",
                    "Riots, disorder in country",
                    "Munitions of war, radiation",
                    "Pressure waves, ionizing radiation",
                    "Design prepared by Employer's Personnel",
                    "Use/occupation by Employer",
                    "Any operation of forces of nature which is Unforeseeable"
                ],
                "contractor_risks": "All risks not specifically allocated to Employer",
                "liability_caps": "Often capped at Contract Price (negotiable)"
            },

            "18": {
                "title": "Insurance",
                "subclauses": {
                    "18.1": "General Requirements for Insurances",
                    "18.2": "Insurance for Works and Contractor's Equipment",
                    "18.3": "Insurance against Injury to Persons and Damage to Property",
                    "18.4": "Insurance for Contractor's Personnel"
                },
                "critical_for": ["risk_mitigation", "insurance_compliance"],
                "required_insurances": [
                    "Works Insurance (all risks)",
                    "Contractor's Equipment Insurance",
                    "Third Party Liability",
                    "Employer's Personnel (if applicable)",
                    "Professional Indemnity (for design elements)"
                ],
                "turkish_requirements": "Zorunlu Trafik Sigortası, İş Kazası Sigortası (compulsory)",
                "claims_procedure": "Clause 17 & 18 interaction critical"
            },

            "19": {
                "title": "Force Majeure",
                "subclauses": {
                    "19.1": "Definition of Force Majeure",
                    "19.2": "Notice of Force Majeure",
                    "19.3": "Duty to Minimise Delay",
                    "19.4": "Consequences of Force Majeure",
                    "19.5": "Force Majeure Affecting Subcontractor",
                    "19.6": "Optional Termination, Payment and Release",
                    "19.7": "Release from Performance under the Law"
                },
                "critical_for": ["extraordinary_events", "termination"],
                "force_majeure_events": [
                    "War (unless in country already)",
                    "Rebellion, revolution",
                    "Strikes/lockouts (not by Contractor's personnel)",
                    "Natural catastrophes",
                    "Epidemic"
                ],
                "consequences": [
                    "Extension of Time (no cost)",
                    "Termination if > 140 days continuous",
                    "Each party bears own costs"
                ],
                "turkish_context": "Earthquakes explicitly included (frequent in Turkey)",
                "2020_addendum": "COVID-19 provisions often added"
            },

            "20": {
                "title": "Claims, Disputes and Arbitration",
                "subclauses": {
                    "20.1": "Contractor's Claims",
                    "20.2": "Appointment of the Dispute Avoidance/Adjudication Board",
                    "20.3": "Failure to Agree Dispute Avoidance/Adjudication Board",
                    "20.4": "Obtaining Dispute Avoidance/Adjudication Board's Decision",
                    "20.5": "Amicable Settlement",
                    "20.6": "Arbitration",
                    "20.7": "Failure to Comply with Dispute Avoidance/Adjudication Board's Decision",
                    "20.8": "Expiry of Dispute Avoidance/Adjudication Board's Appointment"
                },
                "critical_for": ["dispute_resolution", "claims_management"],
                "claims_procedure": {
                    "notice_deadline": "28 days of becoming aware",
                    "fully_detailed_claim": "42 days from notice",
                    "supporting_documentation": "Contemporary records critical"
                },
                "dispute_resolution_tiers": [
                    "1. Engineer's determination (mandatory first step)",
                    "2. DAAB (Dispute Avoidance/Adjudication Board)",
                    "3. Amicable settlement (56 days)",
                    "4. Arbitration (ICC usually)"
                ],
                "turkish_arbitration": [
                    "Istanbul Arbitration Centre (ISTAC)",
                    "ICC Paris",
                    "Often bilingual proceedings (Turkish/English)"
                ],
                "procedural_strictness": "VERY STRICT - missed deadlines = waiver of claims"
            }
        }
    }
}