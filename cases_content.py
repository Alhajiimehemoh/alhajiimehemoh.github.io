"""Case studies. Facts come only from what Alhaji has stated. Bodies use the notes markdown (notes_render.render).
::shot name | caption  places a design mockup from images/cases/<slug>/ inline."""

CASES = []


def case(**kw):
    CASES.append(kw)


case(slug='case-epi-dashboard', title='EPI reporting dashboard', status='Built', stage=3, types='health',
     short='Power BI report from monthly Survey123 immunisation exports, with views for nurses, managers, the DHMT and donors.',
     desc='Case study: a Power BI report built from monthly Survey123 immunisation exports at RHCI, designed to extend each month and serve nurses, management, the DHMT and donors.',
     lede='A Power BI report that turns each monthly Survey123 immunisation export into the same trusted view, for readers who need very different levels of detail.',
     tools=['Power BI', 'Survey123', 'Excel', 'Data modelling'],
     glance=[('Jan 2026', 'reporting from 1 January 2026 to date'), ('Monthly', 'new export added each month'), ('6', 'audiences, from nurses to donors'), ('3', 'build checkpoints')],
     facts=[('Organisation', 'Rural Health Care Initiative (RHCI), Bo District'), ('My role', 'Data Officer: design, build and data quality'),
            ('Data source', 'Survey123 EPI exports, supplied monthly'), ('Audience', 'Nurses, facilities, RHCI management, the DHMT, the RHCI Board and donors')],
     notes=['note-dashboards-people-use', 'note-power-bi-kpis', 'note-check-epi-data-quality'],
     resources=['dashboard-design-checklist.pdf', 'indicator-reference-sheet.pdf', 'reporting-timeliness-tracker.xlsx'],
     body='''## The challenge

Immunisation visit data at RHCI is collected in Survey123 and exported as files. Every month a new export arrives. Rebuilding a report by hand each time is slow, easy to get wrong and impossible to compare month to month. The numbers also need to be trusted by very different readers, from a nurse checking her own facility to a donor reading a summary.

## Who the report is for

| Reader | What they need to see |
| Nurses and facilities | Their own activity and what is outstanding |
| RHCI management | Programme-wide results and which facilities need support |
| DHMT | District-level summaries in a familiar shape |
| RHCI Board and donors | Headline results and trends over time |

## The approach

::flow Monthly Survey123 export > Checks and cleaning > Data model > Measures > Report pages by audience > Validation against source | The same path every month, so the report grows instead of being rebuilt.

The report covers 1 January 2026 to date and is designed to extend as each monthly export arrives. Instead of starting with charts, the build starts with a clean data model and a small set of trusted measures, then adds pages for each audience.

::shot 01-management-overview | Management overview: encounters by month, facility and activity.

## Built in checkpoints

The work moves through three staged checkpoints, and each one is reviewed before the next begins.

1. **Foundation:** the data model and structure, so every later page rests on the same tables.
2. **Build:** measures and report pages for each audience.
3. **Validation and handover:** figures checked against the source export before anything is released.

> **Tip:** Checking a few facilities by hand against the raw export at each checkpoint catches relationship and filter problems before readers do.

::shot 02-facility-and-nurse-performance | Facility and nurse performance: activity delivery and reporting completeness.

## Data quality first

A dashboard is only as good as the records behind it. The report builds on the data quality work I carried out on the nurse datasets, which checks GPS points, dose sequences, duplicates and village names before numbers reach a chart. That work is its own case study.

::shot 04-data-quality-review | Data quality review: flags grouped by issue type and a review queue.

## Where it stands

The report is built. Its structure is designed so that adding a new month means dropping in the new export rather than redesigning pages.

> **Example:** A manager opens the September page, sees which facilities fell short of expected activities, and the follow-up list is already written for the supervision meeting.''')

case(slug='case-epi-data-audit', title='EPI data quality audit', status='Completed', stage=3, types='health',
     short='A multi-stage review of March and April 2026 nurse datasets, with per-nurse audit workbooks and a cleaned dataset.',
     desc='Case study: a multi-stage EPI data quality analysis of March and April 2026 nurse datasets at RHCI, with GPS, dose sequence, duplicate and village checks, per-nurse audit workbooks and management reports.',
     lede='A multi-stage review of immunisation records collected by nurses, ending in a cleaned dataset, an audit workbook for every nurse and reports for management.',
     tools=['Excel', 'Data cleaning', 'Word', 'PowerPoint'],
     glance=[('2', 'months reviewed: March and April 2026'), ('5', 'types of quality check'), ('1', 'audit workbook per nurse'), ('1', 'cleaned dataset')],
     facts=[('Organisation', 'Rural Health Care Initiative (RHCI), Bo District'), ('My role', 'Data Officer: analysis, checks and reporting'),
            ('Period', 'March and April 2026 nurse datasets'), ('Outputs', 'Cleaned dataset, per-nurse Excel audit workbooks, Word reports, presentations')],
     cover='case-epi-dashboard/04-data-quality-review',
     notes=['note-check-epi-data-quality', 'note-clean-data-in-excel', 'note-data-decisions'],
     resources=['me-data-quality-checklist.pdf', 'data-cleaning-log.xlsx'],
     body='''## The challenge

Field records collected by nurses feed every immunisation report. If a GPS point is wrong, a dose is recorded out of order or a household is entered twice, the error travels all the way to the dashboard. Management needed to know how reliable the March and April 2026 data was, and each nurse needed specific, fair feedback.

## Five checks on every record

| Check | What it looks for |
| GPS validation | Locations that fall outside the expected area or are missing |
| Dose sequence | Doses recorded in an impossible order or too close together |
| Duplicate detection | The same visit or child recorded more than once |
| Village names | Different spellings of the same village that split the counts |
| Compliance per nurse | How each nurse's records measure up across the checks |

## The approach

::flow Raw nurse datasets > Stage-by-stage checks > Flag and confirm issues > Cleaned dataset > Per-nurse workbooks > Management reports | Each stage builds on the previous one, so nothing is corrected without a record of why.

The analysis ran in stages rather than as one pass. Each issue was flagged with the rule that caught it, so a correction could always be explained and traced back.

> **Watch out:** A flag is a question, not a verdict. Values that look wrong are confirmed before they are changed, and the reason is written down.

## What each audience received

- **Each nurse:** an Excel audit workbook showing their own records, what was flagged and why.
- **Management:** consolidated Word reports and presentations summarising quality across the team.
- **The data team:** a cleaned dataset ready for analysis and reporting.

## Why it matters

Feedback that names the exact record and the exact rule is easier to act on than a general request to "improve data quality". It also gives the EPI dashboard a stronger foundation, because the patterns found here become checks that run every month.''')

case(slug='case-survey123', title='Survey123 forms and field tools', status='Built', stage=3, types='health it',
     short='Hospitalisation notices, malaria campaign registration with QR autofill, an offline stock dashboard and a campaign inventory tracker.',
     desc='Case study: Survey123 XLSForms for hospitalisation notification and malaria campaign registration with QR autofill, an offline stock dashboard and an Excel campaign inventory tracker at RHCI.',
     lede='Forms and small tools that field and facility staff can use without a training manual, and that produce data a dashboard can trust.',
     tools=['Survey123', 'XLSForm', 'QR codes', 'Excel', 'HTML'],
     glance=[('4', 'tools built for field and office'), ('QR', 'autofill instead of retyping'), ('Offline', 'stock dashboard from CSV exports'), ('3 months', 'campaign across 4 locations')],
     facts=[('Organisation', 'Rural Health Care Initiative (RHCI), Bo District'), ('My role', 'Form design, build and testing'),
            ('Tools', 'Survey123 (XLSForm), Excel, HTML'), ('Audience', 'Field staff, facility staff and programme managers')],
     notes=['note-survey123-mistakes', 'note-qr-code-registration', 'note-stock-reconciliation'],
     resources=['xlsform-cheat-sheet.pdf', 'sample-epi-xlsform.xlsx', 'stock-tracker.xlsx'],
     body='''## The challenge

Field teams record information in difficult conditions: weak signal, busy clinics and long days. Every typed name, retyped ID or unchecked number becomes a cleaning job later. The goal was simple tools that make the right entry the easy entry.

## 1. Hospitalisation notification form

A Survey123 form for staff hospitalisation notices with cascading lookups. Choosing an employee limits the next list to that employee's dependants, so a notice can never be filed against the wrong family.

## 2. Malaria campaign registration and field visits

::shot 01-mobile-registration-form | Registration form: short sections, required fields marked and choices instead of typing.

A registration and field visit form where scanning a QR code fills in the patient's details. Staff scan instead of retyping, which removes typing errors and speeds up every visit.

::flow Register once > Print or issue QR code > Scan at each visit > Details filled in > Record the visit | One scan replaces several typed fields at every visit.

::shot 02-qr-autofill-follow-up | Follow-up visit: scanning the QR code fills in the record.

## 3. Offline stock dashboard

A private dashboard that works offline on Survey123 CSV exports. It reports by day and by location and calculates stock as opening balance plus restock minus use, with Excel and PDF export for reports.

::equation Opening stock + Restock - Used = Remaining stock | The rule the dashboard applies for every item, day and location.

::shot 04-offline-stock-dashboard | Offline stock dashboard with reorder flags.

## 4. Campaign inventory tracker

For a three-month mobile health campaign visiting four locations in rotation, one per week, I built an Excel tracker with a dashboard, a central store ledger and weekly log tabs. It records the stock taken on each trip, what was used and what came back, and keeps a running balance at the central store.

> **Tip:** Recording stock out and stock back on the same trip sheet makes the weekly reconciliation take minutes instead of hours.

## What ties them together

- Choices and lookups instead of free text
- Rules that catch mistakes at the point of entry
- Tools that keep working when the signal does not
- Outputs that drop straight into reports''')

case(slug='case-chw-card-studio', title='CHW Card Studio', status='Completed', stage=3, types='systems health',
     short='Issuing, printing and verifying credential cards for more than 1,000 Community Health Workers.',
     desc='Case study: a credential system for more than 1,000 Community Health Workers with permanent IDs, CR80 cards, QR codes and a public verification page, built for RHCI on Google tools.',
     lede='A system to issue, print and verify credential cards for Community Health Workers, so anyone can check that a card is genuine.',
     tools=['Google Sheets', 'Apps Script', 'Google Drive', 'QR codes', 'HTML'],
     glance=[('1,000+', 'Community Health Workers'), ('CR80', 'standard card size'), ('4', 'lifecycle events handled'), ('3', 'training types shown')],
     facts=[('Organisation', 'Rural Health Care Initiative (RHCI), Bo District'), ('My role', 'Specification, design and build'),
            ('Stack', 'Google Sheets, Apps Script, Google Drive'), ('Audience', 'Administrators, CHWs, facility staff and the public verifying a card')],
     notes=['note-qr-code-registration', 'note-chw-reporting'],
     resources=['it-asset-register.xlsx'],
     body='''## The challenge

More than 1,000 Community Health Workers serve communities on RHCI programmes. Facility staff, partners and community members need a quick way to confirm that someone presenting a card is a genuine, active CHW, and RHCI needs a reliable way to issue, renew and cancel those cards.

## What the system does

- Gives each CHW a permanent ID that never changes
- Produces standard CR80 cards with a QR code
- Handles the full card lifecycle: renewal, replacement, loss and revocation
- Provides a public verification page that confirms whether a card is valid
- Shows whether a CHW is Government-trained, MOMS-trained or dual-trained

::shot 01-card-and-qr-verification | Design mockup with a fictional worker: the sample card and the verification page.

## How verification works

::flow Scan the QR code > Short ID opens the verification page > System checks the register > Shows valid, expired or revoked > Only public details displayed | The QR code carries a short ID, not personal details. The register decides what is shown.

## Why Google tools

| Part | Tool | Why |
| Database | Google Sheets | Staff already know it; easy to review and export |
| Backend | Apps Script | Runs inside Google, no servers to pay for or maintain |
| Screens | Apps Script HTML Service | Simple web pages for staff and the public |
| Files | Google Drive | Stores CHW photos and QR images |

## Built one piece at a time

The build is broken into small parts, such as the card front, the card back, the print sheet and the verification page. Each part is approved before the next begins, so problems are caught while they are small.

> **Watch out:** A printed card cannot be changed. That is why the code holds only an ID, and why lost or revoked cards are cancelled in the register, not on the card.

## Related work already built

The staff medical ID card generator, a separate case study, applies many of the same ideas: print-ready cards, QR verification and security features. CHW Card Studio takes them to a larger scale with a full lifecycle.''')

case(slug='case-staff-id-cards', title='Staff medical ID card generator', status='Built', stage=3, types='systems it',
     short='A single-file HTML app that turns a staff and dependants workbook into print-ready ID cards with QR codes and security patterns.',
     desc='Case study: a single-file HTML app for RHCI that turns a staff and dependants workbook into print-ready 85.6 x 53.98 mm medical ID cards with QR verification and layered security features.',
     lede='A single-file app that turns a staff and dependants spreadsheet into print-ready medical ID cards, front and back, in one step.',
     tools=['HTML', 'JavaScript', 'Excel', 'QR codes', 'Print design'],
     glance=[('1 file', 'runs in a browser, no install'), ('85.6 x 54', 'mm card size, front and back'), ('QR', 'verification on every card'), ('Several', 'design versions refined')],
     facts=[('Organisation', 'Rural Health Care Initiative (RHCI), Bo District'), ('My role', 'Design and build'),
            ('Input', 'Staff and dependants Excel workbook'), ('Output', 'Print-ready front and back cards')],
     notes=['note-qr-code-registration'],
     resources=[],
     body='''## The challenge

Staff and their dependants needed medical ID cards. Designing each card by hand is slow and error-prone, and simple cards are easy to copy. The cards needed to be consistent, quick to produce and harder to fake.

## How it works

::flow Upload staff and dependants workbook > App reads each person > Front and back cards generated > Print sheet at card size > QR verification on each card | Everything runs in the browser from one HTML file.

- Upload the staff and dependants workbook
- The app builds a front and back card for each person
- Cards print at the standard 85.6 by 53.98 mm size
- Each card carries a QR code for verification

## Security layers

Cards are harder to copy when several small features are layered together:

- Guilloche patterns, the fine looping lines used on certificates and banknotes
- Microtext that looks like a line until you look closely
- Faded "ghost" portraits alongside the main photo
- Previews of where UV and holographic features would sit

> **Watch out:** True UV ink, holographic laminate and embossing need secure-card printing hardware. The app prepares the positions and previews; the physical features depend on the printer. Live QR checks depend on deploying a verification page.

## Refined through versions

The design went through several versions, including a version focused on faded portraits and a later design refinement. Each round made the cards clearer to read and harder to reproduce.

## Why a single file

A single HTML file runs on any computer with a browser, needs no installation and keeps the data on that computer. For a small team, that is often more practical than a hosted system.''')

case(slug='case-dms', title='Data Management System', status='Completed', stage=3, types='systems health',
     short='An 11-module system for vaccine coverage and nutrition tracking, built with PostgreSQL, Flask and a progressive web app.',
     desc='Case study: an 11-module data management system for RHCI to track vaccine coverage and nutrition, with role-based access, built with PostgreSQL, Flask and a progressive web app.',
     lede='An 11-module system for tracking vaccine coverage and nutrition, designed to work for nurses in the field and managers in the office.',
     tools=['PostgreSQL', 'Flask', 'PWA', 'System design', 'Documentation'],
     glance=[('11', 'modules'), ('2', 'user roles: admin and nurse'), ('PWA', 'installs on a phone, copes with weak signal'), ('Nov 2024', 'first scope written')],
     facts=[('Organisation', 'Rural Health Care Initiative (RHCI), Bo District'), ('My role', 'System design, documentation and build'),
            ('Stack', 'PostgreSQL, Flask, progressive web app'), ('Users', 'Administrators and nurses, with role-based access')],
     notes=['note-excel-to-database', 'note-chw-reporting'],
     resources=['data-cleaning-log.xlsx'],
     body='''## The challenge

Tracking vaccine coverage and nutrition for individual patients across visits quickly outgrows spreadsheets. Nurses need a simple way to record visits in the field, and managers need reliable reports, reminders and a view of missed appointments.

## What it covers

- Patient management
- Vaccine and nutrition tracking
- Appointments and reminders
- Missed appointment tracking
- Dashboards, graphs and reports
- Real-time notifications
- Role-based access for administrators and nurses

::shot 01-patient-registration-workspace | Design mockup with fictional records: a registration workspace with a built-in data quality checklist.

## How the design evolved

| When | Decision |
| November 2024 | First scope: malaria vaccine coverage and nutrition tracking with admin and nurse roles |
| Early plan | SQL Server, ASP.NET Core, React and related tools |
| January 2025 | Database moved to PostgreSQL |
| Completed system | Flask backend with a progressive web app |

## Why a progressive web app

A PWA installs on a phone like an app, opens quickly and can keep working when the signal is weak, then sync later. Nurses do not need app store downloads, and one codebase serves both phones and office computers.

::flow Nurse records visit on phone > Saved locally if offline > Syncs to PostgreSQL > Reminders and missed visits calculated > Manager dashboard updates | Field and office use the same data, not separate copies.

## Documentation

I produced planning documents across several versions, covering the modules, roles and data model, so a developer or a team can build from them without guessing.

> **Tip:** Writing the modules and roles down before any code is the cheapest place to change your mind.''')

case(slug='case-campaign-inventory', title='Campaign inventory tracker', status='Built', stage=3, types='health it', motif='boxes',
     short='Excel stock tracking for a three-month mobile health campaign rotating across four locations, with a central store ledger and weekly logs.',
     desc='Case study: an Excel inventory tracker for a three-month RHCI mobile health campaign visiting four locations in rotation, with a dashboard, central store ledger and weekly trip logs.',
     lede='An Excel tracker that follows every item from the central store to each campaign trip and back, so the balance is always known.',
     tools=['Excel', 'Stock reconciliation', 'Dashboards'],
     glance=[('3 months', 'mobile health campaign'), ('4', 'locations visited in rotation'), ('1 per week', 'location visited each week'), ('3', 'kinds of tab: dashboard, ledger, weekly logs')],
     facts=[('Organisation', 'Rural Health Care Initiative (RHCI), Bo District'), ('My role', 'Lead on medication and inventory tracking'),
            ('Tools', 'Excel'), ('Audience', 'Campaign team, store keeper and programme management')],
     notes=['note-stock-reconciliation', 'note-clean-data-in-excel'],
     resources=['stock-tracker.xlsx'],
     body='''## The challenge

A mobile health campaign carries medicines and supplies out of a central store to a different community each week. Without careful tracking, it becomes impossible to say how much was taken, how much was used and how much should still be in the store. Over three months and four locations, small gaps add up.

## How the tracker is organised

| Tab | What it does |
| Dashboard | Shows remaining stock, what each trip used and items running low |
| Central store ledger | The running balance of every item in the store |
| Weekly log tabs | One per trip: stock taken out, stock used, stock brought back |

## The flow of stock

::flow Central store > Stock taken on the trip > Used at the location > Remaining brought back > Store balance updated | Every trip opens and closes in the same way, so nothing goes missing between weeks.

::equation Store balance + Returned from trip - Taken for trip = New store balance | The rule behind the central store ledger.

## Why this works

- One trip, one log tab, filled in the same way every week
- The store ledger updates from the weekly logs, so balances are never typed twice
- The dashboard gives managers the picture without opening every tab

> **Tip:** Count and record what comes back on the same day the team returns. Waiting until the next trip is how stock disappears from the records.

## The same idea, free

A simplified version of this approach is in the free stock tracker below, with months of stock and REORDER flags built in.''')

case(slug='case-staff-management', title='Staff management system', status='Completed', stage=3, types='systems', motif='people',
     short='A system for managing staff and employment records with roles, approvals, duplicate checks, audit trails and offline sync.',
     desc='Case study: an RHCI staff and employment records system with roles and permissions, approval routes, duplicate checking, audit trails, Excel import and export, offline queue and PostgreSQL sync.',
     lede='A staff records system planned decision by decision, then built with roles, approvals, audit trails and offline sync.',
     tools=['System design', 'PostgreSQL', 'Web app', 'Offline sync', 'Excel import'],
     glance=[('4', 'record modules'), ('Roles', 'permissions and approval routes'), ('Audit', 'every change recorded'), ('Offline', 'local queue, then sync')],
     facts=[('Organisation', 'Rural Health Care Initiative (RHCI), Bo District'), ('My role', 'Planning, system design and build'),
            ('Status', 'Completed'), ('Stack', 'Cloud PostgreSQL with a synchronised web app')],
     notes=['note-excel-to-database', 'note-ict-needs-assessment'],
     resources=['data-cleaning-log.xlsx', 'new-staff-it-setup.pdf'],
     body='''## The challenge

Staff and employment records are sensitive, change often and are touched by several people: HR, finance, managers and the owner of the organisation. Spreadsheets make it hard to control who changes what, to avoid duplicate records or to know what a record looked like last month.

## What the system covers

- Owner-level access with oversight of everything
- Four record modules for staff and employment information
- Roles and permissions, so each person sees only what they need
- Approval routes for changes that need sign-off
- Duplicate checking before a new record is saved
- Audit trails showing who changed what and when
- Excel import and export, so existing records can move in and reports can move out
- An offline local queue that syncs to a cloud PostgreSQL database and web app

## How a change moves through the system

::flow Staff member edits a record > Duplicate and rule checks > Approval route if needed > Saved with audit entry > Synced to the cloud database | Nothing important changes without a check and a record.

## Planned before it was built

The work started as a decision-by-decision planning workspace: each question about modules, roles, approvals and sync was answered and recorded before development, so the build followed a clear plan.

> **Tip:** Writing down who can approve what is often harder than writing the code. Doing it first avoids rebuilding screens later.

## Why offline matters

Power and internet are not always reliable. A local queue lets staff keep working and sync later, instead of losing changes or waiting for the connection to return.''')

case(slug='case-encms', title='College management system (ENCMS)', status='In progress', stage=2, types='systems', motif='browser',
     short='A cloud-based management platform for Every Nation College, from admissions to results, being built in phases.',
     desc='Case study: the Every Nation College Management System, in progress, a cloud-based platform for admissions, payments, course registration, results approval and student records.',
     lede='A cloud-based management platform for a college, scoped carefully and planned in phases rather than rushed.',
     tools=['System design', 'Cloud hosting', 'Web and mobile', 'Workflow design', 'QR verification'],
     glance=[('Phased', 'current students first, old records later'), ('5', 'step results approval chain'), ('Web + mobile', 'access from any device'), ('Multi-campus', 'ready from the start')],
     facts=[('Organisation', 'Every Nation College'), ('My role', 'Requirements, scope and system planning'),
            ('Status', 'In progress'), ('Approach', 'Phased rollout, not rushed')],
     notes=['note-excel-to-database', 'note-small-organisation-website'],
     resources=[],
     body='''## The challenge

A growing college runs on many connected processes: admissions, fees, course registration, grading, results and student records. When these live in separate files and paper forms, students wait, staff repeat work and results are hard to protect.

## Scope of the platform

| Area | What it covers |
| Admissions | Online applications with an application fee |
| Payments | Bank payments with automatic confirmation, plus a slip or manual fallback |
| Fees | Instalments, invoices, receipts and a minimum payment threshold before results are released |
| Academics | Semester course registration with credits, GPA and CGPA, prerequisites, repeats and carry-overs, and attendance eligibility |
| Results | An approval chain with publication locking and controlled amendments |
| Wider campus | Student records, finance, payroll and HR, library, clinic, transport, ID and visitor management, notifications and reports |

## How results are approved

::flow Lecturer enters marks > Head of Department > Dean > Registry > Registrar publishes | Each step reviews and approves, and published results are locked against quiet changes.

## A phased rollout

1. Start with current students and the processes that matter most.
2. Prove it works and train staff.
3. Add the wider campus modules step by step.
4. Migrate old records once the new system is trusted.

> **Watch out:** Rushing a system that holds grades and payments is risky. The plan is deliberately phased so each part is trusted before the next is added.

## Built for the future

The platform is planned to be cloud-hosted, mobile-friendly with a mobile app, ready for more than one campus, with customisable roles and QR-verifiable documents, alongside a separate public website.''')

case(slug='case-this-website', title='This website', status='Built', stage=3, types='it systems', motif='browser', screens_real=True,
     short='A fast, free-to-host personal site with notes, free resources, case studies, offline support and dark mode.',
     desc='Case study: how alhajiimehemoh.github.io is built: a static site generated with Python, hosted free on GitHub Pages, with notes, 17 free resources, case studies, offline support and dark mode.',
     lede='A fast, free-to-host website that works on a basic phone, keeps working offline and turns my notes and templates into something people can use.',
     tools=['Python', 'HTML and CSS', 'JavaScript', 'GitHub Pages', 'PWA'],
     glance=[('40', 'pages generated from source'), ('17', 'free downloadable resources'), ('19', 'practical notes'), ('Free', 'hosting on GitHub Pages')],
     facts=[('Owner', 'Alhaji Ibrahim Mehemoh'), ('My role', 'Planning, writing and direction, built with AI-assisted development'),
            ('Hosting', 'GitHub Pages, free'), ('Audience', 'Employers, NGOs, clients and anyone learning data and IT skills')],
     notes=['note-small-organisation-website', 'note-backup-rule'],
     resources=['dashboard-design-checklist.pdf'],
     body='''## The goal

I wanted one place that shows what I do, proves it with real work and gives something useful away. It had to load quickly on a phone with mobile data, cost nothing to host and be easy to update.

## How it is built

::flow Content in Python and JSON > Build script generates every page > Resources built as PDF and Excel > Pushed to GitHub > Live on GitHub Pages | One build command regenerates the whole site.

- Every page is generated from a small set of source files, so the menu, footer and styles stay consistent.
- Notes are written in a simple text format with tables, checklists, callouts and diagrams.
- The free PDFs and Excel files are generated by code from the same brand template, with formulas checked automatically.

## What it does for visitors

| Feature | Why it matters |
| Fast static pages | Loads quickly on mobile data |
| Works offline | Pages already visited still open without a connection |
| Dark mode and reduced motion | Comfortable to read, respects device settings |
| Free resources | Checklists, templates and trackers anyone can use |
| WhatsApp and quote forms | The quickest ways to reach me |
| Search-friendly structure | Helps people find the notes and services |

## Honest by design

Screens of RHCI projects are clearly labelled as design mockups with sample data, and no real patient or staff information is published. Illustrations are marked as illustrations.

> **Tip:** A small organisation can use the same approach: a few clear pages, free hosting and content that answers real questions.

## Keep improving

The site is updated as new notes, resources and projects are added, and every change is checked on desktop and mobile before it goes live.''')

MORE_WORK = [
    ('Training manual', 'Data analytics and BI for M&E professionals', 'A comprehensive training manual on data analytics and business intelligence for M&E staff.', 'teach'),
    ('Template', 'Weekly data quality check', 'A redesigned Word template with interactive checkboxes for the weekly checks run with my Assistant Data Officer.', 'check'),
    ('Report', 'Procurement projection for CHW supplies', 'A projection report to plan supplies for the community health worker programme.', 'report'),
    ('Certificates', 'CHW home visit training certificates', 'Managed the certificates for community health workers trained in home visits.', 'teach'),
    ('Design', 'Malaria campaign visual assets', 'Banner, cap and polo shirt mockups for a malaria campaign partnership.', 'web'),
    ('Form', 'Contract staff exit clearance form', 'A clear exit clearance form so departing contract staff return equipment and close accounts.', 'office'),
]
