This is a simple set of Python scripts for queueing up emails to be sent later.
It uses the SMTP protocol.
Run configure_account.py to enter your email account details.
Run configure_program.py to choose program settings.
Note that mails might be sent late - up to the amount specified for the update
frequency - so keep that value realistic.
Emails are simple plaintext files (any extension) with the following structure:

year, month, day, hour, minute
from address
to address
subject
body

For example:
2013, 12, 11, 22, 11
henrebotha@gmail.com
bob@microsoft.com
Re: butts
Butts are funny! LOL

Regards,
H

--end example

Everything after the subject line is considered part of the body, so feel free
to mix in line breaks and whatever else.
