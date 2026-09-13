from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.shapes import MSO_SHAPE
import random
from math import cos, sin, radians

def create_creative_presentation(output_filename):
    # Create presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 aspect ratio
    prs.slide_height = Inches(7.5)

    # ==== SLIDE 1: DYNAMIC TITLE SLIDE (GRADIENT + MODERN TYPOGRAPHY) ====
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank layout

    # Gradient background (dark blue to purple)
    background = slide.background
    fill = background.fill
    fill.gradient()
    fill.gradient_angle = 45
    fill.gradient_stops[0].color.rgb = RGBColor(13, 27, 42)  # Dark blue
    fill.gradient_stops[1].color.rgb = RGBColor(80, 10, 120)  # Purple

    # Main title (modern font styling)
    title = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11), Inches(2))
    tf = title.text_frame
    p = tf.add_paragraph()
    p.text = "INNOVATE. CREATE. ELEVATE."
    p.font.size = Pt(48)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.bold = True
    p.font.name = "Calibri Light"
    p.alignment = PP_ALIGN.CENTER

    # Subtitle with decorative line
    subtitle = slide.shapes.add_textbox(Inches(4), Inches(3.5), Inches(5), Inches(1))
    tf = subtitle.text_frame
    p = tf.add_paragraph()
    p.text = "A FUTURE-READY PRESENTATION"
    p.font.size = Pt(20)
    p.font.color.rgb = RGBColor(200, 200, 255)
    p.alignment = PP_ALIGN.CENTER

    # Add a decorative line under subtitle
    line = slide.shapes.add_shape(MSO_SHAPE.LINE, Inches(4), Inches(4), Inches(5), Inches(0))
    line.line.color.rgb = RGBColor(100, 200, 255)
    line.line.width = Pt(2)

    # Floating abstract shapes (modern design element)
    for i in range(3):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(1 + i*4), Inches(5), Inches(3), Inches(1.5)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(255, 255, 255, 30)  # Semi-transparent
        shape.line.fill.background()
        shape.rotation = -10 if i % 2 else 10  # Slight tilt

    # ==== SLIDE 2: INFOGRAPHIC STYLE (CIRCULAR PROCESS) ====
    slide = prs.slides.add_slide(prs.slide_layouts[5])

    # Light gray background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(240, 240, 240)

    # Title
    title = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(1))
    tf = title.text_frame
    p = tf.add_paragraph()
    p.text = "OUR PROCESS"
    p.font.size = Pt(36)
    p.font.color.rgb = RGBColor(13, 27, 42)
    p.font.bold = True

    # Create a circular process diagram
    center_x, center_y = Inches(6.5), Inches(4)
    radius = Inches(2.5)
    colors = [
        RGBColor(255, 100, 100),  # Red
        RGBColor(100, 200, 255),  # Blue
        RGBColor(150, 255, 150),  # Green
        RGBColor(255, 200, 100)   # Orange
    ]
    
    for i in range(4):
        # Circle segments
        start_angle = i * 90
        end_angle = start_angle + 90
        shape = slide.shapes.add_shape(
            MSO_SHAPE.PIE,
            center_x - radius, center_y - radius,
            radius * 2, radius * 2
        )
        shape.adjustments[0] = start_angle * 60000  # Convert to 1/60000 degrees
        shape.adjustments[1] = end_angle * 60000
        shape.fill.solid()
        shape.fill.fore_color.rgb = colors[i]
        shape.line.fill.background()

        # Labels
        angle = (start_angle + end_angle) / 2
        label_x = center_x + (radius * 0.8) * cos(radians(angle))
        label_y = center_y + (radius * 0.8) * sin(radians(angle))
        label = slide.shapes.add_textbox(label_x - Inches(1), label_y - Inches(0.3), Inches(2), Inches(0.6))
        tf = label.text_frame
        p = tf.add_paragraph()
        p.text = f"Step {i+1}"
        p.font.size = Pt(14)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER

    # ==== SLIDE 3: INTERACTIVE CHART (ANIMATED-STYLE) ====
    slide = prs.slides.add_slide(prs.slide_layouts[5])

    # Dark background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(30, 30, 50)

    # Glowing title effect
    title = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11), Inches(1))
    tf = title.text_frame
    p = tf.add_paragraph()
    p.text = "GROWTH METRICS"
    p.font.size = Pt(40)
    p.font.color.rgb = RGBColor(100, 200, 255)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER

    # 3D-style bar chart
    chart_data = ChartData()
    chart_data.categories = ['2020', '2021', '2022', '2023']
    chart_data.add_series('Revenue', (45, 68, 92, 120))
    
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_STACKED,
        Inches(2), Inches(2), Inches(9), Inches(4.5),
        chart_data
    ).chart

    # Customize chart colors
    series = chart.series[0]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = RGBColor(0, 200, 200)  # Teal

    # Add glow effect (simulated with a white shadow)
    chart.plots[0].has_data_labels = True
    for point in series.points:
        point.data_label.font.size = Pt(14)
        point.data_label.font.color.rgb = RGBColor(255, 255, 255)

    # ==== SLIDE 4: CLOSING SLIDE (CALL-TO-ACTION) ====
    slide = prs.slides.add_slide(prs.slide_layouts[5])

    # Gradient background (purple to blue)
    background = slide.background
    fill = background.fill
    fill.gradient()
    fill.gradient_stops[0].color.rgb = RGBColor(80, 10, 120)
    fill.gradient_stops[1].color.rgb = RGBColor(13, 27, 42)

    # Main message
    title = slide.shapes.add_textbox(Inches(2), Inches(2), Inches(9), Inches(2))
    tf = title.text_frame
    p = tf.add_paragraph()
    p.text = "READY TO INNOVATE?"
    p.font.size = Pt(54)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER

    # CTA Button (simulated with a shape)
    button = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(5), Inches(4.5), Inches(3), Inches(1)
    )
    button.fill.solid()
    button.fill.fore_color.rgb = RGBColor(255, 200, 0)  # Yellow
    button.line.fill.background()

    # Button text
    tf = button.text_frame
    p = tf.add_paragraph()
    p.text = "CONTACT US"
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(0, 0, 0)
    p.alignment = PP_ALIGN.CENTER

    # Final decorative elements (floating dots)
    for _ in range(20):
        x = random.uniform(0.5, 12.5)
        y = random.uniform(1, 6)
        dot = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(x), Inches(y), Inches(0.1), Inches(0.1)
        )
        dot.fill.solid()
        dot.fill.fore_color.rgb = RGBColor(255, 255, 255, 50)  # Semi-transparent
        dot.line.fill.background()

    # Save the presentation
    prs.save(output_filename)
    print(f"✨ Creative PowerPoint generated: {output_filename}")

# Run the generator
create_creative_presentation("Creative_Presentation.pptx")