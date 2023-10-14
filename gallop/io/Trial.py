from dataclasses import dataclass

import xarray as xr


@dataclass
class Trial:
    markers: xr.DataArray
    raw_analog: xr.DataArray
