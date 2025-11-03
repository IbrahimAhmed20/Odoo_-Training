from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import io
import base64
import xlwt
from odoo.tools import date_utils


class PrintLeadWizard(models.TransientModel):
    _name = 'print.lead.wizard'
    _description = 'Print Lead Wizard'
    
    # Fields for date range selection
    date_from = fields.Date('From Date', required=True)
    date_to = fields.Date('To Date', required=True)

    @api.model
    def default_get(self, fields_list):
        res = super(PrintLeadWizard, self).default_get(fields_list)
        today = fields.Date.context_today(self)
        res.update({
            'date_from': today,
            'date_to': today,
        })
        return res

    @api.constrains('date_from', 'date_to')
    def _check_date_range(self):
        """Ensure 'From Date' is not later than 'To Date'."""
        if self.date_from > self.date_to:
            raise ValidationError("The 'From Date' cannot be later than the 'To Date'.")

    def print_pdf(self):
        """Generate PDF report for leads filtered by create_date."""
        leads = self.env['crm.lead'].search([
            ('create_date', '>=', self.date_from),
            ('create_date', '<=', self.date_to),
        ])
        
        if not leads:
            raise UserError("No leads found for the selected date range.")
        
        action = self.env.ref('crm_custom.action_report_crm_lead', raise_if_not_found=False)
        
        if not action:
            raise UserError("Report action not found. Please upgrade the 'crm_custom' module.")
        
        return action.report_action(leads)

    def print_excel(self):
        """Generate Excel report for leads filtered by create_date."""
        leads = self.env['crm.lead'].search([
            ('create_date', '>=', self.date_from),
            ('create_date', '<=', self.date_to),
        ])

        if not leads:
            raise ValidationError("No CRM leads found for the selected date range.")

        # Create Excel file using xlwt
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Leads')

        # Define header row for Excel
        header_style = xlwt.XFStyle()  # Customize header style if needed
        sheet.write(0, 0, 'Lead ID', header_style)
        sheet.write(0, 1, 'Lead Name', header_style)
        sheet.write(0, 2, 'Creation Date', header_style)
        sheet.write(0, 3, 'User Test', header_style)
        sheet.write(0, 4, 'Tags', header_style)
        sheet.write(0, 5, 'Customer', header_style)
        sheet.write(0, 6, 'Email', header_style)
        sheet.write(0, 7, 'Phone', header_style)
        sheet.write(0, 8, 'Next Call Date', header_style)

        # Set column widths for a cleaner Excel layout
        sheet.col(0).width = 256 * 10  # Adjust the width as needed
        sheet.col(1).width = 256 * 20  # Adjust the width as needed
        sheet.col(2).width = 256 * 15  # Adjust the width as needed

        # Write data rows starting from row 1
        row = 1
        for lead in leads:
            sheet.write(row, 0, lead.id)
            sheet.write(row, 1, lead.name or '')
            
            # Format the creation date
            create_date = lead.create_date
            try:
                sheet.write(row, 2, create_date.strftime('%Y-%m-%d') if create_date else '')
            except ValueError:
                sheet.write(row, 2, str(create_date) if create_date else '')
            
            # Add more fields as needed
            sheet.write(row, 3, getattr(lead, 'user_test', '') or '')  # Custom field, ensure it exists
            sheet.write(row, 4, ', '.join(lead.tag_ids.mapped('name')) if lead.tag_ids else '')
            sheet.write(row, 5, lead.partner_id.name or '')
            sheet.write(row, 6, lead.email_from or '')
            sheet.write(row, 7, lead.phone or '')
            sheet.write(row, 8, lead.next_call_date.strftime('%Y-%m-%d') if lead.next_call_date else '')

            row += 1

        # Save the Excel file to a BytesIO stream
        excel_file = io.BytesIO()
        workbook.save(excel_file)
        excel_file.seek(0)

        # Create an attachment for the Excel file and return the download URL
        attachment = self.env['ir.attachment'].create({
            'name': 'crm_lead_report.xls',
            'datas': base64.b64encode(excel_file.read()).decode('utf-8'),
            'type': 'binary',
            'mimetype': 'application/vnd.ms-excel',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/?model=ir.attachment&id={attachment.id}&download=true',
            'target': 'self',
        }
