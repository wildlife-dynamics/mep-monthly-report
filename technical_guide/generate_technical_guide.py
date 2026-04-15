"""
Generate the MEP Monthly Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: mep_monthly_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "mep_monthly_report_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"MEP Monthly Report — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("MEP Monthly Report", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Elephant sightings, patrols, collar voltages, and sitrep analysis", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>monthly_report</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>monthly_report</b> workflow fetches data from EarthRanger to "
      "produce the MEP (Mara Elephant Project) Monthly Report. It covers "
      "all events (scatter map coloured by event type), collar GPS speedmaps, "
      "vehicle and foot patrol trajectories, per-subject collar voltage charts, "
      "and a situation report (sitrep). All outputs are assembled into a "
      "populated Word document."),
    sp(4),
    p("The workflow delivers:"),
    bullet("1 events scatter map (all event types, coloured by type via tab20 palette)"),
    bullet("1 elephant GPS speedmap"),
    bullet("1 vehicle patrol trajectories map"),
    bullet("1 foot patrol trajectories map"),
    bullet("Per-subject collar voltage charts (one per collared animal)"),
    bullet("1 sitrep CSV report"),
    bullet("A Word document report — cover page + populated content page"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output type", "Count", "Description"],
            ["Events scatter map",         "1",          "Scatter layer of all events, coloured by event type (tab20)"],
            ["Speedmap",                   "1",          "GPS trajectories coloured by 6-bin speed classification"],
            ["Vehicle patrol map",         "1",          "Vehicle patrol trajectories coloured by team (viridis)"],
            ["Foot patrol map",            "1",          "Foot patrol trajectories coloured by team (viridis)"],
            ["Vehicle patrol GeoParquet",  "1",          "Raw vehicle patrol trajectory data"],
            ["Foot patrol GeoParquet",     "1",          "Raw foot patrol trajectory data"],
            ["Collar voltage charts",      "1 per subject", "Voltage/GPS fix timeline vs previous period"],
            ["Sitrep CSV",                 "1",          "Situation report compiled from EarthRanger events"],
            ["Word report",                "1",          "Cover page + content page merged into final docx"],
        ],
        [4.5*cm, 2.5*cm, W - 7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-workflows-core",        "0.22.17.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-ecoscope","0.22.17.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",  "0.0.40.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",     "0.0.18.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",     "0.0.7.*",   "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-big-life","0.0.8.*",   "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mep",     "0.0.13.*",  "ecoscope-workflows-custom"],
        ],
        [6.5*cm, 3*cm, W - 9.5*cm],
    ),
    sp(6),
    h2("2.2  Connections"),
    make_table(
        [
            ["Connection", "Task", "Purpose"],
            ["EarthRanger", "set_er_connection",
             "Fetch events, subject group observations, "
             "vehicle and foot patrol data, and sitrep events"],
        ],
        [3.5*cm, 4*cm, W - 7.5*cm],
    ),
    sp(6),
    h2("2.3  Dropbox files"),
    p("Two Word template files are downloaded from Dropbox at runtime if not "
      "already present (<b>overwrite_existing: false</b>, retries: 3):"),
    make_table(
        [
            ["File", "Purpose", "Dropbox URL (abbreviated)"],
            ["mep_monthly_report.docx",
             "Word template for the cover page (title, report period, prepared-by field)",
             "dropbox.com/…/mep_monthly_report.docx?rlkey=nbibg8ulnlz0w4q53jw2db6y3"],
            ["mep_monthly_indv_report.docx",
             "Word template for the content page (maps, charts, collar charts, sitrep table)",
             "dropbox.com/…/mep_monthly_indv_report.docx?rlkey=wss0x8sa9i5fgl9yjco7paa03"],
        ],
        [3.5*cm, 5*cm, W - 8.5*cm],
    ),
    sp(6),
    h2("2.4  Base maps"),
    p("Base map tiles are configured by the user via <b>set_base_maps_pydeck</b>. "
      "Any tile layer supported by deck.gl can be specified."),
    sp(6),
    h2("2.5  Grouper"),
    p("The workflow groups all data by <b>name</b> (subject name). "
      "The grouper is fixed to <b>index_name: name</b> — "
      "users cannot change the grouping dimension."),
    sp(6),
    h2("2.6  Subject group"),
    p("A user-provided string parameter (<b>Subject Group Name</b>) is passed "
      "to both the current-period and previous-period observation fetches, and "
      "also included in the Word report content page context. "
      "Every subject in the group receives a collar voltage chart."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. EVENTS PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Events Pipeline"),
    hr(),
    p("All events within the analysis time range are fetched, cleaned, "
      "coloured by event type, and rendered as a scatter map."),
    sp(6),
    h2("3.1  Event retrieval, cleaning, and colourmap"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "get_events",
             "Fetch all events for the analysis time range (no event_type filter). "
             "Columns retained: id, time, event_type, event_category, reported_by, "
             "serial_number, geometry, created_at, event_details. "
             "include_details: true, include_null_geometry: false, "
             "raise_on_empty: true."],
            ["2", "exclude_geom_outliers",
             "Remove spatial outliers using z_threshold: 3 (flags points more than "
             "3 standard deviations from the centroid)."],
            ["3", "drop_null_geometry",
             "Drop any rows with null geometry after outlier removal."],
            ["4", "apply_color_map",
             "Apply the tab20 palette to the event_type column, writing colours "
             "to the output column event_type_colors. Each distinct event type "
             "receives a unique colour from the tab20 palette."],
        ],
        [1.2*cm, 4*cm, W - 5.2*cm],
    ),
    sp(6),
    h2("3.2  Events scatter map"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Layer type",         "create_scatterplot_layer"],
            ["Fill color",         "event_type_colors (tab20, dynamic per event type)"],
            ["Line color",         "event_type_colors (same column)"],
            ["Line width",         "0.55"],
            ["Radius",             "3.55 m"],
            ["Opacity",            "0.75"],
            ["Stroked",            "true"],
            ["Legend title",       "Legend"],
            ["Legend label column","event_type"],
            ["Legend color column","event_type_colors"],
            ["Max zoom",           "10"],
            ["Screenshot timeout", "40 000 ms (map tile rendering)"],
        ],
        [5*cm, W - 5*cm],
    ),
    p("The map HTML is persisted as <b>elephant_sightings_map.html</b> then "
      "converted to PNG with device_scale_factor: 2.0."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. SUBJECT GPS SPEEDMAP PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Subject GPS Speedmap Pipeline"),
    hr(),
    p("Collar GPS relocations for the subject group are converted to "
      "trajectories and coloured by speed to produce an overall speedmap."),
    sp(6),
    h2("4.1  Observations and relocations"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "get_subjectgroup_observations",
             "Fetch observations for the analysis period (filter: clean, "
             "include_details: true, include_subjectsource_details: true, "
             "raise_on_empty: false)."],
            ["2", "process_relocations",
             "Retain 12 columns: groupby_col, fixtime, junk_status, geometry, "
             "extra__subject__name, extra__subject__hex, extra__subject__sex, "
             "extra__created_at, extra__subject__subject_subtype, "
             "extra__subjectsource__id, extra__subjectsource__assigned_range, "
             "extra__observation_details. "
             "Filter 3 invalid coordinate pairs: (180,90), (0,0), (1,1)."],
        ],
        [1.2*cm, 4*cm, W - 5.2*cm],
    ),
    sp(6),
    h2("4.2  Previous period observations"),
    p("A parallel fetch retrieves observations for the <b>previous period</b> "
      "(computed via <b>get_previous_period</b>) using identical parameters. "
      "Both current and previous observations are passed to "
      "<b>process_collar_voltage_charts</b> to generate per-subject collar "
      "voltage and GPS fix-rate plots that compare the current and prior periods."),
    sp(6),
    h2("4.3  Trajectory segment filter"),
    make_table(
        [
            ["Parameter", "Value", "Description"],
            ["min_length_meters", "0.001", "Minimum segment length"],
            ["max_length_meters", "5 000", "Maximum segment length"],
            ["min_time_secs",     "1",     "Minimum time between fixes"],
            ["max_time_secs",     "21 600","Maximum time (~6 hours)"],
            ["min_speed_kmhr",    "0.01",  "Minimum plausible speed"],
            ["max_speed_kmhr",    "9",     "Maximum plausible speed"],
        ],
        [4.5*cm, 2.5*cm, W - 7*cm],
    ),
    sp(6),
    h2("4.4  Speed classification and colormap"),
    p("After adding a temporal index (time_col: segment_start), speed is "
      "classified into <b>6 equal-interval bins</b> with label_ranges: true, "
      "label_decimals: 1, label_suffix: ' km/h'. Trajectories are sorted "
      "ascending by speed bin then coloured using the following ramp:"),
    make_table(
        [
            ["Bin", "Hex color", "Description"],
            ["1 (slowest)", "#1a9850", "Dark green"],
            ["2",           "#91cf60", "Light green"],
            ["3",           "#d9ef8b", "Yellow-green"],
            ["4",           "#fee08b", "Light amber"],
            ["5",           "#fc8d59", "Orange"],
            ["6 (fastest)", "#d73027", "Red"],
        ],
        [3*cm, 3*cm, W - 6*cm],
    ),
    sp(6),
    h2("4.5  Speedmap layer and map"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Layer type",        "create_path_layer"],
            ["Color column",      "speed_bins_colormap"],
            ["Width",             "2.85, width_units: pixels, min 2 / max 8 px"],
            ["Cap / joint",       "rounded, billboard: false"],
            ["Opacity",           "0.55"],
            ["Legend",            "Speed (km/h), sorted ascending"],
            ["Max zoom",          "10"],
            ["Screenshot timeout","40 000 ms"],
        ],
        [5*cm, W - 5*cm],
    ),
    p("Columns retained for the map layer: dist_meters, speed_bins_colormap, "
      "geometry, speed_kmhr, speed_bins. The HTML is persisted with "
      "filename_suffix: speedmap then converted to PNG."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. VEHICLE PATROL PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Vehicle Patrol Pipeline"),
    hr(),
    p("Vehicle patrol observations are fetched from EarthRanger, converted to "
      "trajectories, and rendered as a map coloured by patrol team."),
    sp(6),
    h2("5.1  Patrol retrieval"),
    p("Task: <b>get_patrol_observations</b> with parameters: "
      "include_patrol_details: true, raise_on_empty: true, sub_page_size: 100, "
      "patrols_overlap_daterange: true. No patrol_type filter is applied — "
      "all vehicle patrol types present in EarthRanger for the time range "
      "are included."),
    sp(6),
    h2("5.2  Relocations"),
    p("Task: <b>process_relocations</b>. Columns retained: patrol_id, "
      "patrol_start_time, patrol_end_time, geometry, patrol_type__value, "
      "patrol_type__display, patrol_serial_number, patrol_status, "
      "patrol_subject, groupby_col, fixtime, junk_status, extra__source. "
      "Invalid coordinate pairs (180,90), (0,0), (1,1) are filtered."),
    sp(6),
    h2("5.3  Trajectory segment filter"),
    make_table(
        [
            ["Parameter", "Value"],
            ["min_length_meters", "0.35"],
            ["max_length_meters", "5 000"],
            ["min_time_secs",     "1"],
            ["max_time_secs",     "18 000 (~5 hours)"],
            ["min_speed_kmhr",    "10"],
            ["max_speed_kmhr",    "100"],
        ],
        [5*cm, W - 5*cm],
    ),
    note("The minimum speed of 10 km/h filters out stationary periods and slow "
         "foot movement, retaining only motorised patrol segments."),
    sp(6),
    h2("5.4  Colormap and map layer"),
    p("Trajectories are coloured by <b>extra__patrol_type__value</b> using the "
      "<b>viridis</b> colormap (task: apply_color_map, output_column: "
      "patrol_type_colormap). A path layer is created with the same style "
      "as the speedmap (width 2.85, opacity 0.55, rounded). Legend title: "
      "<i>Patrol team</i>, sorted ascending."),
    sp(6),
    h2("5.5  Persistence"),
    p("Trajectories are persisted as <b>vehicle_patrol_trajectories.geoparquet</b>. "
      "The map HTML is persisted as <b>vehicle_patrols_map.html</b> then "
      "converted to PNG with a 40 000 ms screenshot timeout."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. FOOT PATROL PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Foot Patrol Pipeline"),
    hr(),
    p("The foot patrol pipeline mirrors the vehicle patrol pipeline but uses "
      "different trajectory thresholds appropriate for walking speeds. "
      "No patrol_type filter is applied — all foot patrol types present "
      "in EarthRanger for the time range are included."),
    sp(6),
    h2("6.1  Trajectory segment filter"),
    make_table(
        [
            ["Parameter", "Value"],
            ["min_length_meters", "0.001"],
            ["max_length_meters", "5 000"],
            ["min_time_secs",     "1"],
            ["max_time_secs",     "14 400 (~4 hours)"],
            ["min_speed_kmhr",    "0.5"],
            ["max_speed_kmhr",    "9"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("6.2  Colormap, map layer, and persistence"),
    p("Identical to the vehicle patrol pipeline: viridis colormap on "
      "extra__patrol_type__value, path layer with legend <i>Patrol team</i>. "
      "Trajectories persisted as <b>foot_patrol_trajectories.geoparquet</b>, "
      "map as <b>foot_patrols_map.html</b> → PNG (40 000 ms timeout)."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. SITREP PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Sitrep (Situation Report) Pipeline"),
    hr(),
    p("The workflow compiles a situation report from EarthRanger events "
      "configured by a region column lookup."),
    sp(6),
    h2("7.1  Configuration and compilation"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "get_sitrep_event_config",
             "Retrieves the sitrep event type configuration keyed by "
             "region_column: 'region'. Returns an event_details mapping "
             "used to categorise events by region."],
            ["2", "compile_sitrep",
             "Fetches and aggregates EarthRanger events for the analysis "
             "time range using the event_details configuration. Produces "
             "a summary DataFrame of incident counts and categories per region."],
            ["3", "persist_df",
             "Saves the sitrep DataFrame as <b>sitrep_report.csv</b> to "
             "ECOSCOPE_WORKFLOWS_RESULTS. Skipped if the result is empty or "
             "a dependency was skipped."],
        ],
        [1.2*cm, 4*cm, W - 5.2*cm],
    ),
    sp(6),
    note("The sitrep CSV is passed directly to create_mep_monthly_context "
         "for inclusion in the Word report's content page."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. COLLAR VOLTAGE CHARTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Collar Voltage Charts"),
    hr(),
    p("Per-subject collar voltage and GPS fix-rate charts are produced using "
      "a single compound task that handles all subjects in the group."),
    sp(6),
    make_table(
        [
            ["Parameter", "Value"],
            ["task",             "process_collar_voltage_charts"],
            ["relocs",           "Current-period subject observations (raw, not processed)"],
            ["previous_relocs",  "Previous-period subject observations"],
            ["time_range",       "Analysis time range"],
            ["output_dir",       "ECOSCOPE_WORKFLOWS_RESULTS"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(4),
    p("The task returns a list of HTML file paths — one chart file per collared "
      "subject. These are passed to <b>html_to_png</b> (wait_for_timeout: 10 ms, "
      "device_scale_factor: 2.0, max_concurrent_pages: 1) to produce PNG files "
      "for inclusion in the Word report."),
    note("process_collar_voltage_charts receives the raw observations "
         "DataFrames (not the processed relocations GeoDataFrame), as it "
         "requires the original voltage and transmission metadata columns."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. WORD REPORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Word Report"),
    hr(),
    p("Two Word document templates are downloaded from Dropbox and populated "
      "with all computed outputs to produce the final MEP Monthly Report."),
    sp(6),
    h2("9.1  Cover page"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download mep_monthly_report.docx from Dropbox."],
            ["2", "create_monthly_ctx_cover",
             "Create cover context: report_period from analysis time range, "
             "prepared_by: 'Ecoscope'."],
            ["3", "create__mep_context_page",
             "Populate the cover template with the context. "
             "Output filename: mep_cover_page.docx."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("9.2  Content page"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download mep_monthly_indv_report.docx from Dropbox."],
            ["2", "create_mep_monthly_context",
             "Populate the content template with: elephant_sightings_map_path, "
             "speedmap_path, foot_patrols_map_path, vehicle_patrol_map_path, "
             "subject_group (subject group name string), "
             "collared_elephant_plot_paths (list), sitrep_df_path. "
             "Output filename: mep_context.docx."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("9.3  Merge"),
    p("Task: <b>merge_mapbook_files</b>. The cover page "
      "(<b>mep_cover_page.docx</b>) and content page (<b>mep_context.docx</b>) "
      "are merged into <b>overall_mep_monthly_report.docx</b> saved to "
      "ECOSCOPE_WORKFLOWS_RESULTS."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Output Files"),
    hr(),
    p("All outputs are written to the directory specified by "
      "<b>ECOSCOPE_WORKFLOWS_RESULTS</b>. Files marked with <i>&lt;subject&gt;</i> "
      "are produced once per collared subject."),
    make_table(
        [
            ["File", "Description"],
            ["elephant_sightings_map.html / .png",
             "Scatter map of all events, coloured by event type (tab20)"],
            ["speedmap.html / .png",
             "GPS trajectories coloured by 6-bin speed classification"],
            ["vehicle_patrols_map.html / .png",
             "Vehicle patrol trajectories coloured by team (viridis)"],
            ["foot_patrols_map.html / .png",
             "Foot patrol trajectories coloured by team (viridis)"],
            ["vehicle_patrol_trajectories.geoparquet",
             "Raw vehicle patrol trajectory GeoDataFrame"],
            ["foot_patrol_trajectories.geoparquet",
             "Raw foot patrol trajectory GeoDataFrame"],
            ["sitrep_report.csv",
             "Situation report: incident counts and categories by region"],
            ["<subject>_collar_voltage.html / .png",
             "Collar voltage and GPS fix-rate chart (current vs previous period)"],
            ["mep_cover_page.docx",
             "Populated Word cover page (report period, prepared by)"],
            ["mep_context.docx",
             "Populated Word content page (maps, charts, sitrep)"],
            ["overall_mep_monthly_report.docx",
             "Final merged Word report (cover + content)"],
        ],
        [6.5*cm, W - 6.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Workflow Execution Logic"),
    hr(),
    h2("11.1  Global skip conditions"),
    p("Most tasks carry the following default skipif block "
      "(<b>task-instance-defaults</b>):"),
    make_table(
        [
            ["Condition", "Behaviour"],
            ["any_is_empty_df",       "Skip task if any input DataFrame is empty"],
            ["any_dependency_skipped","Skip task if any upstream dependency was skipped"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("11.2  Screenshot timing"),
    make_table(
        [
            ["Map / chart", "wait_for_timeout", "Reason"],
            ["Events scatter map",   "40 000 ms", "Tile map — waits for base tile rendering"],
            ["Speedmap",             "40 000 ms", "Tile map — waits for base tile rendering"],
            ["Vehicle patrol map",   "40 000 ms", "Tile map — waits for base tile rendering"],
            ["Foot patrol map",      "40 000 ms", "Tile map — waits for base tile rendering"],
            ["Collar voltage charts","10 ms",     "Static Plotly HTML — no tiles"],
        ],
        [4.5*cm, 3*cm, W - 7.5*cm],
    ),
    sp(6),
    h2("11.3  Dashboard"),
    p("The workflow concludes with <b>gather_dashboard</b> which packages "
      "workflow details, time range, and groupers into a dashboard record. "
      "The <b>widgets</b> list is currently empty — no single-value or map "
      "widgets are configured for this workflow."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 12. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("12. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned in spec.yaml"],
            ["ecoscope-workflows-core",        "0.22.17.*"],
            ["ecoscope-workflows-ext-ecoscope","0.22.17.*"],
            ["ecoscope-workflows-ext-custom",  "0.0.40.*"],
            ["ecoscope-workflows-ext-ste",     "0.0.18.*"],
            ["ecoscope-workflows-ext-mnc",     "0.0.7.*"],
            ["ecoscope-workflows-ext-big-life","0.0.8.*"],
            ["ecoscope-workflows-ext-mep",     "0.0.13.*"],
        ],
        [7*cm, W - 7*cm],
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF written → {OUTPUT_FILE}")
