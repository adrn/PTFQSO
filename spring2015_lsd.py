""" This file just generates individual executables to use the lsd-query tools """

import os

base_str = """
lsd-admin --db $LSD_TEMPDIR create table \
--drop-existing --primary-key=pk --spatial-keys=ra,dec \
{name} \
pk:u8 target_id:u8 ra:f8 dec:f8

lsd-import --db=$LSD_TEMPDIR text -d ' ' \
--cols target_id:1,ra:2,dec:3 {name} data/Spring2015/{filename}

lsd-query \
--define "zp=FileTable('/smallfiles/bsesar/DB/zps.npz', missing='90.0')" \
--define "sys_err=FileTable('/smallfiles/bsesar/DB/sys_err.npz', missing='90.0')" \
--define "best=FileTable('/smallfiles/bsesar/DB/current_pids.npz')" \
'SELECT t.target_id, d.ra as ra, d.dec as dec, d.mjd, \
(d.mag_auto+d.zeropoint)/1000.-zp(pid) as mag, \
sqrt((d.magerr_auto/1000.)**2+(sys_err(pid))**2) as magErr, \
d.flags, d.imaflags_iso, e.ptf_field, e.ccdid, \
m._NR, m._DIST*3600 \
FROM {name} as t, ptf_exp as e, ptf_det as d, \
     ptf_obj(matchedto=t, nmax=1, dmax=3., outer=True) as m \
WHERE ((d.flags & 506) == 0) & (e.fid == 2) & \
((d.imaflags_iso & 1821) == 0) & ((d.infobits & 2**17) == 0) & \
(mag > 10) & (mag < 23) & (magErr < 1) & (best(pid) == 1)' > /scr/aprice-whelan/{name}-output.dat
"""

if not os.path.exists("Spring2015-queries"):
    os.mkdir("Spring2015-queries")

for filename in os.listdir("data/Spring2015"):
    name = filename.split(".txt")[0].lower()
    print(name)
    fmt_str = base_str.format(name=name, filename=filename)

    with open("Spring2015-queries/{0}".format(name), 'w') as f:
        f.write(fmt_str)
