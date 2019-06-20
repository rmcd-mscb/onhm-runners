# markstro
# 2019-04-22
#
# Run this on files that have been created by animation_file_reader. These are some sort of CSV
# files that have been created from PRMS animation files.

import numpy as np
import pandas as pd
from timeit import default_timer as timer
import csv

nhm_seg = [1435, 1436, 1437, 1438, 1439, 1440, 1441, 1442, 1443, 1444, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452,
           1453, 1454, 1455, 1456, 1457, 1458, 1459, 1460, 1461, 1462, 1463, 1464, 1465, 1466, 1467, 1468, 1469, 1470,
           1471, 1472, 1473, 1474, 1475, 1476, 1477, 1478, 1479, 1480, 1481, 1482, 1483, 1484, 1485, 1486, 1487, 1488,
           1489, 1490, 1491, 1492, 1493, 1494, 1495, 1496, 1497, 1498, 1499, 1500, 1501, 1502, 1503, 1504, 1505, 1545,
           1546, 1547, 1548, 1549, 1550, 1551, 1552, 1553, 1554, 1555, 1556, 1557, 1558, 1559, 1560, 1561, 1562, 1563,
           1564, 1565, 1566, 1567, 1568, 1569, 1570, 1571, 1572, 1573, 1574, 1575, 1576, 1577, 1578, 1579, 1580, 1581,
           1582, 1583, 1584, 1585, 1586, 1587, 1588, 1589, 1590, 1591, 1592, 1593, 1594, 1595, 1596, 1597, 1598, 1599,
           1600, 1601, 1602, 1634, 1635, 1636, 1637, 1638, 1639, 1640, 1641, 1642, 1643, 1644, 1645, 1646, 1647, 1648,
           1649, 1650, 1651, 1652, 1653, 1654, 1655, 1656, 1657, 1658, 1659, 1660, 1661, 1662, 1663, 1664, 1665, 1666,
           1667, 1668, 1669, 1670, 1671, 1672, 1673, 1674, 1675, 1676, 1677, 1678, 1679, 1680, 1681, 1682, 1683, 1684,
           1685, 1686, 1687, 1688, 1689, 1690, 1691, 1692, 1693, 1694, 1695, 1696, 1697, 1698, 1699, 1700, 1701, 1702,
           1703, 1704, 1705, 1706, 1707, 1708, 1709, 1710, 1711, 1712, 1713, 1714, 1715, 1716, 1717, 1718, 1719, 1720,
           1721, 1722, 1723, 1724, 1762, 1763, 1764, 1765, 1766, 1767, 1768, 1769, 1770, 1771, 1772, 1773, 1774, 1775,
           1776, 1777, 1778, 1779, 1780, 1781, 1782, 1783, 1784, 1785, 1786, 1787, 1788, 1789, 1790, 1791, 1792, 1793,
           1794, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803, 1804, 1805, 1806, 1807, 1808, 1809, 1810, 1811,
           1812, 1813, 1814, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1826, 1827, 1828, 1829,
           1830, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021,
           2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039,
           2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2277, 2278, 2279, 2280, 2281, 2282, 2283, 2284, 2285,
           2286, 2287, 2288, 2289, 2290, 2291, 2292, 2293, 2294, 2295, 2296, 2297, 2298, 2299, 2300, 2301, 2302, 2303,
           2304, 2305, 2306, 2307, 2308, 2309, 2310, 2311, 2312, 2313, 2314, 2315, 2316, 2317, 2318, 2319, 2320, 2321,
           2322, 2323, 2324, 2325, 2326, 2327, 2328, 2329, 2330, 2331, 2332, 2333, 2334, 2335, 2336, 2337, 2338, 2339,
           2686, 2687, 2688, 2689, 2690, 2691, 2692, 2693, 2694, 2695, 2696, 2697, 2698, 2699, 2700, 3557, 3558, 3559,
           3560, 3561, 3562, 3563, 3564, 3565, 3566, 3567, 3568, 3569, 3570, 3571, 3572, 3573, 3574, 4182, 4183, 4184,
           4185, 4186, 4187, 4188, 4189, 4190, 4191, 4192, 4193, 4194, 4195, 4196, 4197, 4198, 4199, 4200, 4201, 4202,
           4203, 4204, 4205, 4206, 4230, 4231]

# nhm_seg = [2,3]

var_list = ['seg_outflow', 'seg_tave_water', 'seg_width']
# var_list = ['seg_tave_water']

def csv_reader(fn, num_rows, num_cols):
    start = timer()
    v1 = np.zeros(shape=[num_rows, num_cols])

    with open(fn) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        ii = 0
        for row in csv_reader:
            for jj in range(num_segs):
                v1[ii,jj] = float(row[jj])
            ii += 1

    end = timer()
    print("time to read ", str(end - start))  # Time in seconds

    return v1


if __name__ == '__main__':
    dir = '/ssd/markstro/conusStreamTemp/work_lev3/out/'
    dates_fn = 'dates.txt'
    dates = np.loadtxt(dir + dates_fn, dtype=str)

    for ii in range(len(var_list)):
        fn = dir + var_list[ii] + '.txt'
        print("reading ", fn)

        num_segs = 56460
        v1 = csv_reader(fn, len(dates), num_segs)
        print(v1)

        vals = np.zeros(shape=[len(dates), len(nhm_seg)])
        for jj in range(len(dates)):
            for kk in range(len(nhm_seg)):
                # vals[jj,kk] = v1[nhm_seg[kk] - 1,jj]
                vals[jj, kk] = v1[jj, nhm_seg[kk] - 1]

        # Write the output cvs file
        fn2 = dir + var_list[ii] + '.csv'

        print("writing ", fn2)
        fp = open(fn2, mode='w')

        fp.write("date")
        for foo in nhm_seg:
            fp.write("," + str(foo))
        fp.write('\n')

        for jj in range(len(dates)):
            fp.write(dates[jj])
            for kk in range(len(nhm_seg)):
                fp.write(',' + str(vals[jj,kk]))

            fp.write('\n')
        fp.close()
