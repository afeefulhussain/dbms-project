/**
 * Main Frontend Script for Clinic & Hospital Management System
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Table Search / Filter Functionality
    const searchInputs = document.querySelectorAll('.table-search-input');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function () {
            const tableId = this.getAttribute('data-table');
            const table = document.getElementById(tableId);
            if (!table) return;

            const filter = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(filter)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // 2. Print Token Slip Modal Trigger
    window.printToken = function(name, token, docName, date, time) {
        const printWindow = window.open('', '_blank', 'width=450,height=600');
        printWindow.document.write(`
            <html>
            <head>
                <title>Appointment Token #${token}</title>
                <style>
                    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 25px; text-align: center; color: #1e293b; }
                    .header { border-bottom: 2px dashed #0284c7; padding-bottom: 15px; margin-bottom: 15px; }
                    .hospital-title { font-size: 20px; font-weight: bold; color: #0284c7; margin: 0; }
                    .token-box { margin: 20px auto; width: 90px; height: 90px; line-height: 90px; border-radius: 50%; background: #0284c7; color: white; font-size: 38px; font-weight: bold; }
                    .details { text-align: left; margin-top: 20px; line-height: 1.8; font-size: 14px; }
                    .footer { margin-top: 30px; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 10px; }
                    @media print { button { display: none; } }
                </style>
            </head>
            <body>
                <div class="header">
                    <h2 class="hospital-title">CLINIC MANAGEMENT SYSTEM</h2>
                    <p style="margin:5px 0 0 0;font-size:13px;color:#64748b;">Patient Appointment Slip</p>
                </div>
                <div class="token-box">${token}</div>
                <div class="details">
                    <p><strong>Patient Name:</strong> ${name}</p>
                    <p><strong>Doctor:</strong> ${docName}</p>
                    <p><strong>Date:</strong> ${date}</p>
                    <p><strong>Time:</strong> ${time}</p>
                    <p><strong>Status:</strong> Waiting for Consultation</p>
                </div>
                <div class="footer">
                    <p>Please wait for your token to be called.</p>
                    <button onclick="window.print()" style="padding: 8px 16px; background: #0284c7; color: white; border: none; border-radius: 6px; cursor: pointer;">Print Receipt</button>
                </div>
            </body>
            </html>
        `);
        printWindow.document.close();
    };

    // 3. Auto-hide alert messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
