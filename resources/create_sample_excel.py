"""Create sample Leistungsverzeichnis Excel file."""

import pandas as pd
import os

# Create sample data for Leistungsverzeichnis
data = {
    'Pos': ['1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '3.1', '3.2', '3.3', '4.1', '4.2', '5.1'],
    'Beschreibung': [
        'Baustelleneinrichtung und Vorbereitung',
        'Erdaushub für Fundament',
        'Fundamentplatte 30cm, C25/30',
        'Bodenplatte EG, 25cm, C25/30',
        'Wände EG, Stahlbeton C25/30',
        'Decke über EG, 20cm, C25/30',
        'Wände 1.OG, Stahlbeton C25/30',
        'Decke über 1.OG, 20cm, C25/30',
        'Treppenhauskern, Sichtbeton SB3',
        'Stützen, Stahlbeton C30/37',
        'Bewehrung Stahl B500B',
        'Qualitätsprüfung und Dokumentation'
    ],
    'Menge': [1, 2500, 850, 1200, 450, 1200, 400, 1200, 6, 24, 125, 1],
    'Einheit': ['psch', 'm³', 'm³', 'm³', 'm³', 'm²', 'm³', 'm²', 'Stk', 'Stk', 't', 'psch'],
    'EP': [15000.00, 45.00, 320.00, 280.00, 420.00, 185.00, 420.00, 185.00, 8500.00, 2800.00, 1450.00, 5000.00],
    'GP': [15000.00, 112500.00, 272000.00, 336000.00, 189000.00, 222000.00, 168000.00, 222000.00, 51000.00, 67200.00, 181250.00, 5000.00]
}

# Create DataFrame
df = pd.DataFrame(data)

# Add summary rows
df = pd.concat([df, pd.DataFrame({
    'Pos': ['', '', ''],
    'Beschreibung': ['Zwischensumme netto', 'MwSt. 19%', 'Gesamtsumme brutto'],
    'Menge': ['', '', ''],
    'Einheit': ['', '', ''],
    'EP': ['', '', ''],
    'GP': [1840950.00, 349980.50, 2190930.50]
})], ignore_index=True)

# Save to Excel
output_path = 'resources/leistungsverzeichnis.xlsx'
os.makedirs('resources', exist_ok=True)

# Create Excel writer with formatting
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Leistungsverzeichnis', index=False)

    # Get the workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets['Leistungsverzeichnis']

    # Add title
    worksheet.insert_rows(1)
    worksheet['A1'] = 'LEISTUNGSVERZEICHNIS - Neubau Bürogebäude Berlin'
    worksheet.merge_cells('A1:F1')

    # Adjust column widths
    worksheet.column_dimensions['A'].width = 10
    worksheet.column_dimensions['B'].width = 50
    worksheet.column_dimensions['C'].width = 12
    worksheet.column_dimensions['D'].width = 10
    worksheet.column_dimensions['E'].width = 15
    worksheet.column_dimensions['F'].width = 15

print(f"Excel file created: {output_path}")