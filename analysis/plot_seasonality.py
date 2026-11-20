import os
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import psycopg
from dotenv import load_dotenv

project = Path(__file__).resolve().parents[1]
load_dotenv(project / ".env")

query = """
SELECT month, hotel_nights, is_preliminary
FROM marts.tourism_seasonality
WHERE municipality_code = '853'
ORDER BY month;
"""

by_year = defaultdict(list)
with psycopg.connect(
    host=os.getenv("TURKU_POSTGRES_HOST", "127.0.0.1"),
    port=os.getenv("TURKU_POSTGRES_PORT", "5433"),
    dbname=os.getenv("TURKU_POSTGRES_DB", "turku_bi"),
    user="turku",
    password=os.environ["TURKU_POSTGRES_PASSWORD"],
    connect_timeout=10,
) as connection:
    for month, nights, preliminary in connection.execute(query):
        by_year[month.year].append((month.month, nights, preliminary))

if not by_year:
    raise ValueError("В PostgreSQL не найдены данные о ночёвках в Турку.")

fig, ax = plt.subplots(figsize=(11, 6))

for year, rows in sorted(by_year.items()):
    months, nights, preliminary = zip(*sorted(rows))
    ax.plot(
        months, nights,
        label=f"{year}*" if any(preliminary) else str(year),
        linestyle="--" if any(preliminary) else "-",
    )

ax.set_title("Гостиничные ночёвки в Турку по месяцам")
ax.set_ylabel("Количество ночёвок")
ax.set_xticks(range(1, 13), "Янв Фев Мар Апр Май Июн Июл Авг Сен Окт Ноя Дек".split())
ax.yaxis.set_major_formatter(lambda value, position: f"{value:,.0f}".replace(",", " "))
ax.grid(axis="y", alpha=0.25)
ax.legend(ncol=4)

fig.subplots_adjust(bottom=0.19)
fig.text(0.125, 0.09, "Источник: Statistics Finland, StatFin 11lm (CC BY 4.0).", fontsize=9)
fig.text(0.125, 0.05, "* Предварительные данные. В 2025 году изменилась классификация гостиниц.", fontsize=9)

output = project / "reports" / "turku_hotel_nights_seasonality.png"
output.parent.mkdir(exist_ok=True)
fig.savefig(output, dpi=160)
print(f"Сохранён {output.name}")