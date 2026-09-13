import os
import shutil
import zipfile
from pathlib import Path

root = Path(r"D:\zero-trust-mfa-least-privilege")
zip_name = "NHOM_Zero_Trust_MFA_Least_Privilege.zip"
zip_path = root / zip_name

# Create archive from the required directory structure.
# Keep the required root folders and add README PDF.
for folder in ["SETUP", "SOURCE", "THESIS", "SOFT"]:
    if not (root / folder).exists():
        raise FileNotFoundError(f"Missing required folder: {folder}")

# Build a minimal valid PDF file for HUONGDAN.PDF
text = "Huong dan su dung - Zero Trust MFA Least Privilege"
content = "BT /F1 18 Tf 72 720 Td (" + text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)') + ") Tj ET"
objects = [
    b"<< /Type /Catalog /Pages 2 0 R >>",
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
    ("<< /Length " + str(len(content.encode('latin-1'))) + " >>\nstream\n" + content + "\nendstream").encode('latin-1'),
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
]

pdf = bytearray(b'%PDF-1.4\n')
offsets = [0]
for i, obj in enumerate(objects, start=1):
    offsets.append(len(pdf))
    pdf.extend(f"{i} 0 obj\n".encode('latin-1'))
    pdf.extend(obj)
    pdf.extend(b"\nendobj\n")
startxref = len(pdf)
pdf.extend(f"xref\n0 {len(objects)+1}\n".encode('latin-1'))
pdf.extend(b"0000000000 65535 f \n")
for off in offsets[1:]:
    pdf.extend(f"{off:010d} 00000 n \n".encode('latin-1'))
pdf.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{startxref}\n%%EOF\n".encode('latin-1'))

(root / 'HUONGDAN.PDF').write_bytes(bytes(pdf))

# Remove previous zip if present
if zip_path.exists():
    zip_path.unlink()

with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for folder in ['SETUP', 'SOURCE', 'THESIS', 'SOFT']:
        folder_path = root / folder
        for file_path in sorted(folder_path.rglob('*')):
            if file_path.is_file():
                zf.write(file_path, arcname=str(file_path.relative_to(root)))
    zf.write(root / 'HUONGDAN.PDF', arcname='HUONGDAN.PDF')

print(f"Created archive: {zip_path}")
print(f"Archive size: {zip_path.stat().st_size} bytes")
