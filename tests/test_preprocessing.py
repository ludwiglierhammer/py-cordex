import xarray as xr
import numpy as np
import pytest

from cordex.preprocessing.preprocessing import (
    rename_cordex,
    get_grid_mapping,
    replace_coords,
    cordex_dataset_id
)

from cordex import cordex_domain


def create_test_ds(name, pol_name="rotated_latitude_longitude", dummy=True,
                  add_vertices=True, **kwargs):
    domain = cordex_domain(name, mapping_name=pol_name, dummy=dummy, 
                           add_vertices=add_vertices, **kwargs)
    return domain


def create_wrf_test(name):
    ds = create_test_ds("EUR-11", "rotated_pole")
    # reindex dummy with lon lat like in wrf
    ds["dummy"] = xr.DataArray(
        ds.dummy.values, dims=("lat", "lon"), attrs=ds.dummy.attrs
    )
    return ds


# def create_test_ds(xname, yname, xlen, ylen, name):
#     x = np.linspace(0, 359, xlen)
#     y = np.linspace(-90, 89, ylen)

#     data = np.random.rand(len(x), len(y))
#     ds = xr.DataArray(data, coords=[(xname, x), (yname, y)]).to_dataset(
#         name="test"
#     )
#     ds.attrs["source_id"] = "test_id"
#     # if x and y are not lon and lat, add lon and lat to make sure there are no conflicts
#     lon = ds[xname] * xr.ones_like(ds[yname])
#     lat = xr.ones_like(ds[xname]) * ds[yname]
#     if xname != "lon" and yname != "lat":
#         ds = ds.assign_coords(lon=lon, lat=lat)
#     else:
#         ds = ds.assign_coords(longitude=lon, latitude=lat)
#     return ds


def test_wrf_case():
    """Test the wrf exception"""
    ds = create_wrf_test("EUR-11")
    assert rename_cordex(ds).equals(create_test_ds("EUR-11"))
    

@pytest.mark.parametrize("lon_name", ["longitude"])
@pytest.mark.parametrize("lat_name", ["latitude"])
@pytest.mark.parametrize("pol_name", ["rotated_latitude_longitude", "rotated_pole"])
@pytest.mark.parametrize("lon_vertices", ["longitude_vertices"])
@pytest.mark.parametrize("lat_vertices", ["latitude_vertices"])
def test_rename_cordex(lon_name, lat_name, pol_name, lon_vertices, lat_vertices):
    dm = create_test_ds('EUR-11', pol_name)
    dm = dm.rename({'lon': lon_name, 'lat': lat_name, 'lon_vertices': lon_vertices, 'lat_vertices': lat_vertices})
    assert rename_cordex(dm).equals(create_test_ds('EUR-11'))
    
    

def test_grid_mapping():
    ds = create_test_ds('EUR-11')
    assert (get_grid_mapping(ds).equals(ds.rotated_latitude_longitude))
    
    
def test_replace_coords():
    ds = create_test_ds('EUR-11')
    ds['rlon'] = np.arange(ds.rlon.size)
    ds['rlat'] = np.arange(ds.rlat.size)
    ds['lon'] = np.arange(ds.lon.size)
    ds['lat'] = np.arange(ds.lon.size)
    assert(replace_coords(ds).equals(create_test_ds('EUR-11')))
    
    
def test_cordex_dataset_id():
    ds = create_test_ds('EUR-11', attrs='CORDEX')
    ds.attrs['driving_model_id'] = 'MY-DRIVE-MODEL'
    ds.attrs['institute_id'] = 'INSTITUTE'
    ds.attrs['model_id'] = 'RCM'
    ds.attrs['experiment_id'] = 'historical'
    ds.attrs['frequency'] = 'mon'
    assert cordex_dataset_id(ds, sep=".") == 'EUR-11.MY-DRIVE-MODEL.INSTITUTE.RCM.historical.mon'