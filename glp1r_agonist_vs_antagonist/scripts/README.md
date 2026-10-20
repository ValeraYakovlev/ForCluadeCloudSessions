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

## Аннотированные 3D-сцены (figA–figF)

`scene_a2.py`, `scene_b.py`, `scene_c.py`, `scene_d.py`, `scene_e.py`, `scene_f.py` строят сцены в headless PyMOL (ray tracing, ортоскопическая проекция); подписи остатков рисуются поверх через matplotlib: `project.py` калибрует DLT-проекцию по цветным псевдоатомам, `annotate.py` раскладывает подписи по колонкам, `scenes.py` связывает всё вместе, `render_common.py` — палитра и общие настройки. Сцена → рисунок в отчёте: scene_c → figA, scene_f → figB, scene_d → figC, scene_e → figD, scene_a2 → figE, scene_b → figF. `export_annot.py` пишет `structures/6X18_GLP1R_hotspots.pdb`; `an9.py` — проверка столкновений Fab 3F52 (5E94) с активным и неактивным рецептором; `an10.py` — устойчивость вывода к границе ECD/TMD и независимые неактивные эталоны для сдвига TM6. `doc_xml_to_md.py` собирает `REPORT.md` из XML-экспорта документа Claude Docs. Запуск: `bash run_all_scenes.sh` из каталога с `work/pdb/*.cif` и `renders/`; PyMOL — `pip install pymol-open-source`.
