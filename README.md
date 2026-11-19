# Turku Tourism Intelligence

**Data Engineering / Data Analytics portfolio project** using open hotel-night data for Turku, Tampere and Oulu, Finland.

## Choose a language / Выберите язык

| Version | Project and setup | Dashboard PDF |
|---|---|---|
| English | [English documentation](turku_tourism_en/README.md) | [View three-page dashboard](turku_tourism_en/turku_tourism_dashboard.pdf) |
| Русский | [Документация на русском](turku_tourism_ru/README.md) | [Посмотреть дашборд — 3 страницы](turku_tourism_ru/turku_tourism_dashboard.pdf) |

Both folders are language editions of the same project, with the same source data and numeric calculations. Use one edition to run the pipeline; their Docker configurations refer to the same local project and default ports.

## Analytical question

How have hotel nights in Turku changed relative to Tampere and Oulu, and how much have domestic and international nights contributed?

### January–September 2026 versus the same months of 2025

| City | Hotel nights | Change | Growth |
|---|---:|---:|---:|
| Turku | 689,463 | +43,040 | +6.66% |
| Tampere | 1,023,197 | +5,017 | +0.49% |
| Oulu | 449,842 | +53,140 | +13.40% |

Turku grew faster than Tampere and more slowly than Oulu. Domestic and international nights contributed almost equally to Turku's increase; domestic nights contributed most of Oulu's increase. These are descriptive comparisons, without a causal claim.

See the [full comparative analysis](turku_tourism_en/reports/city_comparison.md) for segment contributions, complete-year seasonality, comparison-group rationale and limitations.

## Data and implementation

- **Source:** [Statistics Finland, StatFin 11lm](https://pxdata.stat.fi/PXWeb/pxweb/en/StatFin/StatFin__matk/11lm.px), CC BY 4.0.
- **Grain:** municipality × calendar month; 279 rows, 93 months per city, January 2019–September 2026 in the verified snapshot.
- **Stack:** Python, PostgreSQL 17, Docker Compose, Airflow 3.4.0, dbt Core 1.12.7, SQL, matplotlib and Power BI Desktop.

```text
StatFin API → timestamped raw JSON and validated CSV
→ transactional PostgreSQL upsert
→ three dbt views and quality tests
→ SQL analysis, charts and Power BI import
```

The Airflow DAG runs seven sequential tasks. The local schedule is daily at 01:20 Europe/Moscow, requiring the computer and containers to be running. Power BI import is refreshed separately.

![Seasonality of domestic and international hotel nights in Turku](turku_tourism_en/reports/turku_hotel_nights_segment_seasonality.png)

## Reproduce or review

- Start with the [English setup instructions](turku_tourism_en/README.md#stack-and-local-setup) or [Russian instructions](turku_tourism_ru/README.md).
- For a quick review without Power BI, open either PDF above. Each has Overview 2026, Seasonality 2025 and City comparison 2026.
- For report definitions, open the chosen folder's `turku_tourism_dashboard.pbip` with its neighbouring `.Report` and `.SemanticModel` folders. Refresh against your local PostgreSQL database.
- `.env.example` contains a placeholder; create your own local `.env`. Real credentials, Power BI caches and the legacy PBIX are excluded.

## Verification

The three-city pipeline passed 21 Python tests, three dbt tests and a full seven-task manual Airflow run. Empty-database verification loaded 279 rows, with zero changes on repeat and stale-snapshot loads. The report contains 31 measures and three pages; 612 numerical DAX comparisons were completed on the original model. The English edition preserves all 25 numeric expressions. Both final three-page PDFs were reviewed, with aligned years and matching values.

Details: [verification record](turku_tourism_en/reports/verification.md). A cold installation on a different computer has not been verified. This is a local portfolio deployment.

## Interpretation limits

2026 data are preliminary. Hotel classification changed in 2025, limiting comparisons with earlier years. Hotel nights are not unique visitors, store footfall or sales. The analysis does not control for hotel capacity or other drivers and does not establish causes, forecast demand or select a souvenir-store location. Oulu's official EU title European Capital of Culture 2026 is contextual information; its effect is not estimated.
