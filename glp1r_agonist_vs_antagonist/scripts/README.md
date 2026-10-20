# Скрипты расчётов (воспроизводимость)

Все числа с пометкой «расчёт» в отчёте получены этими скриптами на структурах RCSB.
Скрипты рассчитаны на рабочий каталог со структурой:

```
work/pdb/<ID>.cif      # mmCIF из https://files.rcsb.org/download/<ID>.cif
work/glp1r_ids.json    # список PDB с UniProt P43220 (pdb_list.py)
work/glp1r_pdb_details.json  # метаданные RCSB GraphQL (pdb_details.py)
```

Порядок: `pdb_list.py` → `pdb_details.py` → скачать нужные cif (6X18, 6LN2, 3C5T, 3IOL, 5E94, 7KI0, 7FIM, 7LLL, 6B3J, 9IVG, 6VCB, 6X1A, 6X19, 6XOX, 7S15, 7RG9, 8WG7, 7C2E, 7X8R, 7DUR, 7EVM) → `an1.py`, `an2.py`, `an3.py`, `an5.py`, `an7.py`, `an8.py`, `run_states.py` → `figs.py` → `build_xlsx.py`.

Зависимости: Python 3.13, numpy, biopython, gemmi, matplotlib, openpyxl.
Методика: SASA по Shrake–Rupley (Biopython, зонд 1.4 Å, 200–300 точек); ECD = остатки 29–137, остальное = TMD + петли; «скрыто» = SASA лиганда отдельно минус SASA лиганда в присутствии партнёра; суперпозиция по ядру TMD (остатки 143–400, итеративное отбрасывание выбросов > 3 Å).
В скриптах остались абсолютные пути рабочей сессии (scratchpad) — при повторном запуске замените их.
