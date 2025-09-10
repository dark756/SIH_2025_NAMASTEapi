# TM2 Dataset File Format Guide

This document provides guidelines to prepare and validate TM2 dataset CSV files for successful ingestion by the TM2 Healthcare Data Ingestion Service.

## Required CSV Columns

The CSV file must contain the following columns with exact names (case-sensitive):

- `patient_id`: Unique identifier for the patient (string)
- `tm2_code`: Traditional medicine code (e.g., TM2.A01.01) (string)
- `condition_name`: Name of the medical condition (string)
- `system_type`: Medicine system type (e.g., Ayurveda, Siddha, Unani) (string)
- `severity`: Severity of the condition (e.g., Mild, Moderate, Severe, Critical) (string)
- `diagnosis_date`: Date of diagnosis (ISO 8601 date string recommended, e.g., 2023-09-10) (string)
- `practitioner_id`: Identifier for the healthcare provider (string)

## File Format Requirements

- File must be a CSV file with `.csv` extension.
- Encoding should be UTF-8 without BOM.
- The first row must contain the header with the required columns.
- Data rows must follow the header row.
- No empty rows or columns.
- Avoid extra spaces or special characters in headers.
- Dates should be in a parseable format (ISO 8601 preferred).

## Common Issues and Troubleshooting

- **Empty File**: Ensure the file contains data rows beyond the header.
- **Missing Columns**: Verify all required columns are present and spelled correctly.
- **Encoding Issues**: Save the file as UTF-8 without BOM to avoid parsing errors.
- **Empty Rows**: Remove any completely empty rows.
- **Invalid Data**: Check for invalid or missing values in required fields.
- **File Size**: Ensure the file size does not exceed the configured maximum limit.

## Sample CSV Content

```csv
patient_id,tm2_code,condition_name,system_type,severity,diagnosis_date,practitioner_id
PAT001,TM2.A01.01,Chronic Insomnia,Ayurveda,Mild,2023-09-01,PRAC123
PAT002,TM2.A02.05,Digestive Disorders,Siddha,Moderate,2023-08-15,PRAC456
```

## Submission Recommendations

- Validate your CSV file against this guide before uploading.
- Use a text editor or spreadsheet software that supports UTF-8 encoding.
- Test with a small sample file to confirm successful processing.
- Review server logs for detailed error messages if processing fails.

Following this guide will help ensure your TM2 dataset files are correctly formatted and accepted by the ingestion service.
