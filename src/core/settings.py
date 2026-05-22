from typing import Dict, Any, Union
from pydantic import BaseModel, Field

class DriverConfig(BaseModel):
    type: str
    params: Dict[str, Any] = Field(default_factory=dict)

class Settings(BaseModel):
    context: str
    drivers: Dict[str, Union[str, DriverConfig]]
    
    # Helper to resolve Union[str, DriverConfig] to DriverConfig
    def get_driver_config(self, driver_key: str) -> DriverConfig:
        config = self.drivers.get(driver_key)
        if isinstance(config, str):
            return DriverConfig(type=config)
        return config
