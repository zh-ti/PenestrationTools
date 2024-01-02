"""

Demonstrates the use of multiple Progress instances in a single Live display.

"""

from pathlib import Path
import shutil
from time import sleep

from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, MofNCompleteColumn, TaskProgressColumn, TimeElapsedColumn
from rich.table import Table
from mfio.scanlib.scan import Scan
from collections import defaultdict
from copy import deepcopy

save_path = Path(r"C:\Users\pc\Desktop\save")
img_path = Path(r"C:\Users\pc\Desktop\2023-05-20-14-47-26")
img_list = Scan(img_path, suffixs=[".png", ".jpg", ".jpeg", ".bmp", ".pcd"]).file_list

name_file_dic = defaultdict(list)
total = len(img_list)

for file in img_list:
    idx = file.stem.split("_")[0]
    name_file_dic[idx].append(file)

task_file_dic = deepcopy(name_file_dic)

job_progress = Progress(
    "{task.description}",
    BarColumn(),
    MofNCompleteColumn(),
    TaskProgressColumn(),
    TimeElapsedColumn(),
    auto_refresh=False,
)

overall_progress = Progress(
    "{task.description}",
    BarColumn(),
    MofNCompleteColumn(),
    TaskProgressColumn(),
    TimeElapsedColumn(),
    auto_refresh=False,
)
overall_task = overall_progress.add_task("总进度", total=total)

progress_table = Table.grid()
progress_table.add_row(Panel.fit(overall_progress, title="总进度", border_style="green"))
progress_table.add_row(Panel.fit(job_progress, title="[b]子进度", border_style="red"))

with Live(progress_table, refresh_per_second=10):
    for i in range(3):
        key, value = name_file_dic.popitem()
        job_progress.add_task(f"{key}", total=len(value))
    while not overall_progress.finished:
        for job in job_progress.tasks:
            for file in task_file_dic[job.description]:
                output_file = save_path / job.description / file.relative_to(img_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(file, output_file)
            if not job.finished:
                job_progress.advance(job.id)
                overall_progress.advance(overall_task)
            else:
                if len(job_progress.tasks) > 3:
                    job_progress.remove_task(job.id)
                if name_file_dic:
                    key, value = name_file_dic.popitem()
                    job_progress.add_task(f"{key}", total=len(value))
