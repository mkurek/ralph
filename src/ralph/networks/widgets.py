from django.forms.widgets import CheckboxInput
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html


class DHCPExposeCheckboxInput(CheckboxInput):
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
        btn = ''
        if self.check_test(value):
            final_attrs['checked'] = 'checked'
            btn = """
            <a href="/data_center/datacenterasset/19367/delete/"
               class="deletelink button small alert radius left_margin"
            >Delete DHCP entry</a>
            """
        if not (value is True or value is False or value is None or value == ''):
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(value)
        return format_html('<input{} />', flatatt(final_attrs)) + btn

MANAGE_DNS_EXTRA_INFO = {
    'warning': {
        'color': '#d6c016',
        'icon': 'fa-exclamation-triangle',
    },
    'error': {
        'color': 'red',
        'icon': 'fa-times-circle',
    },
    'ok': {
        'color': 'green',
        'icon': 'fa-check-circle',
    }
}

table = """
<table>

    <thead>
      <tr>

          <th>Name</th>

          <th>Type</th>

          <th>PTR</th>

          <th>Content</th>

      </tr>
    </thead>
  <tbody>
    <tr>
        <td>s12345.mydc.net</td>
        <td>A</td>
        <td><i class="fa fa-lg fa-check-circle" style="color: green"></i></td>
        <td>10.20.30.40</td>
    </tr>
    <tr>
        <td>mysql2-db1.dc5.alledc.net</td>
        <td>CNAME</td>
        <td></td>
        <td>s12345.mydc.net</td>
    </tr>
    <tr>
        <td>s12345.mydc.net</td>
        <td>TXT</td>
        <td></td>
        <td>LOCATION: DC5 / I / Rack 307 / 10 </td>
    </tr>
    <tr>
        <td>s12345.mydc.net</td>
        <td>TXT</td>
        <td></td>
        <td>CONFIGURATION_PATH: ralph_prod / db </td>
    </tr>

  </tbody>
</table>
"""


class ManageDNSCheckboxInput(CheckboxInput):
    def render(self, name, value, attrs=None):
        extra_info = self.attrs.pop('extra_info', {})
        final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
        tooltip = ''
        if self.check_test(value):
            final_attrs['checked'] = 'checked'

        if extra_info:
            tooltip = """
            <i
            style="color: {color};"
            class="fa fa-lg {icon} has-tip tip-top" data-tooltip aria-haspopup="true"
            title="{msg}"
            ></i>
            """.format(
                msg=extra_info['msg'],
                **MANAGE_DNS_EXTRA_INFO[extra_info['type']],
            )
        more = ''
        more_table = ''
        if self.attrs.get('show_more'):
            more = """
            <i class="fa fa-lg fa-caret-down dns-more-toggle"></i>
            """
            more_table = table

        if not (value is True or value is False or value is None or value == ''):
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(value)
        return """
            <div>
                <span>{}</span>
                <span>{}</span>
                <span class="float: right">{}</span>
            </div>
            <div class="dns-more">
                {}
            </div>
        """.format(format_html('<input{} />', flatatt(final_attrs)), tooltip, more, more_table)
