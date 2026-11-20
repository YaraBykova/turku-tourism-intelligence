import os
from pathlib import Path

import matplotlib.pyplot as plt
import psycopg
from dotenv import load_dotenv

MONTHS_RU = "Янв Фев Мар Апр Май Июн Июл Авг Сен Окт Ноя Дек".split()

project = Path(__file__).resolve().parents[1]
load_dotenv(project / ".env")

query = (project / "sql" / "tourism_monthly_change.sql").read_text(
    encoding="utf-8-sig"
)

with psycopg.connect(
    host=os.getenv("TURKU_POSTGRES_HOST", "127.0.0.1"),
    port=os.getenv("TURKU_POSTGRES_PORT", "5433"),
    dbname=os.getenv("TURKU_POSTGRES_DB", "turku_bi"),
    user="turku",
    password=os.environ["TURKU_POSTGRES_PASSWORD"],
    connect_timeout=10,
) as connection:
    rows = connection.execute(query).fetchall()

if not rows:
    raise ValueError("Не найдены данные для помесячного сравнения.")

if any(row[1] is None for row in rows):
    raise ValueError("Для части месяцев отсутствуют данные предыдущего года.")

year = rows[0][0].year
months = [row[0].month for row in rows]
changes = [row[3] for row in rows]

previous_total = sum(row[1] for row in rows)
total_change = sum(changes)
change_pct = 100.0 * total_change / previous_total
formatted_change = f"{total_change:+,}".replace(",", " ")
formatted_pct = f"{change_pct:+.2f}".replace(".", ",")

period = (
    f"{MONTHS_RU[months[0] - 1]}"
    f"–{MONTHS_RU[months[-1] - 1]}"
)

fig, ax = plt.subplots(figsize=(11, 6))

bars = ax.bar(
    months,
    changes,
    color=["#2166AC" if value >= 0 else "#B2182B" for value in changes],
)

ax.bar_label(
    bars,
    labels=[f"{value:+,}".replace(",", " ") for value in changes],
    padding=4,
    fontsize=9,
)

ax.set_title(
    f"Ночёвки в Турку: помесячное изменение, {year} к {year - 1}\n"
    f"{period}: {formatted_change} ночёвок ({formatted_pct}%)"
)
ax.set_ylabel("Изменение количества ночёвок")
ax.set_xticks(months, [MONTHS_RU[month - 1] for month in months])
ax.yaxis.set_major_formatter(lambda value, position: f"{value:,.0f}".replace(",", " "))
ax.axhline(0, color="#333333", linewidth=0.8)
ax.set_axisbelow(True)
ax.grid(axis="y", alpha=0.2)
ax.margins(y=0.18)

fig.subplots_adjust(bottom=0.19)
fig.text(
    0.125, 0.09,
    "Источник: Statistics Finland, StatFin 11lm (CC BY 4.0).",
    fontsize=9,
)

if any(row[5] for row in rows):
    fig.text(
        0.125, 0.05,
        "* В сравнении используются предварительные данные.",
        fontsize=9,
    )

output = project / "reports" / "turku_hotel_nights_monthly_change.png"
output.parent.mkdir(exist_ok=True)
fig.savefig(output, dpi=160)
plt.close(fig)

print(f"Сохранён {output.name}")