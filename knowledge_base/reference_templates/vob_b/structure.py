VOB_B_STRUCTURE = {
    "§1": {
        "title": "Art und Umfang der Leistung",
        "title_en": "Type and Scope of Work",
        "mandatory": True,
        "typical_clauses": [
            "1.1_leistungsbeschreibung",  # Description of work
            "1.2_leistungsverzeichnis_reference",  # Reference to LV
            "1.3_ausfuehrungsunterlagen",  # Execution documents (plans, specs)
            "1.4_nebenleistungen",  # Ancillary services
            "1.5_besondere_leistungen"  # Special services
        ],
        "critical_for": ["scope_definition", "claims_prevention"],
        "links_to_documents": ["Leistungsverzeichnis", "Ausführungspläne"],
        "common_disputes": [
            "Unklare Leistungsabgrenzung",
            "Fehlende Planungsunterlagen"
        ]
    },

    "§2": {
        "title": "Vergütung",
        "title_en": "Payment/Remuneration",
        "mandatory": True,
        "subsections": {
            "§2_Nr1": "Einheitspreise (Unit prices)",
            "§2_Nr2": "Pauschalsumme (Lump sum)",
            "§2_Nr3": "Stundenlohnarbeiten (Time & materials)",
            "§2_Nr4": "Mehrmengen/Mindermengen (Quantity variations)",
            "§2_Nr5": "Nachtragspreise (Change order pricing)",
            "§2_Nr6": "Stoffpreisgleitklausel (Material price escalation)",
            "§2_Nr7": "Abrechnung (Invoicing)",
            "§2_Nr8": "Abschlagszahlungen (Progress payments)"
        },
        "critical_for": ["payment_disputes", "change_orders", "cash_flow"],
        "links_to_documents": ["Leistungsverzeichnis", "Preisnachweise"],
        "calculation_fields": [
            "base_unit_prices",
            "total_contract_sum",
            "payment_milestone_percentages",
            "retention_percentage",
            "escalation_formula"
        ],
        "common_disputes": [
            "Streit über Nachtragspreise",
            "Mengenmehrungen > 10%",
            "Zahlungsverzug"
        ]
    },

    "§3": {
        "title": "Ausführungsunterlagen",
        "title_en": "Execution Documents",
        "mandatory": True,
        "typical_clauses": [
            "3.1_bereitstellung_unterlagen",  # Document provision by employer
            "3.2_pruefpflicht_auftragnehmer",  # Contractor's duty to check
            "3.3_hinweispflicht_fehler"  # Duty to notify errors
        ],
        "critical_for": ["delay_claims", "defect_liability"],
        "document_types": [
            "Ausführungspläne (Execution drawings)",
            "Statische Berechnungen (Structural calcs)",
            "Baubeschreibung (Building description)"
        ]
    },

    "§4": {
        "title": "Ausführung",
        "title_en": "Execution",
        "mandatory": True,
        "subsections": {
            "§4_Nr1": "Allgemeine Ausführungspflichten",
            "§4_Nr2": "Zutrittsrechte (Access rights)",
            "§4_Nr3": "Schutzmaßnahmen (Protection measures)",
            "§4_Nr4": "Behinderungsanzeige (Notice of impediment)",
            "§4_Nr7": "Baustelleneinrichtung (Site facilities)"
        },
        "critical_for": ["site_management", "delay_claims"],
        "common_clauses": [
            "Baustellenordnung",
            "Arbeitssicherheit",
            "Koordinierung mit anderen Gewerken"
        ]
    },

    "§5": {
        "title": "Ausführungsfristen",
        "title_en": "Execution Deadlines",
        "mandatory": True,
        "subsections": {
            "§5_Nr1": "Vertragliche Fristen (Contractual deadlines)",
            "§5_Nr2": "Beginn der Ausführung (Commencement)",
            "§5_Nr3": "Behinderungen (Impediments)",
            "§5_Nr4": "Fristverlängerung (Time extensions)"
        },
        "critical_for": ["delay_analysis", "liquidated_damages", "EOT_claims"],
        "date_fields": [
            "contract_start_date",
            "milestone_dates",
            "completion_date",
            "handover_date"
        ],
        "common_disputes": [
            "Behinderungsanzeige nicht rechtzeitig",
            "Fristverlängerungsanspruch",
            "Verzögerungsschäden"
        ]
    },

    "§6": {
        "title": "Behinderung und Unterbrechung",
        "title_en": "Hindrance and Interruption",
        "mandatory": True,
        "subsections": {
            "§6_Nr1": "Anzeigepflicht (Notification duty)",
            "§6_Nr2": "Behinderungsfolgen (Consequences of hindrance)",
            "§6_Nr3": "Vergütungsanspruch (Compensation claim)",
            "§6_Nr4": "Unterbrechung (Suspension)"
        },
        "critical_for": ["delay_claims", "compensation_claims"],
        "procedural_requirements": [
            "Schriftliche Anzeige unverzüglich",
            "Dokumentation der Behinderung",
            "Nachweis der Mehrkosten"
        ],
        "triggers_for": ["time_extension", "cost_claim", "termination"]
    },

    "§7": {
        "title": "Verteilung der Gefahr",
        "title_en": "Risk Allocation",
        "mandatory": True,
        "subsections": {
            "§7_Nr1": "Gefahrtragung bis Abnahme (Risk until acceptance)",
            "§7_Nr2": "Versicherungspflicht (Insurance obligations)"
        },
        "critical_for": ["insurance", "liability", "force_majeure"],
        "insurance_types": [
            "Bauleistungsversicherung",
            "Haftpflichtversicherung",
            "Bauherren-Haftpflicht"
        ]
    },

    "§8": {
        "title": "Kündigung durch den Auftraggeber",
        "title_en": "Termination by Employer",
        "mandatory": True,
        "subsections": {
            "§8_Nr1": "Freie Kündigung (Termination for convenience)",
            "§8_Nr2": "Wichtiger Grund (Termination for cause)",
            "§8_Nr3": "Vergütungsanspruch (Payment upon termination)"
        },
        "critical_for": ["termination_rights", "exit_strategy"],
        "notice_periods": "Variable by contract value",
        "financial_consequences": [
            "Vergütung erbrachter Leistungen",
            "Entschädigung nicht erbrachter Leistungen",
            "Gewinnausfall bei freier Kündigung"
        ]
    },

    "§9": {
        "title": "Kündigung durch den Auftragnehmer",
        "title_en": "Termination by Contractor",
        "mandatory": True,
        "grounds": [
            "Nichterfüllung durch AG",
            "Zahlungsverzug > 30 Tage",
            "Arbeitsunterbrechung > 3 Monate"
        ],
        "critical_for": ["contractor_protection", "payment_security"]
    },

    "§10": {
        "title": "Haftung der Vertragsparteien",
        "title_en": "Liability of Parties",
        "mandatory": True,
        "liability_types": [
            "Vertragliche Haftung",
            "Deliktische Haftung",
            "Haftungsbeschränkungen"
        ],
        "critical_for": ["risk_management", "insurance", "indemnity"],
        "common_modifications": [
            "Haftungsobergrenzen",
            "Ausschluss Mangelfolgeschäden",
            "Freistellungsverpflichtungen"
        ]
    },

    "§11": {
        "title": "Vertragsstrafe",
        "title_en": "Liquidated Damages",
        "mandatory": False,  # Only if parties agree
        "typical_structure": {
            "trigger": "Completion delay",
            "calculation": "€X per day of delay",
            "cap": "Usually 5-10% of contract sum",
            "prerequisites": "Keine Annahme/Abnahme"
        },
        "critical_for": ["schedule_enforcement", "damages"],
        "legal_limits": "Must be reasonable (§ 343 BGB)"
    },

    "§12": {
        "title": "Abnahme",
        "title_en": "Acceptance/Handover",
        "mandatory": True,
        "subsections": {
            "§12_Nr1": "Vollendung (Completion)",
            "§12_Nr2": "Abnahme (Acceptance)",
            "§12_Nr3": "Abnahmefiktion (Deemed acceptance)",
            "§12_Nr4": "Förmliche Abnahme (Formal acceptance)",
            "§12_Nr5": "Teilabnahme (Partial acceptance)"
        },
        "critical_for": ["warranty_start", "payment_trigger", "risk_transfer"],
        "legal_significance": [
            "Gefahrübergang",
            "Beginn Gewährleistung",
            "Umkehr Beweislast",
            "Fälligkeit Schlusszahlung"
        ],
        "document_output": "Abnahmeprotokoll"
    },

    "§13": {
        "title": "Mängelansprüche",
        "title_en": "Defect Claims/Warranty",
        "mandatory": True,
        "subsections": {
            "§13_Nr1": "Mängelbegriff (Definition of defect)",
            "§13_Nr2": "Mängelanzeige (Defect notification)",
            "§13_Nr3": "Mängelbeseitigung (Defect remedy)",
            "§13_Nr4": "Fristsetzung (Setting deadlines)",
            "§13_Nr5": "Selbstvornahme (Self-remedy by employer)",
            "§13_Nr6": "Minderung (Price reduction)",
            "§13_Nr7": "Schadensersatz (Damages)"
        },
        "warranty_period": {
            "standard": "4 years from acceptance",
            "VOB_specific": "Can be shortened to 2 years (building works)",
            "BGB_default": "5 years (if VOB not applied)"
        },
        "critical_for": ["quality_assurance", "warranty_management"],
        "procedural_requirements": [
            "Schriftliche Mängelanzeige",
            "Angemessene Frist zur Nachbesserung",
            "Dokumentation (Fotos, Gutachten)"
        ]
    },

    "§14": {
        "title": "Abrechnung",
        "title_en": "Final Account",
        "mandatory": True,
        "subsections": {
            "§14_Nr1": "Aufmaß (Measurement)",
            "§14_Nr2": "Aufmaßverfahren (Measurement procedure)",
            "§14_Nr3": "Abrechnung nach Zeichnung (As-built drawings)"
        },
        "critical_for": ["final_payment", "dispute_prevention"],
        "deliverables": [
            "Schlussrechnung (Final invoice)",
            "Aufmaßblätter (Measurement sheets)",
            "Bestandspläne (As-built drawings)"
        ]
    },

    "§15": {
        "title": "Stundenlohnarbeiten",
        "title_en": "Time & Materials Work",
        "mandatory": True,
        "when_applicable": "Unforeseen works, variations",
        "documentation_requirements": [
            "Stundenzettel (Time sheets)",
            "Materialnachweis (Material receipts)",
            "Geräteliste (Equipment list)"
        ],
        "approval_process": "Daily/weekly sign-off by site supervisor"
    },

    "§16": {
        "title": "Zahlung",
        "title_en": "Payment",
        "mandatory": True,
        "subsections": {
            "§16_Nr1": "Abschlagszahlungen (Progress payments)",
            "§16_Nr2": "Vorauszahlungen (Advance payments)",
            "§16_Nr3": "Schlusszahlung (Final payment)",
            "§16_Nr4": "Sicherheiten (Securities)",
            "§16_Nr5": "Zahlungsfristen (Payment terms)",
            "§16_Nr6": "Verzugszinsen (Default interest)"
        },
        "payment_terms": {
            "progress_payment_frequency": "Monthly",
            "payment_deadline": "Within 30 days of invoice (can be modified)",
            "retention": "Usually 5-10% until end of warranty",
            "default_interest": "Base rate + 9% (§ 288 BGB)"
        },
        "critical_for": ["cash_flow", "payment_disputes"],
        "securities": [
            "Bürgschaft (Bank guarantee)",
            "Sicherheitseinbehalt (Retention)",
            "Gewährleistungsbürgschaft (Warranty bond)"
        ]
    },

    "§17": {
        "title": "Sicherheitsleistung",
        "title_en": "Performance Security",
        "mandatory": False,
        "security_types": [
            "Vertragserfüllungsbürgschaft (Performance bond)",
            "Mängelansprüche-Bürgschaft (Warranty bond)",
            "Anzahlungsbürgschaft (Advance payment bond)"
        ],
        "typical_amounts": "5-10% of contract sum",
        "duration": "Until acceptance + warranty period"
    },

    "§18": {
        "title": "Streitigkeiten",
        "title_en": "Disputes",
        "mandatory": True,
        "dispute_resolution": [
            "Verhandlung (Negotiation)",
            "Schlichtung (Mediation) - optional",
            "Schiedsgericht (Arbitration) - if agreed",
            "Ordentliche Gerichte (Courts) - default"
        ],
        "critical_for": ["dispute_resolution", "jurisdiction"]
    }
}