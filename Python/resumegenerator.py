# Creating a sample resume PDF for model testing.
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import textwrap
from pathlib import Path

output_path = r"C:\Users\SHIVANSH\Desktop\example_resume.pdf"  # adjust if needed
output_path = Path(output_path).resolve()
c = canvas.Canvas(str(output_path), pagesize=A4)
width, height = A4

# Helper to draw wrapped text
def draw_wrapped_text(c, x, y, text, max_width, leading=12, font="Helvetica", font_size=10):
    c.setFont(font, font_size)
    wrapper = textwrap.TextWrapper(width=100)
    lines = []
    for paragraph in text.split("\n"):
        # approximate wrap by characters per line based on font size and max_width
        approx_chars = int(max_width / (font_size * 0.55))
        wrapper.width = approx_chars
        wrapped = wrapper.wrap(paragraph)
        if not wrapped:
            lines.append("")
        else:
            lines.extend(wrapped)
    textobj = c.beginText(x, y)
    textobj.setLeading(leading)
    for line in lines:
        textobj.textLine(line)
    c.drawText(textobj)
    return y - leading * len(lines)

# Header
c.setFont("Helvetica-Bold", 20)
c.drawString(2*cm, height - 2*cm, "ALEXANDER R. SAMPLE")
c.setFont("Helvetica", 11)
c.drawString(2*cm, height - 2.7*cm, "Software Engineer • Full‑Stack Developer • Open‑Source Enthusiast")
c.setStrokeColorRGB(0.2,0.2,0.2)
c.setLineWidth(0.5)
c.line(2*cm, height - 3*cm, width - 2*cm, height - 3*cm)

# Left column (contact + skills)
left_x = 2*cm
right_x = width/2 + 0.2*cm
y = height - 3.6*cm

# Contact
c.setFont("Helvetica-Bold", 12)
c.drawString(left_x, y, "Contact")
c.setFont("Helvetica", 10)
y -= 0.5*cm
c.drawString(left_x, y, "Email: alex.sample@example.com")
y -= 0.4*cm
c.drawString(left_x, y, "Phone: +1 (555) 123-4567")
y -= 0.4*cm
c.drawString(left_x, y, "Location: San Francisco, CA")
y -= 0.6*cm

# Skills
c.setFont("Helvetica-Bold", 12)
c.drawString(left_x, y, "Skills")
c.setFont("Helvetica", 10)
y -= 0.5*cm
skills = ["Python", "JavaScript (React/Node)", "Docker & Kubernetes", "PostgreSQL", "CI/CD", "AWS"]
for s in skills:
    c.drawString(left_x + 6, y, "• " + s)
    y -= 0.4*cm

# Education
y -= 0.2*cm
c.setFont("Helvetica-Bold", 12)
c.drawString(left_x, y, "Education")
c.setFont("Helvetica", 10)
y -= 0.5*cm
c.drawString(left_x + 6, y, "M.S. Computer Science, Stanford University — 2018")
y -= 0.4*cm
c.drawString(left_x + 6, y, "B.S. Computer Science, University of Illinois — 2016")

# Right column (summary + experience + projects)
y_right = height - 3.6*cm
c.setFont("Helvetica-Bold", 12)
c.drawString(right_x, y_right, "Professional Summary")
c.setFont("Helvetica", 10)
y_right -= 0.6*cm
summary = ("Practical full-stack engineer with 6+ years building scalable web applications and APIs. "
           "Comfortable leading small teams, designing distributed systems, and improving developer workflows. "
           "Passionate about clean code, automated testing, and developer experience.")
y_right = draw_wrapped_text(c, right_x, y_right, summary, max_width=width-right_x-2*cm, leading=13, font_size=10)

# Experience
y_right -= 0.4*cm
c.setFont("Helvetica-Bold", 12)
c.drawString(right_x, y_right, "Experience")
c.setFont("Helvetica-Bold", 10)
y_right -= 0.6*cm
c.drawString(right_x, y_right, "Senior Software Engineer — Nimbus Labs")
c.setFont("Helvetica", 10)
c.drawString(right_x + 6, y_right, "Jan 2021 — Present")
y_right -= 0.5*cm
exp1 = ("Led development of a microservices-based analytics platform handling 500k+ events/day. "
        "Built RESTful APIs, migrated services to Kubernetes, and introduced end-to-end testing which reduced regressions by 35%.")
y_right = draw_wrapped_text(c, right_x + 6, y_right, exp1, max_width=width-right_x-2.5*cm, leading=12, font_size=10)

y_right -= 0.4*cm
c.setFont("Helvetica-Bold", 10)
c.drawString(right_x, y_right, "Software Engineer — BrightApps")
c.setFont("Helvetica", 10)
c.drawString(right_x + 6, y_right, "Jul 2018 — Dec 2020")
y_right -= 0.5*cm
exp2 = ("Built single-page applications with React and complex backend services in Python. "
        "Improved page load performance by 40% and led adoption of feature flags across multiple squads.")
y_right = draw_wrapped_text(c, right_x + 6, y_right, exp2, max_width=width-right_x-2.5*cm, leading=12, font_size=10)

# Projects
y_right -= 0.4*cm
c.setFont("Helvetica-Bold", 12)
c.drawString(right_x, y_right, "Selected Projects")
c.setFont("Helvetica-Bold", 10)
y_right -= 0.6*cm
c.drawString(right_x, y_right, "OpenMetrics · GitHub")
y_right -= 0.4*cm
proj1 = ("An open-source metrics collector and dashboard. Responsible for core ingestion pipeline and exporter adapters.")
y_right = draw_wrapped_text(c, right_x + 6, y_right, proj1, max_width=width-right_x-2.5*cm, leading=12, font_size=10)

y_right -= 0.4*cm
c.setFont("Helvetica-Bold", 10)
c.drawString(right_x, y_right, "Resume Website Generator — Personal")
y_right -= 0.4*cm
proj2 = ("A generator that turns structured resume data into a responsive HTML/CSS site with PDF export.")
y_right = draw_wrapped_text(c, right_x + 6, y_right, proj2, max_width=width-right_x-2.5*cm, leading=12, font_size=10)

# Footer
c.setFont("Helvetica-Oblique", 9)
c.drawCentredString(width/2, 1.5*cm, "This is a sample resume PDF generated for model testing purposes.")

c.showPage()
c.save()

print("Created:", output_path)
