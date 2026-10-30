
from pypdf import PdfWriter

# Mention PDF filenames in the exact order you want them merged.
pdf_files = [
 "1.pdf",
 "question 1.pdf",
 "2.pdf",
 "question 2.pdf",
 "3.pdf",
  "question 3.pdf",
 "question 4.pdf",
 "question 5.pdf",
]

# Output filename
output_file = "merged.pdf"

merger = PdfWriter()

# Merge PDFs in the order specified above
for pdf in pdf_files:
    print(f"Adding: {pdf}")
    merger.append(pdf)

# Save the merged PDF
merger.write(output_file)
merger.close()

print(f"\nSuccessfully merged PDFs into: {output_file}")
