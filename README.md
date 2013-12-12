This is a simple set of Python (3.3) scripts for queueing up emails to be sent
later. It uses the SMTP protocol, which means you can use it with services like
Gmail.

To 'install', simply download `configure_account.py`, `configure_program.py`, and
`emailsched.py`. You'll need to have Python 3 installed for it to work. I've only
tested it on Windows 7. At a guess, I'd say it'll run just fine on other
versions of Windows, but I don't know about Linux, OSX or anything else.

Run `configure_account.py` to enter your email account details.
Run `configure_program.py` to choose program settings and create folders.

Note that mails might be sent late - up to the amount specified for the update
frequency (which is in seconds, btw) - so keep that value realistic.

Emails are simple plaintext files (any extension) with the following structure:

`year, month, day, hour, minute
from address
to address
subject
body`

For example:
`2013, 12, 11, 22, 11
henrebotha@gmail.com
bob@microsoft.com
Re: butts
Butts are funny! LOL

Regards,
H`

Everything after the subject line is considered part of the body, so feel free
to mix in line breaks and whatever else.

Store your emails in the email folder (`.\emails` by default). You can create and
edit emails while the main script is running; it will handle edits (including
changes to scheduled times).

Mails are moved to the archive folder (`.\archive` by default) when they are sent.
The program can handle multiple files with the same name in the archive, but
only up to a point, so try not to use one filename more than a thousand times,
or just clear out the archive every so often.
