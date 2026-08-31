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
    bullet("1 events scatter map (all event types, coloured by type via tab20 palette) + 1 events CSV export"),
    bullet("1 elephant GPS speedmap"),
    bullet("1 vehicle patrol trajectories map"),
    bullet("1 foot patrol trajectories map"),
    bullet("Per-subject historic voltage charts — current voltage vs. a previous-period min/mean/max band"),
    bullet("1 sitrep report — CSV export plus a sortable/filterable dashboard table"),
    bullet("An interactive dashboard — 6 widgets: Collar Voltage, Elephant Sightings Map, Speed Map, "
           "Vehicle Patrols Map, Foot Patrols Map, Sitrep Report"),
    bullet("A Word document report (overall_report.docx) — every map, chart, and the sitrep table"),
    bullet("A separate Word cover page — MEP logo (auto-downloaded), report period, prepared-by"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output type", "Count", "Description"],
            ["Events CSV",                 "1",          "All fetched events with event_details flattened into columns"],
            ["Events scatter map",         "1",          "Scatter layer of all events, coloured by event type (tab20)"],
            ["Speedmap",                   "1",          "GPS trajectories coloured by 6-bin speed classification"],
            ["Vehicle patrol map",         "1",          "Vehicle patrol trajectories coloured by team (viridis)"],
            ["Foot patrol map",            "1",          "Foot patrol trajectories coloured by team (viridis)"],
            ["Vehicle patrol GeoParquet",  "1",          "Raw vehicle patrol trajectory data"],
            ["Foot patrol GeoParquet",     "1",          "Raw foot patrol trajectory data"],
            ["Relocations GeoParquet",     "2",          "Current-period and previous-period relocations, each with extracted voltage"],
            ["Historic voltage charts",    "1 per subject", "Current voltage vs. previous-period min/mean/max band"],
            ["Sitrep report",              "1",          "CSV export + sortable/filterable dashboard table"],
            ["Dashboard widgets",          "6",          "Collar Voltage, Sightings, Speed, Vehicle, Foot, Sitrep"],
            ["Word report",                "1",          "Content report (overall_report.docx), all maps/charts/sitrep"],
            ["Word cover page",            "1",          "Separate document — MEP logo, report period, prepared-by"],
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
            ["ecoscope-platform",              ">=2.15.0, <2.16.0", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",  "0.1.0rc14.*",       "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",     "0.0.0rc1.*",        "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mep",     "1.0.1.*",           "ecoscope-workflows-custom"],
            ["pydeck",                         "0.9.2",             "conda-forge"],
            ["opentelemetry-sdk",              ">=1.20.0, <2.0.0",  "conda-forge"],
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
    p("All events within the analysis time range are fetched, normalized, "
      "coloured by event type, and rendered as a scatter map."),
    sp(6),
    h2("3.1  Event retrieval, normalization, and colourmap"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "get_events",
             "Fetch all events for the analysis time range (no event_type filter). "
             "Columns retained: id, time, event_type, event_category, reported_by, "
             "serial_number, geometry, created_at, event_details. "
             "include_details: true, include_null_geometry: false, "
             "force_point_geometry: true, raise_on_empty: true."],
            ["2", "normalize_json_column",
             "Flatten the event_details JSON column into top-level columns "
             "(skip_if_not_exists: true, sort_columns: true)."],
            ["3", "persist_df",
             "Persist the normalized events as events.csv to ECOSCOPE_WORKFLOWS_RESULTS."],
            ["4", "apply_color_map",
             "Apply the tab20 palette to the event_type column, writing colours "
             "to the output column event_type_colors. Each distinct event type "
             "receives a unique colour from the tab20 palette."],
        ],
        [1.2*cm, 4*cm, W - 5.2*cm],
    ),
    note("Spatial-outlier exclusion and null-geometry dropping (previously "
         "exclude_geom_outliers / drop_null_geometry) are no longer part of "
         "this pipeline — events are fetched with force_point_geometry: true "
         "and mapped directly."),
    sp(6),
    h2("3.2  Events scatter map"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Layer type",         "ecoscope_workflows_ext_custom.tasks.results.create_scatterplot_layer"],
            ["Fill color",         "event_type_colors (tab20, dynamic per event type)"],
            ["Line color",         "event_type_colors (same column)"],
            ["Line width",         "0.55"],
            ["Radius",             "3.55 m"],
            ["Opacity",            "0.55"],
            ["Stroked",            "true"],
            ["Legend title",       "Legend"],
            ["Legend label column","event_type"],
            ["Legend color column","event_type_colors"],
            ["View state",         "compute_view_state_from_gdf (ext_ste), max_zoom: 15"],
            ["Draw task",          "ecoscope_workflows_ext_custom.tasks.results.draw_map"],
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
             "Fetch observations for the current time range (filter: clean, "
             "include_details: true, include_subjectsource_details: true, "
             "raise_on_empty: false)."],
            ["2", "get_timezone_from_time_range → convert_values_to_timezone",
             "Convert the fixtime column to the analysis timezone."],
            ["3", "process_relocations",
             "Retain 12 columns: groupby_col, fixtime, junk_status, geometry, "
             "extra__subject__name, extra__subject__hex, extra__subject__sex, "
             "extra__created_at, extra__subject__subject_subtype, "
             "extra__subjectsource__id, extra__subjectsource__assigned_range, "
             "extra__observation_details. "
             "Filter 3 invalid coordinate pairs: (180,90), (0,0), (1,1)."],
            ["4", "sort_values → persist_df",
             "Sort by fixtime ascending, then persist as GeoParquet "
             "(relocations.parquet). This sorted GeoDataFrame feeds both the "
             "trajectory/speedmap pipeline below and the historic voltage "
             "pipeline in Section 8."],
        ],
        [1.2*cm, 4*cm, W - 5.2*cm],
    ),
    sp(6),
    h2("4.2  Previous period observations"),
    p("A parallel fetch retrieves observations for a user-configurable "
      "<b>Previous Period</b> (via "
      "ecoscope_workflows_ext_ste.tasks.filter.flexible_previous_period — "
      "Custom offset, a Preset lookback, or an exact Calendar date), processed "
      "identically (timezone conversion, process_relocations, sort, persist "
      "as previous_period_relocations.parquet). See Section 8 for how the "
      "current and previous relocation sets are combined into the historic "
      "voltage charts."),
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
            ["Column filter",     "subset_columns (was: filter_df_cols), exclude: null, strict: false"],
            ["Layer type",        "ecoscope_workflows_ext_custom.tasks.results.create_path_layer"],
            ["Color column",      "speed_bins_colormap"],
            ["Width",             "2.85, width_units: pixels, min 2 / max 8 px"],
            ["Cap / joint",       "rounded, billboard: false"],
            ["Opacity",           "0.55"],
            ["Legend",            "Speed (km/h), sorted ascending"],
            ["View state",        "compute_view_state_from_gdf (ext_ste), max_zoom: 15"],
            ["Draw task",         "ecoscope_workflows_ext_custom.tasks.results.draw_map"],
            ["Max zoom",          "10"],
            ["Screenshot timeout","40 000 ms"],
        ],
        [5*cm, W - 5*cm],
    ),
    p("Columns retained for the map layer: dist_meters, speed_bins_colormap, "
      "geometry, speed_kmhr, speed_bins. The HTML is persisted as "
      "<b>elephant_speedmap.html</b> (filename_suffix: null) then converted to PNG."),
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
      "patrol_type_colormap). A path layer is created via "
      "<b>ecoscope_workflows_ext_custom.tasks.results.create_path_layer</b> "
      "with the same style as the speedmap (width 2.85, opacity 0.55, "
      "rounded). View state comes from "
      "<b>ecoscope_workflows_ext_ste.tasks.spatial_operations."
      "compute_view_state_from_gdf</b> (max_zoom: 15), and the map is drawn "
      "via <b>ecoscope_workflows_ext_custom.tasks.results.draw_map</b>. "
      "Legend title: <i>Patrol team</i>, sorted ascending."),
    sp(6),
    h2("5.5  Persistence"),
    p("Trajectories are persisted as <b>vehicle_patrol_trajectories.geoparquet</b>. "
      "The map HTML is persisted as <b>vehicle_patrols_map.html</b> "
      "(filename_suffix: null) then converted to PNG with a 40 000 ms "
      "screenshot timeout."),
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
    p("Identical to the vehicle patrol pipeline (same renamespaced "
      "create_path_layer / draw_map / compute_view_state_from_gdf tasks): "
      "viridis colormap on extra__patrol_type__value, path layer with legend "
      "<i>Patrol team</i>. Trajectories persisted as "
      "<b>foot_patrol_trajectories.geoparquet</b>, map as "
      "<b>foot_patrols_map.html</b> (filename_suffix: null) → PNG "
      "(40 000 ms timeout)."),
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
    h2("7.2  Dashboard table"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "draw_table",
             "Render the sitrep DataFrame as a sortable, filterable table "
             "(enable_sorting: true, enable_filtering: true, "
             "enable_download: false, widget_id: 'Sitrep Report')."],
            ["2", "persist_text",
             "Persist the rendered table HTML as sitrep_report_table.html."],
            ["3", "create_table_widget_single_view",
             "Wrap the table HTML as the 'Sitrep Report' dashboard widget."],
        ],
        [1.2*cm, 4*cm, W - 5.2*cm],
    ),
    note("The sitrep CSV (sitrep_report.csv) is picked up by filename when "
         "create_mep_monthly_report scans ECOSCOPE_WORKFLOWS_RESULTS for "
         "inclusion in the Word report's content — see Section 9.2 — while "
         "the sitrep table above feeds the dashboard independently."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. COLLAR VOLTAGE CHARTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Collar Voltage Charts"),
    hr(),
    p("The single compound task previously used here "
      "(process_collar_voltage_charts) has been replaced by an explicit, "
      "reusable per-step pipeline shared with the standalone collar/source "
      "voltage workflows, built on the sorted, timezone-converted current "
      "and previous relocation GeoDataFrames from Section 4."),
    sp(6),
    h2("8.1  Voltage extraction"),
    p("Both relocation sets go through <b>extract_value_from_json_column</b> "
      "against their <b>observation_details</b> column, producing a float "
      "<b>voltage</b> column:"),
    make_table(
        [
            ["Parameter", "Value"],
            ["column_name",        "observation_details"],
            ["field_name_options", "battery, mainVoltage, batt, power (checked in this order)"],
            ["output_type",        "float"],
            ["output_column_name", "voltage"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("8.2  Per-subject fan-out"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "split_groups",
             "Split current and previous relocations by the configured grouper (name)"],
            ["2", "column_first_unique_value",
             "Get each subject's display name from the current-period slice"],
            ["3", "safe_string (ext_ste)",
             "Sanitize the subject name for use in a filename"],
            ["4", "prefix_string_var",
             "Build the chart filename: <safe_subject_name>_historic_voltage.html"],
            ["5", "groupbykey",
             "Pair each subject's current-period slice with its previous-period "
             "slice (zip_current_prev_name)"],
        ],
        [1.2*cm, 3.5*cm, W - 4.7*cm],
    ),
    sp(6),
    h2("8.3  Plotting"),
    p("<b>plot_historic_voltage</b> (column: voltage) draws the subject's "
      "current voltage series against a band built from the previous "
      "period's 2.5th/97.5th percentile and mean. If the previous-period "
      "slice is missing or empty, the current period's own values are used "
      "for the band instead. If the computed band collapses to a single "
      "value, it is widened by ±2.5% so the shaded region remains visible."),
    sp(6),
    h2("8.4  Persisting, widget, and PNG"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "groupbykey",
             "Pair each chart's filename with its rendered HTML "
             "(historic_voltage_text); skipped if any dependency was skipped "
             "or any keyed pair is a skip (any_keyed_iterables_are_skips, "
             "unpack_depth: 1)"],
            ["2", "persist_text",
             "Write the chart HTML to ECOSCOPE_WORKFLOWS_RESULTS "
             "(filename_suffix: null — the filename built in 8.2 is used verbatim)"],
            ["3", "create_map_widget_single_view",
             "Title: 'Collar Voltage'; skipif: never, so a widget is always "
             "created even if the underlying chart data is empty"],
            ["4", "merge_widget_views",
             "Merge every subject's widget into a single dashboard widget"],
            ["5", "html_to_png",
             "device_scale_factor: 2.0, wait_for_timeout: 10 ms, "
             "max_concurrent_pages: 1, full_page: false"],
        ],
        [1.2*cm, 3.5*cm, W - 4.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. WORD REPORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Word Report"),
    hr(),
    p("The cover page and the content report are now two separate final "
      "documents — there is no longer a merge step producing a single "
      "combined file."),
    sp(6),
    h2("9.1  Cover page"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download mep_monthly_report.docx (cover template) from Dropbox."],
            ["2", "ecoscope_workflows_ext_ste.tasks.io.fetch_and_persist_file",
             "Download the MEP organisation logo (MEP-logo-dark-linear.png) "
             "from Dropbox — always applied, not user-configurable "
             "(overwrite_existing: false, retries: 2)."],
            ["3", "prepare_cover_metadata",
             "Build the cover context: org_logo_path (from step 2), "
             "report_period (analysis time range), prepared_by: 'Ecoscope', "
             "extra_fields: null, time_generated_format: '%Y-%m-%d %H:%M:%S'."],
            ["4", "create_context_page",
             "Populate the cover template with the context. skipif: "
             "any_dependency_skipped (unpack_depth: 1). Output filename: "
             "mep_monthly_cover_page.docx."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("9.2  Content report"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download mep_monthly_indv_report.docx (content template) from Dropbox."],
            ["2", "create_mep_monthly_report",
             "Takes only template_path and output_dir — no explicit chart/CSV "
             "paths. It walks ECOSCOPE_WORKFLOWS_RESULTS and classifies files "
             "by their known filename stems: elephant_speedmap, "
             "elephant_sightings_map, vehicle_patrols_map, foot_patrols_map "
             "(single images), any <subject>_historic_voltage image (grouped "
             "by subject, suffix stripped), and sitrep_report.csv (rendered "
             "as the sitrep table). Output filename: overall_report.docx."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    note("Because the content report is assembled by scanning "
         "ECOSCOPE_WORKFLOWS_RESULTS for these specific filenames rather than "
         "receiving explicit paths, renaming any upstream persist_text / "
         "persist_df filename above will silently drop that chart or table "
         "from the report instead of raising an error."),
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
            ["events.csv",
             "All fetched events with event_details flattened into columns"],
            ["elephant_sightings_map.html / .png",
             "Scatter map of all events, coloured by event type (tab20)"],
            ["elephant_speedmap.html / .png",
             "GPS trajectories coloured by 6-bin speed classification"],
            ["vehicle_patrols_map.html / .png",
             "Vehicle patrol trajectories coloured by team (viridis)"],
            ["foot_patrols_map.html / .png",
             "Foot patrol trajectories coloured by team (viridis)"],
            ["vehicle_patrol_trajectories.geoparquet",
             "Raw vehicle patrol trajectory GeoDataFrame"],
            ["foot_patrol_trajectories.geoparquet",
             "Raw foot patrol trajectory GeoDataFrame"],
            ["relocations.parquet",
             "All subjects' current-period relocations, including extracted voltage"],
            ["previous_period_relocations.parquet",
             "All subjects' previous-period relocations, including extracted voltage"],
            ["<subject>_historic_voltage.html / .png",
             "Historic voltage chart — current voltage vs. previous-period min/mean/max band"],
            ["sitrep_report.csv",
             "Situation report: incident counts and categories by region"],
            ["sitrep_report_table.html",
             "Sitrep report rendered as a sortable/filterable table (dashboard widget source)"],
            ["mep_monthly_cover_page.docx",
             "Populated Word cover page (MEP logo, report period, prepared by)"],
            ["overall_report.docx",
             "Final Word monthly report (every map, chart, and the sitrep table)"],
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
    p("Every task now inherits the same skip conditions from a single "
      "top-level <b>task-instance-defaults</b> block, rather than each task "
      "declaring its own identical skipif (previously duplicated across "
      "roughly 30 individual task definitions):"),
    make_table(
        [
            ["Condition", "Behaviour"],
            ["any_is_empty_df",       "Skip task if any input DataFrame is empty"],
            ["any_dependency_skipped","Skip task if any upstream dependency was skipped"],
        ],
        [5*cm, W - 5*cm],
    ),
    p("Two tasks override this default:"),
    bullet("<b>collared_voltage_widget</b> uses <b>skipif: conditions: "
           "[never]</b>, so a dashboard widget is always created even if the "
           "underlying chart data is empty"),
    bullet("<b>persist_cover_page</b> and <b>historic_voltage_text</b> use "
           "<b>any_dependency_skipped</b> (the latter also "
           "<b>any_keyed_iterables_are_skips</b>, unpack_depth: 1), so an "
           "individual subject's filename/chart pair — or the cover page — "
           "is skipped without failing the whole zip"),
    sp(6),
    h2("11.2  Screenshot timing"),
    make_table(
        [
            ["Map / chart", "wait_for_timeout", "Reason"],
            ["Events scatter map",   "40 000 ms", "Tile map — waits for base tile rendering"],
            ["Speedmap",             "40 000 ms", "Tile map — waits for base tile rendering"],
            ["Vehicle patrol map",   "40 000 ms", "Tile map — waits for base tile rendering"],
            ["Foot patrol map",      "40 000 ms", "Tile map — waits for base tile rendering"],
            ["Historic voltage charts","10 ms",   "Static Plotly HTML — no tiles"],
        ],
        [4.5*cm, 3*cm, W - 7.5*cm],
    ),
    sp(6),
    h2("11.3  Dashboard"),
    p("The workflow concludes with <b>gather_dashboard</b>, which packages "
      "workflow details, time range, groupers, and 6 widgets into the final "
      "interactive dashboard:"),
    make_table(
        [
            ["Widget", "Source"],
            ["Collar Voltage",         "grouped_collared_widget (merged per-subject historic voltage charts)"],
            ["Elephant Sightings Map", "sightings_map_widget (persist_sightings_urls)"],
            ["Speed Map",              "speedmap_widget (persist_speedmap_html)"],
            ["Vehicle Patrols Map",    "vehicle_map_widget (vehicle_patrol_map)"],
            ["Foot Patrols Map",       "foot_map_widget (foot_patrol_map)"],
            ["Sitrep Report",          "sitrep_table_widget (persist_sitrep_table_html)"],
        ],
        [5*cm, W - 5*cm],
    ),
    p("Previously the <b>widgets</b> list was empty — this workflow had no "
      "interactive dashboard content beyond the Word report."),
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
            ["ecoscope-platform",              ">=2.15.0, <2.16.0"],
            ["ecoscope-workflows-ext-custom",  "0.1.0rc14.*"],
            ["ecoscope-workflows-ext-ste",     "0.0.0rc1.*"],
            ["ecoscope-workflows-ext-mep",     "1.0.1.*"],
            ["pydeck",                         "0.9.2"],
            ["opentelemetry-sdk",              ">=1.20.0, <2.0.0"],
        ],
        [7*cm, W - 7*cm],
    ),
    sp(6),
    note("All packages are resolved from the prefix.dev Ecoscope conda "
         "channels. ecoscope-workflows-ext-mnc, ecoscope-workflows-ext-big-life, "
         "and ecoscope-workflows-ext-icf are no longer dependencies of this "
         "workflow. ecoscope-workflows-ext-ste is pinned to a pre-release "
         "(0.0.0rc1.*)."),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF written → {OUTPUT_FILE}")
