# MEP Monthly Report — User Guide

This guide walks you through configuring and running the MEP Monthly Report workflow, which ingests events, collar GPS tracks, and vehicle and foot patrol data from EarthRanger to produce a comprehensive monthly report for the Mara Elephant Project.

---

## Overview

The workflow delivers, for each run:

- **4 maps** — events scatter map (coloured by event type), GPS speedmap, vehicle patrol trajectories map, and foot patrol trajectories map
- **Per-subject collar voltage charts** — GPS fix-rate and voltage timeline vs previous period for each collared animal
- **1 sitrep CSV** — situation report with incident counts by region
- **A Word document report** — cover page and populated content page merged into a single monthly report

---

## Prerequisites

Before running the workflow, ensure you have:

- Access to an **EarthRanger** instance with events, subject group observations, vehicle patrol, and foot patrol data logged for the analysis period

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste the GitHub repository URL into the **Github Link** field:

```
https://github.com/wildlife-dynamics/mep-monthly-report.git
```

Then click **Add Template**.

![Add Workflow Template](data/screenshots/add_workflow.png)

---

### Step 2 — Add an EarthRanger Connection

Navigate to **Data Sources** and add a new EarthRanger connection. Fill in:

- **Data Source Name** — a label to identify this connection
- **EarthRanger URL** — your instance URL (e.g. `your-site.pamdas.org`)
- **EarthRanger Username** and **EarthRanger Password**

> Credentials are not validated at setup time. Any authentication errors will appear when the workflow runs.

![EarthRanger Connection](data/screenshots/er_connection.png)

---

### Step 3 — Select the Workflow

After the template is added, it appears in the **Workflow Templates** list as **mep-monthly-report**. Click it to open the workflow configuration form.

> The card may show **Initializing…** briefly while the environment is set up.

![Select Workflow Template](data/screenshots/select_workflow.png)

---

### Step 4 — Set Workflow Details and Analysis Time Range

The configuration form opens with two sections at the top.

**Set workflow details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional notes (e.g. month, site, or reporting period) |

**Define analysis time range**

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time of the analysis period |
| Until | End date and time of the analysis period |

All events, observations, and patrol data are fetched within this window.

![Set Workflow Details and Analysis Time Range](data/screenshots/set_workflow_details_time_range.png)

---

### Step 5 — Configure Base Maps, Connect to EarthRanger, Set Subject Group, and Retrieve Vehicle Patrols

Scroll down to configure the next four sections.

**Configure base map layers**

Expand **Advanced Configurations** to select the base map tile layers displayed on all maps.

**Connect to earth ranger**

Select the EarthRanger data source configured in Step 2 from the **Data Source** dropdown.

**Subject Group**

Enter the name of the EarthRanger subject group in the field (e.g. `MEP`). This group is used to generate collar voltage charts and the overall GPS speedmap. The subject group name is also included in the Word report.

**Retrieve vehicle patrols**

Expand **Advanced Configurations** to review or override the default vehicle patrol trajectory segment filter thresholds (max length: 5 000 m, max time: 18 000 s, speed: 10–100 km/h).

![Configure Base Maps, Connect to EarthRanger, Subject Group, and Retrieve Vehicle Patrols](data/screenshots/configure_basemaps_connect_er_subject_group_vehicle_patrols.png)

---

### Step 6 — Configure Foot Patrols

Scroll down to configure the final section, then click **Submit**.

**Retrieve foot patrols**

Expand **Advanced Configurations** to review or override the default foot patrol trajectory segment filter thresholds (max length: 5 000 m, max time: 14 400 s, speed: 0.5–9 km/h).

Once all parameters are set, click **Submit**.

![Configure Foot Patrols](data/screenshots/configure_foot_patrols.png)

---

## Running the Workflow

Once submitted, the runner will:

1. Fetch all events; remove spatial outliers and null geometries; apply tab20 colour palette by event type; generate events scatter map.
2. Fetch subject group observations for the current and previous periods; produce per-subject collar voltage charts.
3. Convert GPS observations to trajectories; classify speed into 6 bins; generate speedmap.
4. Compile sitrep report from EarthRanger events; persist as CSV.
5. Fetch vehicle patrol observations; convert to trajectories; generate vehicle patrol map.
6. Fetch foot patrol observations; convert to trajectories; generate foot patrol map.
7. Download Word templates from Dropbox; populate cover page and content page with all maps, charts, and sitrep data.
8. Merge cover page and content page into the final Word report.
9. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`. Files marked with `<subject>` are produced once per collared subject.

| File | Description |
|------|-------------|
| `elephant_sightings_map.html` / `.png` | Scatter map of all events, coloured by event type |
| `speedmap.html` / `.png` | GPS trajectories coloured by 6-bin speed classification |
| `vehicle_patrols_map.html` / `.png` | Vehicle patrol trajectories coloured by team |
| `foot_patrols_map.html` / `.png` | Foot patrol trajectories coloured by team |
| `vehicle_patrol_trajectories.geoparquet` | Raw vehicle patrol trajectory data |
| `foot_patrol_trajectories.geoparquet` | Raw foot patrol trajectory data |
| `sitrep_report.csv` | Situation report — incident counts and categories by region |
| `<subject>_collar_voltage.html` / `.png` | Collar voltage and GPS fix-rate chart (current vs previous period) |
| `mep_cover_page.docx` | Populated Word cover page |
| `mep_context.docx` | Populated Word content page |
| `overall_mep_monthly_report.docx` | Final merged Word monthly report |
