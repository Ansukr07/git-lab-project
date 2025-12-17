import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURATION ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "ansukumar2111@gmail.com"
SENDER_PASSWORD = "cuofeitzewgxnvaz"  # use Gmail app password

# --- EMAIL SUBJECT ---
subject = "Invitation to Submit a Problem Statement for CodeRed 3.0"

# --- EMAIL BODY (your exact content) ---
body = """\
Dear Team {company_name},

I’m Ansu Kumar, Technical Associate at E-Cell, BMS Institute of Technology and Management. We’re organizing CodeRed 3.0, a 24-hour national-level hackathon on December 12–13, and I’m reaching out to explore a potential partnership and collaboration opportunity with {company_name}.

CodeRed 3.0 brings together some of the brightest and most innovative student developers from across India. Our last edition received 3000+ applications from institutes such as IITs and NITs, and this year we’re hosting 50 elite finalist teams building impactful, real-world solutions.

Through this collaboration, {company_name} can:

● Accelerate research and development by outsourcing a key challenge and receive handful of working prototypes and Fresh Perspectives in just 24 hours. This is a high-reward model for crowdsourcing innovation to meet specific business need.

● It is the perfect way to spot a hidden talent that doesn't show up on a resume. You gain access to top candidates as they tackle your real-world challenges. You get to see their skills, creativity, and performance under the pressure of a 24-hour time constraint.  

● Enhance brand visibility among thousands of aspiring engineers and innovators.

You can learn more about the event at codered.vercel.app.
I’d be happy to schedule a brief 15-minute call at your convenience to explore how we can collaborate effectively.
Looking forward to hearing from you.

Ansu Kumar
Technical Associate, E-Cell
BMS Institute of Technology and Management
+91 9707335878
ansukumar2111@gmail.com
"""

# --- RECIPIENTS (edit this list) ---
recipients = {
    "Ansu": "anznup@gmail.com"
}

# --- SEND EMAIL ---
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        for company, email in recipients.items():
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = email
            msg["Subject"] = subject

            # personalize email with company name
            msg.attach(MIMEText(body.format(company_name=company), "plain"))

            server.sendmail(SENDER_EMAIL, email, msg.as_string())
            print(f"✅ Email sent successfully to {company} ({email})")

except Exception as e:
    print("❌ Error:", e)
