"""Excel extractor node for processing Leistungsverzeichnis."""

import pandas as pd
from typing import Dict, Any, List
from datetime import date
from src.models.state import ContractState
from src.models.contract import LeistungsverzeichnisData, PerformanceItem


def excel_extractor_node(state: ContractState) -> Dict[str, Any]:
    """
    Extract data from Leistungsverzeichnis Excel file.
    """
    print("📊 Extracting data from Leistungsverzeichnis...")

    updates = {
        "current_step": "excel_extractor",
        "messages": []
    }

    excel_path = state.get("excel_path")
    if not excel_path:
        updates["messages"].append({
            "role": "system",
            "content": "⚠️ No Excel file available, skipping Excel extraction"
        })
        return updates

    try:
        # Read Excel file (use the first row as header)
        df = pd.read_excel(excel_path, sheet_name=0, header=0)

        # Store raw data
        updates["leistungsverzeichnis_raw"] = df.to_dict('records')

        # Extract performance items
        performance_items = []
        subtotal = 0.0

        # Expected column mappings (adjust based on actual Excel structure)
        column_mappings = {
            'position': ['Pos', 'Position', 'Pos.', 'Nr', 'Number'],
            'description': ['Beschreibung', 'Description', 'Leistung', 'Leistungsbeschreibung', 'Text'],
            'quantity': ['Menge', 'Quantity', 'Anzahl', 'Amount'],
            'unit': ['Einheit', 'Unit', 'ME'],
            'unit_price': ['Einzelpreis', 'EP', 'Unit Price', 'Preis/Einheit'],
            'total_price': ['Gesamtpreis', 'GP', 'Total', 'Gesamt', 'Total Price']
        }

        # Find actual column names
        actual_columns = {}
        for key, possible_names in column_mappings.items():
            for col in df.columns:
                if any(name.lower() in str(col).lower() for name in possible_names):
                    actual_columns[key] = col
                    break

        # If we can't find columns, try to infer from data
        if not actual_columns:
            # Assume first 6 columns are: position, description, quantity, unit, unit_price, total_price
            if len(df.columns) >= 6:
                actual_columns = {
                    'position': df.columns[0],
                    'description': df.columns[1],
                    'quantity': df.columns[2],
                    'unit': df.columns[3],
                    'unit_price': df.columns[4],
                    'total_price': df.columns[5]
                }

        # Extract items
        for index, row in df.iterrows():
            try:
                # Skip empty rows
                if pd.isna(row.get(actual_columns.get('description', df.columns[1]))):
                    continue

                quantity = float(row.get(actual_columns.get('quantity', 1)) or 1)
                unit_price = float(row.get(actual_columns.get('unit_price', 0)) or 0)
                total_price = float(row.get(actual_columns.get('total_price', quantity * unit_price)) or quantity * unit_price)

                item = PerformanceItem(
                    position_number=str(row.get(actual_columns.get('position', index + 1)) or index + 1),
                    description=str(row.get(actual_columns.get('description', 'Item')) or 'Item'),
                    quantity=quantity,
                    unit=str(row.get(actual_columns.get('unit', 'pcs')) or 'pcs'),
                    unit_price=unit_price,
                    total_price=total_price,
                    notes=None
                )

                performance_items.append(item)
                subtotal += total_price

            except (ValueError, TypeError) as e:
                updates["messages"].append({
                    "role": "system",
                    "content": f"⚠️ Skipped row {index}: {str(e)}"
                })

        # Calculate totals
        tax_rate = 0.19  # 19% German VAT
        tax_amount = round(subtotal * tax_rate, 2)
        total_amount = round(subtotal + tax_amount, 2)

        # Create structured data
        leistungsverzeichnis_data = {
            "document_title": "Leistungsverzeichnis",
            "project_reference": state.get("verhandlungsprotokoll_data", {}).get("project_name", "Project"),
            "creation_date": date.today(),
            "performance_items": performance_items,
            "subtotal": round(subtotal, 2),
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "total_amount": total_amount,
            "currency": "EUR",
            "notes": None
        }

        updates["leistungsverzeichnis_data"] = leistungsverzeichnis_data
        updates["messages"].append({
            "role": "system",
            "content": f"✓ Extracted {len(performance_items)} items, Total: {total_amount:.2f} EUR"
        })

    except Exception as e:
        updates["error"] = f"Excel extraction failed: {str(e)}"
        updates["messages"].append({
            "role": "system",
            "content": f"❌ Excel extraction error: {str(e)}"
        })
        # Don't use defaults - return None and let the system handle missing data
        updates["leistungsverzeichnis_data"] = None

    return updates


