from dataclasses import dataclass

import dataclasses_json

from chronus.domain.model import Model


@dataclasses_json.dataclass_json
@dataclass
class LocalSettings:
    loaded_model: Model = None
