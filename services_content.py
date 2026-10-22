"""Services: what each one is, what the client gets, and proof from real work.
Deliverables describe what is offered; prices only where Alhaji has set them (IT packages)."""

SERVICES = [
    dict(key='dashboards', group='data', icon='chart', title='Dashboards and reports', form='Dashboards and reports',
         lead='Power BI and Excel dashboards that refresh from your survey exports, with a view for each reader.',
         gets=['A clean data model that grows with each new export', 'Pages for field staff, managers and donors', 'Targets shown next to every key number', 'A short guide and a handover session'],
         fit='Programmes with monthly data and several audiences', proof=('case-epi-dashboard.html', 'EPI reporting dashboard')),
    dict(key='forms', group='data', icon='form', title='Survey and form design', form='Survey and form design',
         lead='Survey123 and KoboToolbox forms with lookups, skip logic, validation and QR autofill, tested before field use.',
         gets=['A complete XLSForm, built and versioned', 'Choice lists and rules that stop bad entries', 'Offline testing on real phones', 'Training for data collectors'],
         fit='Field teams, campaigns and facility reporting', proof=('case-survey123.html', 'Survey123 forms and field tools')),
    dict(key='quality', group='data', icon='check', title='Data quality audits', form='Data quality audits',
         lead='Checks for duplicates, GPS errors, impossible dose sequences, inconsistent names and missing records.',
         gets=['A cleaned dataset and an issue log', 'Feedback workbooks per team or worker', 'A summary report for management', 'Checks you can repeat every month'],
         fit='Datasets you are about to report or rely on', proof=('case-epi-data-audit.html', 'EPI data quality audit')),
    dict(key='reporting', group='data', icon='report', title='M&E reporting', form='M&E reporting',
         lead='Monthly and quarterly programme reports, indicator tracking and presentations for management, boards and donors.',
         gets=['Indicator reference sheets everyone can follow', 'A tracker against targets', 'Clear monthly or quarterly reports', 'Slides for board and donor meetings'],
         fit='Programmes reporting to donors, boards or the DHMT', proof=('resources.html', 'Free M&E templates')),
    dict(key='systems', group='data', icon='db', title='Data systems', form='Data systems',
         lead='Database and web tool design for tracking patients, supplies, staff or credentials, built for low connectivity.',
         gets=['Requirements and modules written down', 'Roles, permissions and approval routes', 'Offline-friendly web apps and databases', 'Documentation your team can maintain'],
         fit='Teams that have outgrown spreadsheets', proof=('case-dms.html', 'Data Management System')),
    dict(key='training', group='data', icon='teach', title='Training', form='Training',
         lead='Hands-on training in Excel, data entry, data quality and basic dashboards for programme and facility staff.',
         gets=['A session plan built around your work', 'Practice with anonymised real examples', 'Pre and post tests to show progress', 'Handouts people keep using'],
         fit='Facility staff, data clerks and programme teams', proof=('resources.html', 'Training templates')),
    dict(key='hardware', group='it', icon='tool', title='Technical support and hardware', form='Technical support and hardware',
         lead='Repairs, RAM and SSD upgrades, software installation, virus removal, printer and scanner setup.',
         gets=['Diagnosis before any purchase', 'Upgrades that extend a computer\'s life', 'Clean installs and virus removal', 'Advice on what to replace and when'],
         fit='Offices, clinics, schools and individuals', proof=('note-small-business-it.html', 'Why basic IT support matters')),
    dict(key='network', group='it', icon='wifi', title='Networking and internet', form='Networking and internet',
         lead='LAN and Wi-Fi setup, routers, network design and cable management for offices, NGOs and clinics.',
         gets=['Wi-Fi coverage across the whole office', 'Router and network configuration', 'Tidy, labelled cabling', 'A device setup checklist'],
         fit='Offices with slow or patchy connections', proof=('portfolio.html#projects', 'Office network support')),
    dict(key='web', group='it', icon='web', title='Web and digital', form='Web and digital',
         lead='Websites, domains and hosting, maintenance, professional email and basic graphics.',
         gets=['A fast site that works on phones', 'Domain, hosting and email setup', 'Contact by WhatsApp, phone and email', 'Updates and backups'],
         fit='Small organisations and businesses', proof=('case-this-website.html', 'This website')),
    dict(key='security', group='it', icon='lock', title='Security and backups', form='Security and backups',
         lead='Backup and recovery, antivirus and firewall setup, user accounts, access control and system checks.',
         gets=['A 3-2-1 backup routine that is tested', 'Antivirus and updates on every device', 'Separate accounts and two-step verification', 'A simple security checklist'],
         fit='Any office holding important files', proof=('note-backup-rule.html', 'The 3-2-1 backup rule')),
    dict(key='contracts', group='it', icon='office', title='Office and NGO IT support', form='Office and NGO IT support',
         lead='Support contracts, staff training, ICT consultancy and inventory tools for organisations.',
         gets=['A named person to call when things break', 'Regular maintenance visits', 'An IT asset register', 'An ICT needs assessment and plan'],
         fit='NGOs, clinics and schools without IT staff', proof=('#packages', 'IT support packages')),
]

AUDIENCES = [('NGOs and health programmes', 'people'), ('Clinics and health facilities', 'health'), ('Schools and colleges', 'browser'), ('Small businesses and offices', 'wrench')]

# ---------------------------------------------------------------- detail pages
DETAIL = {
 'dashboards': dict(
    intro='A dashboard is only useful when the person it is built for opens it and finds their answer. I build Power BI and Excel reports around your readers, from a clean data model that grows with each new export.',
    how=[('Agree the questions', 'Who reads the report, and what decision does each reader make?'), ('Shape the data', 'Clean the export and build a simple model with lookup tables.'), ('Build the pages', 'Headline numbers, trends, comparisons and a table, with targets shown.'), ('Check and hand over', 'Numbers checked against the source, then a guide and a handover session.')],
    faq=[('Power BI or Excel?', 'Excel suits small teams and simple sharing. Power BI suits larger data, several audiences and regular refreshes. I will recommend one after seeing your data.'),
         ('Can it update every month?', 'Yes. The report is designed so a new month is added by dropping in the new export with the same column names.')],
    notes=['note-dashboards-people-use', 'note-power-bi-kpis'], resources=['dashboard-design-checklist.pdf', 'indicator-tracker.xlsx'], cases=['case-epi-dashboard']),
 'forms': dict(
    intro='Most data quality problems start in the form. I build Survey123 and KoboToolbox forms that make the right entry the easy entry, and test them on real phones before your team goes to the field.',
    how=[('Map the questions', 'Only the questions your reports will use, in a sensible order.'), ('Build the XLSForm', 'Choice lists, skip logic, constraints and QR or lookup features.'), ('Test offline', 'Real phones, no signal, then sync and check every record arrives.'), ('Train and launch', 'A short session for collectors and a quick guide to keep.')],
    faq=[('Which tool should we use?', 'It depends on your team, your connectivity and where the data goes. I can help you choose between Survey123, KoboToolbox, ODK and CommCare.'),
         ('Can you fix an existing form?', 'Yes. I can review your current XLSForm, fix errors and add validation without losing existing data structure.')],
    notes=['note-survey123-mistakes', 'note-choosing-data-collection-tool', 'note-qr-code-registration'], resources=['xlsform-cheat-sheet.pdf', 'sample-epi-xlsform.xlsx', 'field-supervision-checklist.pdf'], cases=['case-survey123']),
 'quality': dict(
    intro='Before numbers reach a report, the records behind them should be checked. I review your dataset for the errors that matter most and give each team clear, fair feedback.',
    how=[('Receive a safe export', 'You send an export with identifying details removed or protected.'), ('Run the checks', 'Completeness, duplicates, GPS, dose or visit sequences and name consistency.'), ('Confirm and clean', 'Flags are confirmed before anything changes, and every correction is logged.'), ('Report back', 'A cleaned dataset, feedback per team and a summary for management.')],
    faq=[('Will you change our data?', 'Only after an issue is confirmed, and every change is recorded in a cleaning log so it can be traced.'),
         ('Can our team run the checks themselves later?', 'Yes. I can turn the checks into a monthly routine with a checklist and a log.')],
    notes=['note-check-epi-data-quality', 'note-clean-data-in-excel'], resources=['me-data-quality-checklist.pdf', 'data-cleaning-log.xlsx'], cases=['case-epi-data-audit']),
 'reporting': dict(
    intro='Good M&E reporting answers the same questions, the same way, every period. I help you define indicators clearly, track them against targets and turn them into reports people read.',
    how=[('Define the indicators', 'Numerator, denominator, source, frequency and owner for each one.'), ('Set up tracking', 'A tracker with baselines, targets and progress by period.'), ('Write the report', 'Highlights first, then indicators, changes, challenges and actions.'), ('Present it', 'Slides for management, board or donor meetings.')],
    faq=[('Can you work with our existing logframe?', 'Yes. I can review it, tighten indicator definitions and build tracking around it.'),
         ('Do you write donor reports?', 'I prepare the data, tables, charts and draft narrative for your team to review and submit.')],
    notes=['note-me-indicators', 'note-data-decisions'], resources=['indicator-reference-sheet.pdf', 'logframe-template.pdf', 'monthly-report-template.pdf', 'indicator-tracker.xlsx'], cases=['case-epi-dashboard']),
 'systems': dict(
    intro='When spreadsheets start to break, a simple database with clear rules can save hours every month. I design systems for patients, supplies, staff or credentials that work in low connectivity.',
    how=[('Understand the process', 'Who enters data, who checks it and who uses it.'), ('Design on paper', 'Tables, modules, roles and approval routes written down first.'), ('Build in steps', 'Start with the dataset that causes the most pain, then grow.'), ('Run side by side', 'Compare with the old system before switching over.')],
    faq=[('Do we need a big budget?', 'Not always. Some needs are met with Google Sheets and Apps Script; others need a database such as PostgreSQL. The choice depends on users, data and support.'),
         ('Will it work offline?', 'It can. Progressive web apps and local queues let staff keep working and sync later.')],
    notes=['note-excel-to-database', 'note-qr-code-registration'], resources=['data-cleaning-log.xlsx'], cases=['case-dms', 'case-staff-management', 'case-chw-card-studio']),
 'training': dict(
    intro='Training sticks when people practise on their own devices with examples from their own work. I run practical sessions in Excel, data entry, data quality and basic dashboards.',
    how=[('Check the starting point', 'A short pre-test shows what people already know.'), ('Plan the session', 'Objectives, a timed agenda and practice data with no real names.'), ('Teach by doing', 'Short demonstrations, then hands-on practice with support.'), ('Measure and follow up', 'A post-test, certificates where agreed, and a follow-up date.')],
    faq=[('How many people per session?', 'Small groups work best for hands-on practice. Tell me your numbers and I will suggest a plan.'),
         ('Can training be in Krio?', 'Yes. I train in English and Krio.')],
    notes=['note-clean-data-in-excel', 'note-check-epi-data-quality'], resources=['training-session-plan.pdf', 'training-tracker.xlsx'], cases=[]),
 'hardware': dict(
    intro='Slow or faulty computers cost hours every week. I diagnose the problem first, then fix, upgrade or advise, so you only spend money where it makes a difference.',
    how=[('Diagnose', 'Find the real cause before suggesting any purchase.'), ('Fix or upgrade', 'Repairs, RAM and SSD upgrades, clean installs and virus removal.'), ('Set up properly', 'Updates, antivirus, backups and the software you need.'), ('Advise', 'What to keep, what to replace and when.')],
    faq=[('Do you come to us?', 'Yes, in Bo and nearby areas. Some software problems can also be fixed remotely.'),
         ('Can an old computer be made faster?', 'Often yes. An SSD and more memory can make a big difference for a fraction of the cost of a new computer.')],
    notes=['note-small-business-it', 'note-protect-your-computer'], resources=['it-asset-register.xlsx', 'backup-security-checklist.pdf'], cases=[]),
 'network': dict(
    intro='Patchy Wi-Fi and unreliable connections slow everyone down. I design and set up networks that cover the whole office and are easy to maintain.',
    how=[('Survey the space', 'Where people work, where signal drops and what equipment you have.'), ('Design the network', 'Router placement, access points and cabling plan.'), ('Install and configure', 'Secure Wi-Fi, tidy labelled cables and tested coverage.'), ('Document', 'Passwords, settings and a device setup checklist kept safely.')],
    faq=[('Do we need new equipment?', 'Not always. Better placement and configuration often fixes coverage before anything is bought.'),
         ('Can guests use the Wi-Fi safely?', 'Yes. A separate guest network keeps visitors away from office computers and files.')],
    notes=['note-ict-needs-assessment', 'note-small-business-it'], resources=['it-asset-register.xlsx'], cases=[]),
 'web': dict(
    intro='A few clear pages can answer common questions, build trust and bring in enquiries at any hour. I build fast, phone-friendly sites and set up domains, hosting and email.',
    how=[('Plan the pages', 'Home, About, Services and Contact, with one clear message.'), ('Write and design', 'Real photos and proof, contact buttons where thumbs reach.'), ('Launch', 'Domain, hosting and professional email set up.'), ('Keep it working', 'Updates, backups and fresh content when things change.')],
    faq=[('Can hosting be free?', 'For simple sites, yes. This website is hosted free on GitHub Pages. Other options suit sites that need logins or shops.'),
         ('Can we update it ourselves?', 'Yes. I can choose a setup your team can edit, and show you how.')],
    notes=['note-small-organisation-website'], resources=[], cases=['case-this-website']),
 'security': dict(
    intro='Lost files, viruses and stolen accounts are mostly preventable. I set up backups that are tested, protection on every device and simple habits your team can follow.',
    how=[('Check the risks', 'Where important files live and how they are protected today.'), ('Set up backups', 'The 3-2-1 rule with a weekly routine and a tested restore.'), ('Protect devices and accounts', 'Antivirus, updates, separate accounts and two-step verification.'), ('Train the team', 'Spotting fake emails, safe sharing and what to do if something goes wrong.')],
    faq=[('We already have antivirus. Is that enough?', 'It helps, but backups, updates and account security matter just as much. A short check shows where the gaps are.'),
         ('What if we are hit by a virus?', 'Disconnect the computer, do not plug in backup drives, and get help. Tested backups make recovery much easier.')],
    notes=['note-backup-rule', 'note-protect-your-computer'], resources=['backup-security-checklist.pdf', 'new-staff-it-setup.pdf'], cases=[]),
 'contracts': dict(
    intro='Organisations without IT staff still need someone who knows their setup. I provide ongoing support, maintenance, staff training and planning on a monthly basis.',
    how=[('Assess', 'An ICT needs assessment of devices, network, data and skills.'), ('Agree the plan', 'What is covered, how often I visit and how to reach me.'), ('Maintain', 'Regular checks, updates, backups and an asset register.'), ('Review', 'A short review every quarter with priorities for the next one.')],
    faq=[('What does a contract include?', 'It depends on your size and needs. The Premium package is the starting point for ongoing monthly support.'),
         ('Do you support NGOs outside Bo?', 'Yes, remotely across Sierra Leone, with visits where needed.')],
    notes=['note-ict-needs-assessment', 'note-small-business-it'], resources=['it-asset-register.xlsx', 'new-staff-it-setup.pdf', 'backup-security-checklist.pdf'], cases=[]),
}

FINDER = [
    ('I need to see my programme results clearly', 'dashboards'),
    ('My team collects data on phones or paper', 'forms'),
    ('I am not sure our numbers are correct', 'quality'),
    ('I report to donors, a board or the DHMT', 'reporting'),
    ('Our spreadsheets are getting out of control', 'systems'),
    ('My staff need data or Excel skills', 'training'),
    ('Our computers are slow or keep breaking', 'hardware'),
    ('Our internet or Wi-Fi is unreliable', 'network'),
    ('We need a website or professional email', 'web'),
    ('I worry about losing files or viruses', 'security'),
    ('We have no one to look after our IT', 'contracts'),
]

PRICE_FACTORS = [
    ('Scope', 'How many forms, pages, indicators or devices are involved.'),
    ('Data', 'How much data there is and how clean it is to start with.'),
    ('People', 'How many users, audiences or trainees need to be supported.'),
    ('Location', 'Onsite in Bo, travel elsewhere, or fully remote.'),
    ('Deadline', 'Urgent work may need to be planned around other commitments.'),
    ('Support', 'One-off delivery or ongoing help after handover.'),
]
