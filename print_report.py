from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import io
import base64
import xlwt
from odoo.tools import date_utils

class PrintPropertyWizard(models.TransientModel):
    _name = 'print.property.wizard'
    _description = 'Print Property Wizard'

    # Fields for date range selection and salesperson selection
    date_from = fields.Date('From Date', required=True)
    date_to = fields.Date('To Date', required=True)
    sales_agent_id = fields.Many2one('res.users', string="Sales Agent", required=True)


    @api.model
    def default_get(self, fields_list):
        res = super(PrintPropertyWizard, self).default_get(fields_list)
        today = fields.Date.context_today(self)
        res.update({
            'date_from': today,
            'date_to': today,
            'sales_agent_id': self.env.user.id,  # Default to current user as salesperson
        })
        return res

    @api.constrains('date_from', 'date_to')
    def _check_date_range(self):
        """Ensure 'From Date' is not later than 'To Date'."""
        if self.date_from > self.date_to:
            raise ValidationError("The 'From Date' cannot be later than the 'To Date'.")

    def print_excel(self):
        """Generate Excel report for properties filtered by create_date and grouped by salesperson."""
        # Correct filtering for sales agent using .id to get the actual ID
        properties = self.env['estate.property'].search([
            ('create_date', '>=', self.date_from),
            ('create_date', '<=', self.date_to),
            ('user_id', '=', self.sales_agent_id.id),
        ])

        if not properties:
            raise ValidationError("No properties found for the selected filters.")

        # Get company data
        company_name = "Estate_Alex"
        company_address = "123 Main St, Alexandria"  # Replace with actual address or logic

        # Create Excel file using xlwt
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Properties')

        # Define header style for Excel
        header_style = xlwt.XFStyle()
        header_style.font.bold = True
        header_style.alignment.horz = xlwt.Alignment.HORZ_CENTER
        header_style.alignment.vert = xlwt.Alignment.VERT_CENTER

        # Write company info and date range in merged header cells
        sheet.write_merge(0, 0, 0, 8, company_name, header_style)
        sheet.write_merge(1, 1, 0, 8, company_address, header_style)
        sheet.write_merge(2, 2, 0, 8, f"From: {self.date_from} To: {self.date_to}", header_style)
        sheet.write_merge(3, 3, 0, 8, f"Sales Agent: {self.sales_agent_id.name}", header_style)

        # Define Excel header row for the report
        sheet.write(4, 0, 'Name', header_style)
        sheet.write(4, 1, 'Property Code', header_style)
        sheet.write(4, 2, 'Expected Price', header_style)
        sheet.write(4, 3, 'Available on Web', header_style)
        sheet.write(4, 4, 'Sales State', header_style)
        sheet.write(4, 5, 'Sales Agent', header_style)
        sheet.write(4, 6, 'Property Type', header_style)
        sheet.write(4, 7, 'Commission Amount', header_style)

        # Set column widths for a cleaner Excel layout
        sheet.col(0).width = 256 * 20  # Name
        sheet.col(1).width = 256 * 15  # Property Code
        sheet.col(2).width = 256 * 15  # Expected Price
        sheet.col(3).width = 256 * 15  # Available on Web
        sheet.col(4).width = 256 * 15  # Sales State
        sheet.col(5).width = 256 * 20  # Sales Agent
        sheet.col(6).width = 256 * 15  # Property Type
        sheet.col(7).width = 256 * 15  # Commission Amount

        # Start writing data from row 5 onwards
        row = 5
        total_expected_price = 0
        for property in properties:
            sheet.write(row, 0, property.name or '')  # Property Name
            sheet.write(row, 1, property.property_code or '')  # Property Code
            sheet.write(row, 2, property.expected_price or '')  # Expected Price
            total_expected_price += property.expected_price if property.expected_price else 0
            sheet.write(row, 3, 'Yes' if property.available_on_web else 'No')  # Available on Web
            sheet.write(row, 4, property.state or '')  # Sales State
            sheet.write(row, 5, property.user_id.name if property.user_id else '')  # Sales Agent
            sheet.write(row, 6, property.property_type_id.name if property.property_type_id else '')  # Property Type
            sheet.write(row, 7, property.commission_amount or '')  # Commission Amount

            row += 1

        # Add Total Row
        sheet.write(row, 1, 'Total', header_style)
        sheet.write(row, 2, total_expected_price, header_style)

        # Save the Excel file to a BytesIO stream
        excel_file = io.BytesIO()
        workbook.save(excel_file)
        excel_file.seek(0)

        # Create an attachment for the Excel file and return the download URL
        attachment = self.env['ir.attachment'].create({
            'name': 'estate_property_report.xls',
            'datas': base64.b64encode(excel_file.read()).decode('utf-8'),
            'type': 'binary',
            'mimetype': 'application/vnd.ms-excel',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/?model=ir.attachment&id={attachment.id}&download=true',
            'target': 'self',
        }
