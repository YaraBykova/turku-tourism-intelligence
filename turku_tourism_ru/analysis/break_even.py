import csv
from math import ceil
from pathlib import Path

project = Path(__file__).resolve().parents[1]
listings = project / "data" / "rent_listings.csv"

with listings.open(encoding="utf-8-sig", newline="") as file:
    listing = next(row for row in csv.DictReader(file) if row["listing_id"] == "KIR01")

rent = float(listing["asking_rent_eur_month"])

# Допущения для первого сценария, суммы в евро.
open_days = 26
average_purchase_excl_vat = 18
variable_cost_per_purchase = 10
monthly_staff_cost = 1800
other_monthly_fixed_costs = 300

contribution_per_purchase = average_purchase_excl_vat - variable_cost_per_purchase
monthly_fixed_costs = rent + monthly_staff_cost + other_monthly_fixed_costs
purchases_per_month = ceil(monthly_fixed_costs / contribution_per_purchase)
purchases_per_day = ceil(purchases_per_month / open_days)

print(f"Помещение — {listing['address']}")
print(f"Ежемесячные расходы по сценарию — {monthly_fixed_costs:,.0f} евро")
print(f"После переменных затрат остаётся {contribution_per_purchase:.0f} евро с покупки")
print(f"Порог — {purchases_per_month} покупок в месяц, около {purchases_per_day} в рабочий день")
print("\nКак меняется порог:")
for amount in (6, 8, 10):
    monthly = ceil(monthly_fixed_costs / amount)
    daily = ceil(monthly / open_days)
    print(f"{amount} евро с покупки — {monthly} в месяц, {daily} в рабочий день")

print("\nКакой поток нужен у входа:")
for conversion_percent in (1, 2, 3):
    passages = ceil(purchases_per_day / (conversion_percent / 100))
    print(f"{conversion_percent}% проходов заканчиваются покупкой — {passages} проходов в день")
