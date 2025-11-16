from flask import send_file
import csv
import io

def export_to_csv(items, headers, filename):
    """Export items to CSV format"""
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(headers)
    
    for item in items:
        writer.writerow(item)
    
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    
    return send_file(
        output, 
        mimetype='text/csv', 
        as_attachment=True, 
        download_name=filename
    )