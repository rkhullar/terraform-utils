from pathlib import Path, PurePosixPath
from typing import Dict


def build_output(data: Dict[str, str], key: str = None, component: str = None,
                 prefix: str = '{app_name}-', suffix: str = '-{app_env}-{company}',
                 bucket_name: str = 'terraformstate', table_name: str = 'terraformlock',
                 state_name: str = 'terraform.tfstate', app_env_var: str = 'app_env') -> str:

    if key:
        return data.get(key)

    if component == 'env':
        return data[app_env_var]

    if component == 'bucket':
        return prefix.format(**data) + bucket_name + suffix.format(**data)

    if component == 'table':
        return prefix.format(**data) + table_name + suffix.format(**data)

    if component == 'object':
        state_path = Path(data['construct']) / state_name
        state_path = PurePosixPath(state_path)
        return str(state_path)
