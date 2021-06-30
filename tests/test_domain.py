# -*- coding: utf-8 -*-
# flake8: noqa
import pytest
import cordex as cx 


def test_constructor():
    eur11 = cx.cordex_domain('EUR-11')
    eur11_user = cx.create_dataset(nlon=424, nlat=412, dlon=0.11, dlat=0.11, ll_lon=-28.375, ll_lat=-23.375, pollon=-162.00, pollat=39.25)
    assert(eur11_user.equals(eur11))
