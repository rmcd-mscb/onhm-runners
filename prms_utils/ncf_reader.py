from netCDF4 import Dataset
from netCDF4 import num2date
import datetime


def read(nc_fn):
    nc_fid = Dataset(nc_fn, 'r')
    nc_attrs = nc_fid.ncattrs()
    # print 'attrs', nc_attrs

    nc_dims = [dim for dim in nc_fid.dimensions]
    # print 'dims', nc_dims

    # Figure out the variable names with data in the ncf.
    nc_vars = [var for var in nc_fid.variables]
    remove_list = list(nc_dims)
    remove_list.extend(['hru_lat', 'hru_lon', 'seg_lat', 'seg_lon'])
    var_names = [e for e in nc_vars if e not in remove_list]
    # print 'var_names', var_names

    time = nc_fid.variables['time'][:]
    nts = len(time)
    # print(time, nts)

    time_var = nc_fid.variables['time']
    # print(str(time_var))
    dtime = num2date(time_var[:],time_var.units)
    # print("dtime = " + str(dtime[0]))

    base_date_str = str(dtime[0])
    print('base_date_str ' + base_date_str)
    # base_date_str = "2019-05-05"
    tok = base_date_str.split(' ')
    ymd = tok[0]
    tok = ymd.split('-')
    base_date = datetime.date(int(tok[0]), int(tok[1]), int(tok[2]))
    print(base_date)

    # Read the values into a dictionary.
    vals = {}
    for var in var_names:
        f1 = nc_fid.variables[var][:]
        vals[var] = f1

    nc_fid.close()

    return var_names, base_date, nts, vals