from __future__ import print_function
import shutil
import time
import fastreport_cloud_sdk
from fastreport_cloud_sdk.rest import ApiException
from pprint import pprint
import environ

report = "77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4NCjxSZXBvcnQgU2NyaXB0TGFuZ3VhZ2U9IkNTaGFycCIgUmVwb3J0SW5mby5DcmVhdGVkPSIwMS8xMS8yMDE3IDE5OjEwOjIzIiBSZXBvcnRJbmZvLk1vZGlmaWVkPSIwMy8yNC8yMDE3IDE3OjE0OjMxIiBSZXBvcnRJbmZvLkNyZWF0b3JWZXJzaW9uPSIxLjAuMC4wIj4NCiAgPFN0eWxlcz4NCiAgICA8U3R5bGUgTmFtZT0iU3R5bGUxIiBCb3JkZXIuU2hhZG93PSJ0cnVlIiBGaWxsLkNvbG9yPSJPcmFuZ2VSZWQiIEZvbnQ9IkFyaWFsIE5hcnJvdywgMzZwdCwgc3R5bGU9Qm9sZCwgSXRhbGljIiBBcHBseUJvcmRlcj0iZmFsc2UiIEFwcGx5RmlsbD0iZmFsc2UiLz4NCiAgICA8U3R5bGUgTmFtZT0iU3R5bGUyIiBUZXh0RmlsbC5Db2xvcj0iV2hpdGUiIEZvbnQ9IkFyaWFsLCAyNnB0LCBzdHlsZT1Cb2xkIiBBcHBseUJvcmRlcj0iZmFsc2UiIEFwcGx5RmlsbD0iZmFsc2UiLz4NCiAgICA8U3R5bGUgTmFtZT0iU3R5bGUzIiBGb250PSJHZW9yZ2lhLCAyNHB0IiBBcHBseUJvcmRlcj0iZmFsc2UiIEFwcGx5RmlsbD0iZmFsc2UiLz4NCiAgPC9TdHlsZXM+DQogIDxEaWN0aW9uYXJ5Lz4NCiAgPFJlcG9ydFBhZ2UgTmFtZT0iUGFnZTEiIExhbmRzY2FwZT0idHJ1ZSIgUGFwZXJXaWR0aD0iMjk3IiBQYXBlckhlaWdodD0iMjEwIiBSYXdQYXBlclNpemU9IjkiIEZpcnN0UGFnZVNvdXJjZT0iMTUiIE90aGVyUGFnZXNTb3VyY2U9IjE1IiBVbmxpbWl0ZWRIZWlnaHQ9InRydWUiPg0KICAgIDxSZXBvcnRUaXRsZUJhbmQgTmFtZT0iUmVwb3J0VGl0bGUxIiBXaWR0aD0iMTA0Ny4wNiIgSGVpZ2h0PSI2Ni4xNSI+DQogICAgICA8VGV4dE9iamVjdCBOYW1lPSJUZXh0MTIiIFRvcD0iMTguOSIgV2lkdGg9IjEwNDguOTUiIEhlaWdodD0iMjguMzUiIFRleHQ9IkJveCBQYWNrYWdlIHdpdGggUGhhcm1hY29kZSBhbmQgRUFOIiBIb3J6QWxpZ249IkNlbnRlciIgRm9udD0iQXJpYWwsIDE0cHQsIHN0eWxlPUJvbGQiLz4NCiAgICA8L1JlcG9ydFRpdGxlQmFuZD4NCiAgICA8RGF0YUJhbmQgTmFtZT0iRGF0YTEiIFRvcD0iNzEuODYiIFdpZHRoPSIxMDQ3LjA2IiBIZWlnaHQ9Ijc5My44Ij4NCiAgICAgIDxQb2x5Z29uT2JqZWN0IE5hbWU9IlBvbHlnb24xMSIgTGVmdD0iNTE5Ljc1IiBUb3A9IjE0MS43NSIgV2lkdGg9IjM3OCIgSGVpZ2h0PSI0OTEuNCIgUG9seVBvaW50cz0iMFwwXDB8Mzc4XDBcMXwzNzhcNDkxLjRcMXwwXDQ5MS40XDEiIENlbnRlclg9IjAiIENlbnRlclk9IjAiLz4NCiAgICAgIDxQb2x5Z29uT2JqZWN0IE5hbWU9IlBvbHlnb24xIiBMZWZ0PSIyOC4zNSIgVG9wPSIxNDEuNzUiIFdpZHRoPSIzNy40OCIgSGVpZ2h0PSI0OTEuNCIgUG9seVBvaW50cz0iMFwwXDB8LTE4LjlcMFwxfC0zNy40NzgwMlw5LjQ1XDF8LTM3LjQ3ODAyXDQ4MS45NVwxfC0xOC45XDQ5MS40XDF8MFw0OTEuNFwxfDBcNDcyLjVcMSIgQ2VudGVyWD0iMzcuNDc4MDIiIENlbnRlclk9IjAiLz4NCiAgICAgIDxQb2x5Z29uT2JqZWN0IE5hbWU9IlBvbHlnb24yIiBMZWZ0PSI1MTkuNzUiIFRvcD0iMjguMzUiIFdpZHRoPSIzNzgiIEhlaWdodD0iMzcuOCIgUG9seVBvaW50cz0iMFwwXDB8MFwtMTguOVwxfDkuNDVcLTM3LjhcMXwzNjguNTVcLTM3LjhcMXwzNzhcLTE4LjlcMXwzNzhcMFwxIiBDZW50ZXJYPSIwIiBDZW50ZXJZPSIzNy44Ii8+DQogICAgICA8UG9seWdvbk9iamVjdCBOYW1lPSJQb2x5Z29uNCIgTGVmdD0iNDQ0LjE1IiBUb3A9Ijg1LjA1IiBXaWR0aD0iNzUuNiIgSGVpZ2h0PSI1Ni43IiBQb2x5UG9pbnRzPSIwXDBcMHwtOS40NVwtOS40NVwxfC05LjQ1XC01Ni43XDF8LTQ3LjI1XC01Ni43XDF8LTc1LjZcLTI4LjM1XDF8LTc1LjZcMFwxIiBDZW50ZXJYPSI3NS42IiBDZW50ZXJZPSI1Ni43Ii8+DQogICAgICA8UG9seWdvbk9iamVjdCBOYW1lPSJQb2x5Z29uNSIgTGVmdD0iNDQ0LjE1IiBUb3A9IjYzMy4xNSIgV2lkdGg9Ijc1LjYiIEhlaWdodD0iNTYuNyIgUG9seVBvaW50cz0iMFwwXDB8MFwwXDF8OS40NVw5LjQ1XDF8OS40NVw1Ni43XDF8NDcuMjVcNTYuN1wxfDc1LjZcMjguMzVcMXw3NS42XDBcMSIgQ2VudGVyWD0iMCIgQ2VudGVyWT0iMCIvPg0KICAgICAgPFBvbHlnb25PYmplY3QgTmFtZT0iUG9seWdvbjYiIExlZnQ9Ijg5Ny43NSIgVG9wPSI4NS4wNSIgV2lkdGg9Ijc1LjYiIEhlaWdodD0iNTYuNyIgUG9seVBvaW50cz0iMFwwXDB8OS40NVwtOS40NVwxfDkuNDVcLTU2LjdcMXw0Ny4yNVwtNTYuN1wxfDc1LjZcLTI4LjM1XDF8NzUuNlwwXDEiIENlbnRlclg9IjAiIENlbnRlclk9IjU2LjciLz4NCiAgICAgIDxQb2x5Z29uT2JqZWN0IE5hbWU9IlBvbHlnb243IiBMZWZ0PSI4OTcuNzUiIFRvcD0iNjMzLjE1IiBXaWR0aD0iNzUuNiIgSGVpZ2h0PSI1Ni43IiBQb2x5UG9pbnRzPSIwXDBcMHwwXDI4LjM1XDF8MjguMzVcNTYuN1wxfDY2LjE1XDU2LjdcMXw2Ni4xNVw5LjQ1XDF8NzUuNlwwXDEiIENlbnRlclg9IjAiIENlbnRlclk9IjAiLz4NCiAgICAgIDxCYXJjb2RlT2JqZWN0IE5hbWU9IkJhcmNvZGUyIiBMZWZ0PSI2NDIuNiIgVG9wPSIzNy44IiBXaWR0aD0iMTQ4Ljc1IiBIZWlnaHQ9IjI4LjM1IiBBbmdsZT0iMTgwIiBTaG93VGV4dD0iZmFsc2UiIEJhcmNvZGU9IlBoYXJtYWNvZGUiIEJhcmNvZGUuUXVpZXRab25lPSJ0cnVlIi8+DQogICAgICA8UG9seWdvbk9iamVjdCBOYW1lPSJQb2x5Z29uOCIgTGVmdD0iNjYuMTUiIFRvcD0iNjMzLjE1IiBXaWR0aD0iMzc4IiBIZWlnaHQ9Ijc1LjYiIEZpbGwuQ29sb3I9Ik9yYW5nZSIgUG9seVBvaW50cz0iMFwwXDB8MFwtNzUuNlwxfDM3OFwtNzUuNlwxfDM3OFwwXDEiIENlbnRlclg9IjAiIENlbnRlclk9Ijc1LjYiLz4NCiAgICAgIDxQb2x5Z29uT2JqZWN0IE5hbWU9IlBvbHlnb24xMCIgTGVmdD0iNDQ0LjE1IiBUb3A9IjE0MS43NSIgV2lkdGg9Ijc1LjYiIEhlaWdodD0iNDkxLjQiIFBvbHlQb2ludHM9IjBcMFwwfDc1LjZcMFwxfDc1LjZcNDkxLjRcMXwwXDQ5MS40XDEiIENlbnRlclg9IjAiIENlbnRlclk9IjAiLz4NCiAgICAgIDxQb2x5Z29uT2JqZWN0IE5hbWU9IlBvbHlnb24xMiIgTGVmdD0iODk3Ljc1IiBUb3A9IjE0MS43NSIgV2lkdGg9Ijc1LjYiIEhlaWdodD0iNDkxLjQiIFBvbHlQb2ludHM9IjBcMFwwfDBcLTQ5MS40XDF8NzUuNlwtNDkxLjRcMXw3NS42XDBcMSIgQ2VudGVyWD0iMCIgQ2VudGVyWT0iNDkxLjQiLz4NCiAgICAgIDxQb2x5Z29uT2JqZWN0IE5hbWU9IlBvbHlnb245IiBMZWZ0PSI2Ni4xNSIgVG9wPSIxNDEuNzUiIFdpZHRoPSIzNzgiIEhlaWdodD0iNDkxLjQiIEZpbGwuQ29sb3I9Ik9yYW5nZSIgUG9seVBvaW50cz0iMFwwXDB8MFwtNDkxLjRcMXwzNzhcLTQ5MS40XDF8Mzc4XDBcMSIgQ2VudGVyWD0iMCIgQ2VudGVyWT0iNDkxLjQiLz4NCiAgICAgIDxUZXh0T2JqZWN0IE5hbWU9IlRleHQxIiBMZWZ0PSI5NC41IiBUb3A9IjMyMS4zIiBXaWR0aD0iNjYuMTUiIEhlaWdodD0iMjc0LjA1IiBUZXh0PSJMb3JlbSBJcHN1bSIgQW5nbGU9IjI3MCIgRm9udD0iQXJpYWwgTmFycm93LCAzNnB0LCBzdHlsZT1Cb2xkLCBJdGFsaWMiIFN0eWxlPSJTdHlsZTEiLz4NCiAgICAgIDxQb2x5Z29uT2JqZWN0IE5hbWU9IlBvbHlnb24xMyIgTGVmdD0iNTE5Ljc1IiBUb3A9IjY2LjE1IiBXaWR0aD0iMzc4IiBIZWlnaHQ9Ijc1LjYiIEZpbGwuQ29sb3I9Ik9yYW5nZSIgUG9seVBvaW50cz0iMFwwXDB8MFwtNzUuNlwxfDM3OFwtNzUuNlwxfDM3OFwwXDEiIENlbnRlclg9IjAiIENlbnRlclk9Ijc1LjYiLz4NCiAgICAgIDxUZXh0T2JqZWN0IE5hbWU9IlRleHQzIiBMZWZ0PSI4NS4wNSIgVG9wPSI2NDIuNiIgV2lkdGg9IjIxNy4zNSIgSGVpZ2h0PSI1Ni43IiBUZXh0PSJMb3JlbSBJcHN1bSIgRm9udD0iQXJpYWwgTmFycm93LCAyOHB0LCBzdHlsZT1Cb2xkLCBJdGFsaWMiLz4NCiAgICAgIDxUZXh0T2JqZWN0IE5hbWU9IlRleHQ0IiBMZWZ0PSI2NjEuNSIgVG9wPSI3NS42IiBXaWR0aD0iMjE3LjM1IiBIZWlnaHQ9IjU2LjciIFRleHQ9IkxvcmVtIElwc3VtIiBBbmdsZT0iMTgwIiBGb250PSJBcmlhbCBOYXJyb3csIDI4cHQsIHN0eWxlPUJvbGQsIEl0YWxpYyIvPg0KICAgICAgPFRleHRPYmplY3QgTmFtZT0iVGV4dDUiIExlZnQ9IjM3OCIgVG9wPSIxNzkuNTUiIFdpZHRoPSI0Ny4yNSIgSGVpZ2h0PSIxNjAuNjUiIEZpbGwuQ29sb3I9Ik9yYW5nZSIgVGV4dD0iMjAgY2FwcyIgQW5nbGU9IjI3MCIgRm9udD0iQXJpYWwsIDI2cHQsIHN0eWxlPUJvbGQiIFRleHRGaWxsLkNvbG9yPSJXaGl0ZSIgU3R5bGU9IlN0eWxlMiIvPg0KICAgICAgPFRleHRPYmplY3QgTmFtZT0iVGV4dDYiIExlZnQ9IjU0OC4xIiBUb3A9IjE5OC40NSIgV2lkdGg9IjMyMS4zIiBIZWlnaHQ9IjE4OSIgVGV4dD0iTG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVyIGFkaXBpc2NpbmcgZWxpdCwgc2VkIGRvIGVpdXNtb2QgdGVtcG9yIGluY2lkaWR1bnQgdXQgbGFib3JlIGV0IGRvbG9yZSBtYWduYSBhbGlxdWEuIFV0IGVuaW0gYWQgbWluaW0gdmVuaWFtLCBxdWlzIG5vc3RydWQgZXhlcmNpdGF0aW9uIHVsbGFtY28gbGFib3JpcyBuaXNpIHV0IGFsaXF1aXAgZXggZWEgY29tbW9kbyBjb25zZXF1YXQuIER1aXMgYXV0ZSBpcnVyZSBkb2xvciBpbiByZXByZWhlbmRlcml0IGluIHZvbHVwdGF0ZSB2ZWxpdCBlc3NlIGNpbGx1bSBkb2xvcmUgZXUgZnVnaWF0IG51bGxhIHBhcmlhdHVyLiBFeGNlcHRldXIgc2ludCBvY2NhZWNhdCBjdXBpZGF0YXQgbm9uIHByb2lkZW50LCBzdW50IGluIGN1bHBhIHF1aSBvZmZpY2lhIGRlc2VydW50IG1vbGxpdCBhbmltIGlkIGVzdCBsYWJvcnVtLiIgQW5nbGU9IjkwIiBGb250PSJBcmlhbCBOYXJyb3csIDEycHQiLz4NCiAgICAgIDxUZXh0T2JqZWN0IE5hbWU9IlRleHQyIiBMZWZ0PSIxNjAuNjUiIFRvcD0iNTAwLjg1IiBXaWR0aD0iNTYuNyIgSGVpZ2h0PSI5NC41IiBGaWxsLkNvbG9yPSJPcmFuZ2UiIFRleHQ9IjUwbWciIEhvcnpBbGlnbj0iSnVzdGlmeSIgQW5nbGU9IjI3MCIgRm9udD0iR2VvcmdpYSwgMjRwdCIgU3R5bGU9IlN0eWxlMyIvPg0KICAgICAgPFRleHRPYmplY3QgTmFtZT0iVGV4dDciIExlZnQ9IjMyMS4zIiBUb3A9IjY0Mi42IiBXaWR0aD0iNzUuNiIgSGVpZ2h0PSIyOC4zNSIgRmlsbC5Db2xvcj0iT3JhbmdlIiBUZXh0PSI1MG1nIiBIb3J6QWxpZ249Ikp1c3RpZnkiIEZvbnQ9Ikdlb3JnaWEsIDE2cHQiLz4NCiAgICAgIDxUZXh0T2JqZWN0IE5hbWU9IlRleHQ4IiBMZWZ0PSI1NjciIFRvcD0iMTAzLjk1IiBXaWR0aD0iNzUuNiIgSGVpZ2h0PSIyOC4zNSIgRmlsbC5Db2xvcj0iT3JhbmdlIiBUZXh0PSI1MG1nIiBIb3J6QWxpZ249Ikp1c3RpZnkiIEFuZ2xlPSIxODAiIEZvbnQ9Ikdlb3JnaWEsIDE2cHQiLz4NCiAgICAgIDxUZXh0T2JqZWN0IE5hbWU9IlRleHQ5IiBMZWZ0PSIzMjEuMyIgVG9wPSI2NzAuOTUiIFdpZHRoPSI5NC41IiBIZWlnaHQ9IjI4LjM1IiBGaWxsLkNvbG9yPSJPcmFuZ2UiIFRleHQ9IjIwIGNhcHMiIEZvbnQ9IkFyaWFsLCAxNnB0LCBzdHlsZT1Cb2xkIiBUZXh0RmlsbC5Db2xvcj0iV2hpdGUiLz4NCiAgICAgIDxUZXh0T2JqZWN0IE5hbWU9IlRleHQxMCIgTGVmdD0iNTQ4LjEiIFRvcD0iNzUuNiIgV2lkdGg9Ijk0LjUiIEhlaWdodD0iMjguMzUiIEZpbGwuQ29sb3I9Ik9yYW5nZSIgVGV4dD0iMjAgY2FwcyIgQW5nbGU9IjE4MCIgRm9udD0iQXJpYWwsIDE2cHQsIHN0eWxlPUJvbGQiIFRleHRGaWxsLkNvbG9yPSJXaGl0ZSIvPg0KICAgICAgPEJhcmNvZGVPYmplY3QgTmFtZT0iQmFyY29kZTMiIExlZnQ9IjU3Ni40NSIgVG9wPSI0NTMuNiIgV2lkdGg9IjExOS4zIiBIZWlnaHQ9IjEyOC43NSIgRmlsbC5Db2xvcj0iV2hpdGUiIEFuZ2xlPSI5MCIgQmFyY29kZT0iRUFOMTMiLz4NCiAgICAgIDxTaGFwZU9iamVjdCBOYW1lPSJTaGFwZTEiIExlZnQ9IjUxOS43NSIgVG9wPSIxNjAuNjUiIFdpZHRoPSIzNzgiIEhlaWdodD0iOS40NSIgQm9yZGVyLkNvbG9yPSJUcmFuc3BhcmVudCIgRmlsbC5Db2xvcj0iT3JhbmdlIi8+DQogICAgICA8U2hhcGVPYmplY3QgTmFtZT0iU2hhcGUyIiBMZWZ0PSI2Ni4xNSIgVG9wPSIxNjAuNjUiIFdpZHRoPSIzNzgiIEhlaWdodD0iOS40NSIgQm9yZGVyLkNvbG9yPSJUcmFuc3BhcmVudCIgRmlsbC5Db2xvcj0iV2hpdGUiLz4NCiAgICAgIDxUZXh0T2JqZWN0IE5hbWU9IlRleHQxMSIgTGVmdD0iNzE4LjIiIFRvcD0iNDUzLjYiIFdpZHRoPSI3NS42IiBIZWlnaHQ9IjEzMi4zIiBUZXh0PSJOdW5jIHF1aXMgcXVhbSB1dCBtYXVyaXMgbW9sZXN0aWUgZWxlbWVudHVtIGEgdmVsIGxvcmVtLiAiIEFuZ2xlPSI5MCIgRm9udD0iQXJpYWwgTmFycm93LCAxMnB0Ii8+DQogICAgICA8U2hhcGVPYmplY3QgTmFtZT0iU2hhcGU1IiBMZWZ0PSIxMDMuOTUiIFRvcD0iMjA3LjkiIFdpZHRoPSI1Ni43IiBIZWlnaHQ9IjU2LjciIEJvcmRlci5Db2xvcj0iV2hpdGUiIEJvcmRlci5XaWR0aD0iMiIgRmlsbC5Db2xvcj0iTWVkaXVtU2VhR3JlZW4iIFNoYXBlPSJEaWFtb25kIi8+DQogICAgICA8U2hhcGVPYmplY3QgTmFtZT0iU2hhcGU2IiBMZWZ0PSI4MTIuNyIgVG9wPSI1MjkuMiIgV2lkdGg9IjU2LjciIEhlaWdodD0iNTYuNyIgQm9yZGVyLkNvbG9yPSJXaGl0ZSIgQm9yZGVyLldpZHRoPSIyIiBGaWxsLkNvbG9yPSJNZWRpdW1TZWFHcmVlbiIgU2hhcGU9IkRpYW1vbmQiLz4NCiAgICAgIDxQb2x5Z29uT2JqZWN0IE5hbWU9IlBvbHlnb24zIiBMZWZ0PSI2Ni4xNSIgVG9wPSI3MDguNzUiIFdpZHRoPSIzNzgiIEhlaWdodD0iMzcuOCIgUG9seVBvaW50cz0iMFwwXDB8MFwxOC45XDF8OS40NTAwMDFcMzcuOFwxfDM2OC41NVwzNy44XDF8Mzc4XDE4LjlcMXwzNzhcMFwxIiBDZW50ZXJYPSIwIiBDZW50ZXJZPSIwIi8+DQogICAgICA8QmFyY29kZU9iamVjdCBOYW1lPSJCYXJjb2RlMSIgTGVmdD0iMTc5LjU1IiBUb3A9IjcwOC43NSIgV2lkdGg9IjE0OC43NSIgSGVpZ2h0PSIyOC4zNSIgU2hvd1RleHQ9ImZhbHNlIiBCYXJjb2RlPSJQaGFybWFjb2RlIiBCYXJjb2RlLlF1aWV0Wm9uZT0idHJ1ZSIvPg0KICAgIDwvRGF0YUJhbmQ+DQogIDwvUmVwb3J0UGFnZT4NCjwvUmVwb3J0Pg0K";

env = environ.Env()
environ.Env.read_env('.env')
TOKEN = env('TOKEN')
PROS = env('PROS')


def _config_api(token: str) -> fastreport_cloud_sdk.configuration.Configuration:
    configuration = fastreport_cloud_sdk.Configuration(
        host="https://fastreport.cloud",
        username='apikey',
        password=token,
    )
    return configuration

def get_subscription() -> fastreport_cloud_sdk.models.subscription_vm.SubscriptionVM:
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        a = fastreport_cloud_sdk.SubscriptionsApi(api_client)
        try:
            return a.subscriptions_get_subscription(id=PROS)
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_create_group: %s\n" % e)


def create_group(name: str):
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.GroupsApi(api_client)
        create_group_vm = fastreport_cloud_sdk.CreateGroupVM(name=name, subscription_id=PROS)

        try:
            api_response = api_instance.groups_create_group(create_group_vm=create_group_vm)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_create_group: %s\n" % e)


def _get_group(name: str = None) -> str:
    """Возвращает id группы с именем name"""
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.GroupsApi(api_client)
        skip = 0
        take = 10

        try:
            api_response = api_instance.groups_get_group_list(skip=skip, take=take)
            id = [i.id for i in api_response.groups if i.name == name]
            # print(api_response)
            return id[0]
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_get_group_list: %s\n" % e)


def update_name_group(name: str, new_name: str = None):
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        id = _get_group(name)
        api_instance = fastreport_cloud_sdk.GroupsApi(api_client)
        rename_group_vm = fastreport_cloud_sdk.RenameGroupVM(name=new_name)
        try:
            # api_response = api_instance.groups_create_group(create_group_vm=upd)
            # pprint(api_response)
            response = api_instance.groups_rename_group(id, rename_group_vm)

            pprint(response)
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_create_group: %s\n" % e)

def update_permissions_group(name: str, permissions: str = None):
    """НЕ РАБОТАЕТ"""
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.GroupsApi(api_client)
        id = _get_group(name)
        # update_group_permissions_vm = fastreport_cloud_sdk.UpdateGroupPermissionsVM()

        try:
            # Update permissions
            print(api_instance.groups_get_permissions(id))
            # api_instance.groups_update_permissions(id, update_group_permissions_vm=update_group_permissions_vm)
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_update_permissions: %s\n" % e)


def delete_group(name: str):
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.GroupsApi(api_client)
        id = _get_group(name)
        try:
            api_instance.groups_delete_group(id)
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_delete_group: %s\n" % e)




# create_group('qwerty')
# id = _get_group('qwerty')
# print(id)
# update_name_group('qwerty', new_name='qwerty123')
# update_permissions_group('qwerty123')