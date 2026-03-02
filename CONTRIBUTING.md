# Contributing: Adding New Bikes

This guide walks through adding new bicycle geometry data to the comparator and submitting a pull request.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Python 3.13+
- Git

## Data Directory Structure

All bike data lives under `data/` organized by brand, model, optional variant, and year:

```
data/
└── <brand>/
    ├── defaults.ini              # brand name
    └── <model>/
        ├── defaults.ini          # (optional) model name
        ├── metric_mappings.ini   # (optional) column renames
        └── <year>/
            ├── defaults.ini      # year
            └── geometry.csv      # geometry measurements
```

If a bike has distinct frame variants (e.g. aluminum vs carbon, different generations), add an intermediate directory:

```
data/
└── trek/
    └── domane/
        ├── al/
        │   └── gen4/
        │       ├── defaults.ini          # model : Domane AL Gen 4
        │       ├── metric_mappings.ini
        │       └── 2024/
        │           ├── defaults.ini      # year : 2024
        │           └── geometry.csv
        └── carbon/
            └── gen4/
                └── 2023/
                    ├── defaults.ini
                    └── geometry.csv
```

## Step-by-Step Guide

### 1. Create the directory structure

For a new brand:

```bash
mkdir -p data/mybrand/mymodel/2025
```

For an existing brand:

```bash
mkdir -p data/canyon/grail/2025
```

### 2. Create `defaults.ini` files

Each level needs a `defaults.ini` that provides metadata values applied to every row in the geometry CSV.

**Brand level** — `data/mybrand/defaults.ini`:

```ini
brand : MyBrand
```

**Model level** (optional, can be combined with year) — `data/mybrand/mymodel/defaults.ini`:

```ini
model : My Model
```

**Year level** — `data/mybrand/mymodel/2025/defaults.ini`:

```ini
year : 2025
```

If the brand directory already has a `defaults.ini`, you don't need to create it again.

You can put `brand`, `model`, and `year` at any level — they cascade downward and child values override parent values. The simplest setup with no variant is:

```
data/mybrand/defaults.ini          → brand : MyBrand
data/mybrand/mymodel/defaults.ini  → model : My Model
data/mybrand/mymodel/2025/defaults.ini → year : 2025
```

### 3. Create `geometry.csv`

Place a `geometry.csv` in the year directory. Each row is one frame size.

**Minimal example** (columns match the database schema exactly):

```csv
size,stack,reach,seat_tube_length,top_tube_length,head_tube_length,head_tube_angle,seat_tube_angle,chainstay,wheelbase,bb_drop,trail,standover_height
XS,522,373,450,508,114,71.4,75.5,410,978,76,62,719
S,540,380,470,525,130,72.0,74.5,410,982,75,60,738
M,563,388,500,545,150,72.5,74.0,412,990,75,58,760
L,583,395,530,565,170,73.0,73.5,412,998,74,56,785
XL,605,402,560,585,195,73.0,73.0,415,1010,72,55,800
```

**Required columns:**

| Column | Type | Constraint |
|--------|------|------------|
| `size` | text | Frame size label (e.g. `XS`, `54cm`, `17.5"`) |
| `stack` | integer (mm) | Must be between 400 and 800 |
| `reach` | integer (mm) | Must be between 300 and 600 |

`brand`, `model`, and `year` come from `defaults.ini` — do **not** include them in the CSV.

**Optional geometry columns:**

| Column | Type | Description |
|--------|------|-------------|
| `top_tube_length` | integer (mm) | Horizontal top tube length |
| `seat_tube_length` | integer (mm) | Seat tube length |
| `seat_tube_angle` | float (degrees) | Seat tube angle |
| `head_tube_angle` | float (degrees) | Head tube angle |
| `head_tube_length` | integer (mm) | Head tube length |
| `chainstay` | integer (mm) | Chainstay length |
| `wheelbase` | integer (mm) | Wheelbase |
| `trail` | integer (mm) | Trail |
| `bb_drop` | integer (mm) | Bottom bracket drop |
| `front_center_distance` | integer (mm) | Front center distance |
| `standover_height` | integer (mm) | Standover height |
| `fork_rake` | integer (mm) | Fork rake / offset |
| `fork_axle_to_crown` | integer (mm) | Fork axle to crown |

**Optional component columns:**

| Column | Type | Constraint |
|--------|------|------------|
| `stem_length` | integer (mm) | 9 - 200 |
| `handlebar_width` | integer (mm) | 200 - 900 |
| `crank_length` | float (mm) | 120 - 220 |
| `saddle_width` | integer (mm) | 50 - 300 |
| `seat_post_length` | integer (mm) | 20 - 600 |
| `wheel_size` | text | e.g. `700c`, `29"`, `27.5"` |
| `chainring_size` | text | e.g. `50/34` |
| `seat_post_diameter` | text | e.g. `27.2mm` |
| `cockpit_dimensions` | text | Integrated bar/stem specs |
| `body_height_range` | text | e.g. `170-180 cm` |
| `seat_height_range` | text | Seat height range |

### 4. Create `metric_mappings.ini` (if needed)

If the manufacturer's column names don't match the schema above, create a `metric_mappings.ini` to map them. This file goes alongside the `geometry.csv` or at a parent level if shared across years.

**Format:**

```ini
<csv_column_name> : <schema_column_name>
```

Map a column to `-` to exclude it:

```ini
<csv_column_name> : -
```

**Example** — the manufacturer uses `effective_top_tube` instead of `top_tube_length`, and has a `bottom_bracket_height` column you want to ignore:

```ini
effective_top_tube : top_tube_length
head_angle : head_tube_angle
chainstay_length : chainstay
bottom_bracket_drop : bb_drop
standover : standover_height
frame_reach : reach
frame_stack : stack
bottom_bracket_height : -
```

**Common rename patterns:**

| Manufacturer might call it | Schema name |
|----------------------------|-------------|
| `effective_top_tube`, `top_tube_horizontal` | `top_tube_length` |
| `head_angle` | `head_tube_angle` |
| `seat_tube` | `seat_tube_length` |
| `chainstay_length`, `chain_stay_length` | `chainstay` |
| `bottom_bracket_drop` | `bb_drop` |
| `standover`, `stand_over_height` | `standover_height` |
| `frame_reach` | `reach` |
| `frame_stack` | `stack` |
| `fork_rake_offset` | `fork_rake` |
| `axle_to_crown` | `fork_axle_to_crown` |

Mappings cascade just like defaults — define them at the brand or model level if they apply to multiple years.

### 5. Build and verify

```bash
make build
```

This assembles all data into `build/database.csv`. Check that your bike appears:

```bash
grep "MyBrand" build/database.csv
```

If the build fails, check:

- **Stack out of range**: must be 400-800 mm (integer)
- **Reach out of range**: must be 300-600 mm (integer)
- **Duplicate primary key**: `(brand, model, year, size)` must be unique
- **Column mismatch**: CSV column names must match schema names or have a mapping

### 6. Run the full test suite

```bash
make test
```

This runs linting, type checking, and pytest (including data validity tests).

### 7. Preview in the frontend (optional)

```bash
make dev
```

Open the Vite dev server URL and verify your bike shows up in search and comparison views.

## Submitting a Pull Request

1. Fork the repository and create a branch:

   ```bash
   git checkout -b add-mybrand-mymodel-2025
   ```

2. Add your data files (geometry.csv, defaults.ini, metric_mappings.ini as needed).

3. Verify the build passes:

   ```bash
   make build
   ```

4. Commit your changes:

   ```bash
   git add data/mybrand/
   git commit -m "Add MyBrand My Model 2025 geometry data"
   ```

5. Push and open a PR against `main`:

   ```bash
   git push origin add-mybrand-mymodel-2025
   ```

Include in your PR description:
- Which bike(s) you added
- Source of the geometry data (manufacturer website link)

## Real-World Examples

### Simple case: Rose Reveal 2020

No column renaming needed — CSV columns match the schema directly.

```
data/rose/
├── defaults.ini                → brand : Rose
└── reveal/
    └── 2020/
        ├── defaults.ini        → year : 2020
        └── geometry.csv        → size,stack,reach,seat_tube_length,...
```

Note that `model` is not set in any `defaults.ini` here — the directory name `reveal` is not automatically used. Add a `data/rose/reveal/defaults.ini` with `model : Reveal` if needed.

### Complex case: Trek Marlin Gen 3 2023

CSV uses non-standard column names, some columns excluded, uses variant directory.

```
data/trek/
├── defaults.ini                        → brand : Trek
└── marlin/
    └── gen3/
        ├── defaults.ini                → model : Marlin Gen 3
        ├── metric_mappings.ini         → renames + exclusions
        └── 2023/
            ├── defaults.ini            → year : 2023
            └── geometry.csv
```

The `metric_mappings.ini`:

```ini
_offset : -
seat_tube : seat_tube_length
head_angle : head_tube_angle
effective_top_tube : top_tube_length
bottom_bracket_drop : bb_drop
chainstay_length : chainstay
standover : standover_height
frame_reach : reach
frame_stack : stack
seat_tube_angle : -
effective_seat_tube_angle : seat_tube_angle
bottom_bracket_height : -
size : -
frame_size_letter : size
```

This renames columns like `frame_reach` to `reach`, swaps `size`/`frame_size_letter`, and drops `_offset` and `bottom_bracket_height`.

## Tips

- Copy the geometry table directly from the manufacturer's website into a spreadsheet, then export as CSV.
- All length measurements should be in **millimeters**. Convert from centimeters if needed.
- Angles are in **degrees** as floats (e.g. `72.5`).
- The `size` column is free-form text — use whatever the manufacturer uses (`XS`, `54`, `54cm`, `17.5"`).
- When in doubt about a column name, check the schema in `src/bike_geometry_comparator/database/schema.sql`.
