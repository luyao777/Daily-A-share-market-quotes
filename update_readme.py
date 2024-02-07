import os
from datetime import datetime


def update_readme(date_str, sh_img_path, sz_img_path, bj_img_path):
    now = datetime.now()
    current_hr = str(now.hour)
    current_min = str(now.minute)

    readme_file_name = 'README.md'

    # current_file_path = os.path.abspath(__file__)
    # current_directory = os.path.dirname(current_file_path)
    current_directory = '.'

    readme_file_path = os.path.join(current_directory, readme_file_name)

    file_content = f"""
# Daily-A-share-market-quotes 每日 A 股指数（5min 更新）- {date_str}

### 上证指数 {date_str} {current_hr}:{current_min}
![]({sh_img_path})

### 深证成指 {date_str} {current_hr}:{current_min}
![]({sz_img_path})

### 北证50 {date_str} {current_hr}:{current_min}
![]({bj_img_path})
"""

    with open(readme_file_path, 'w') as f:
        f.write(file_content)


if __name__ == '__main__':
    update_readme('2024-02-06', './fig/2024/2/20240206-sh000001.png', './fig/2024/2/20240206-sh000001.png', './fig/2024/2/20240206-sh000001.png')
