#!/usr/bin/python3
"""
Usage: python3 pp-rps-mc.py 1,2,52-53 > 03-mc-fixrps-ran-du-fec1-smci00-profile0.yaml ; oc apply -f 03-mc-fixrps-ran-du-fec1-smci00-profile0.yaml
Note: Housekeeping/Reserved Cores parameter MUST be both cores and siblings in HT environments!

Updated April 2 2021 -- patch to address issue cnf1360, adjust deployment methodology for upgrades of clusters
Updated April 4 2021 -- confirmed 4.6.16 --> 4.6.18 upgrade

This script generates a MachineConfiguration OCP object that
can be applied to a 4.6 cluster and adds additional tuning
fixes related to networking.

This workarounds the following bugs:
    - https://bugzilla.redhat.com/show_bug.cgi?id=1899321
    - https://bugzilla.redhat.com/show_bug.cgi?id=1887568
"""

import base64
import functools
import gzip
import shutil
import sys

LLHOOKSSH = """#!/usr/bin/env bash

mask="${1}"
[ -n "${mask}" ] || { logger "${0}: The rps-mask parameter is missing" ; exit 0; }

pid=$(jq '.pid' /dev/stdin 2>&1)
[[ $? -eq 0 && -n "${pid}" ]] || { logger "${0}: Failed to extract the pid: ${pid}"; exit 0; }

ns=$(ip netns identify "${pid}" 2>&1)
[[ $? -eq 0 && -n "${ns}" ]] || { logger "${0} Failed to identify the namespace: ${ns}"; exit 0; }

mode=$(ip netns exec "${ns}" [ -w /sys ] && echo "rw" || echo "ro" 2>&1)
[ $? -eq 0 ] || { logger "${0} Failed to determine if the /sys is writable: ${mode}"; exit 0; }

if [ "${mode}" = "ro" ]; then
    res=$(ip netns exec "${ns}" mount -o remount,rw /sys 2>&1)
    [ $? -eq 0 ] || { logger "${0}: Failed to remount /sys as rw: ${res}"; exit 0; }
fi

# /sys/class/net can't be used recursively to find the rps_cpus file, use /sys/devices instead
res=$(ip netns exec "${ns}" find /sys/devices -type f -name rps_cpus -exec sh -c "echo ${mask} | cat > {}" \; 2>&1)
[[ $? -eq 0 && -z "${res}" ]] || logger "${0}: Failed to apply the RPS mask: ${res}"

if [ "${mode}" = "ro" ]; then
    ip netns exec "${ns}" mount -o remount,ro /sys
    [ $? -eq 0 ] || exit 1 # Error out so the pod will not start with a writable /sys
fi
"""

RUNCWRPR = """#!/usr/bin/env bash

if [ -n "$3" ] && [ "$3" == "create" ] && [ -f "$5/config.json" ]; then
        conf="$5/config.json"
        cpus=$(jq -r '.linux.resources.cpu.cpus // empty' $conf)
        if [ -n $cpus ]; then
            tmp=$(mktemp)
            jq '.linux.resources.cpu.cpus = "{mask}"' $conf > "$tmp"
            mv "$tmp" $conf
        fi
fi

/bin/runc "$@"
"""

CRIORNTM = """# We should copy paste the default runtime because this snippet will override the whole runtimes section
[crio.runtime.runtimes.runc]
runtime_path = "/usr/local/bin/runc-wrapper.sh"
runtime_type = "oci"
runtime_root = "/run/runc"

# The CRI-O will check the runtime handler name under the code and will activate high-performance features,
# like CPU load balancing.
# We should provide the runtime_path because we need to inform that we want to re-use runc binary and we
# do not have high-performance binary under the $PATH that will point to it.
[crio.runtime.runtimes.high-performance]
runtime_path = "/usr/local/bin/runc-wrapper.sh"
runtime_type = "oci"
runtime_root = "/run/runc"
"""
SETRPSMSK = """#!/usr/bin/env bash

dev=$1
[ -n "${dev}" ] || { echo "The device argument is missing" >&2 ; exit 1; }

mask=$2
[ -n "${mask}" ] || { echo "The mask argument is missing" >&2 ; exit 1; }

dev_dir="/sys/class/net/${dev}"

function find_dev_dir {
  systemd_devs=$(systemctl list-units -t device | grep sys-subsystem-net-devices | cut -d' ' -f1)

  for systemd_dev in ${systemd_devs}; do
    dev_sysfs=$(systemctl show "${systemd_dev}" -p SysFSPath --value)

    dev_orig_name="${dev_sysfs##*/}"
    if [ "${dev_orig_name}" = "${dev}" ]; then
      dev_name="${systemd_dev##*-}"
      dev_name="${dev_name%%.device}"
      if [ "${dev_name}" = "${dev}" ]; then # disregard the original device unit
              continue
      fi

      echo "${dev} device was renamed to $dev_name"
      dev_dir="/sys/class/net/${dev_name}"
      break
    fi
  done
}

[ -d "${dev_dir}"/queues ] || find_dev_dir                # the net device was renamed, find the new name
[ -d "${dev_dir}"/queues ] || { sleep 5; find_dev_dir; }  # search failed, wait a little and try again
[ -d "${dev_dir}"/queues ] || { echo "${dev_dir}"/queues directory not found >&2 ; exit 0; } # the interface disappeared, not an error

find "${dev_dir}"/queues -type f -name rps_cpus -exec sh -c "echo ${mask} | cat > {}" \;
"""

JSONTPL = """{{
  "version": "1.0.0",
  "hook": {{
    "path": "/usr/local/bin/low-latency-hooks.sh",
    "args": ["low-latency-hooks.sh", "{mask}"]
  }},
  "when": {{
    "always": true
  }},
  "stages": ["prestart"]
}}
"""

TPL = """apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  labels:
    machineconfiguration.openshift.io/role: ran-du-fec1-smci00
  name: ran-du-fec1-smci00-fixrps-netqueues
spec:
  config:
    ignition:
      version: 3.1.0
    storage:
      files:
      - contents:
          source: data:text/plain;charset=utf-8;base64,{llhooks}
          verification: {{}}
        filesystem: root
        mode: 448
        path: /usr/local/bin/low-latency-hooks.sh
      - contents:
          source: data:text/plain;charset=utf-8;base64,{runcwrapper}
          verification: {{}}
        filesystem: root
        mode: 448
        path: /usr/local/bin/runc-wrapper.sh
      - contents:
          source: data:text/plain;charset=utf-8;base64,{crioruntime}
          verification: {{}}
        filesystem: root
        mode: 448
        path: /etc/crio/crio.conf.d/99-runtimes.conf
      - contents:
          source: data:text/plain;charset=utf-8;base64,{setrpsmask}
          verification: {{}}
        filesystem: root
        mode: 448
        path: /usr/local/bin/set-rps-mask.sh
      - contents:
          source: data:text/plain;charset=utf-8;base64,{json}
          verification: {{}}
        filesystem: root
        mode: 420
        path: /etc/containers/oci/hooks.d/99-low-latency-hooks.json
      - contents:
          source: data:text/plain;charset=utf-8;base64,U1VCU1lTVEVNPT0ibmV0IiwgQUNUSU9OPT0iYWRkIiwgVEFHKz0ic3lzdGVtZCIsIEVOVntTWVNURU1EX1dBTlRTfT0idXBkYXRlLXJwc0Alay5zZXJ2aWNlIgo=
          verification: {{}}
        filesystem: root
        mode: 420
        path: /etc/udev/rules.d/99-netdev-rps.rules
      - contents:
          source: data:text/plain;charset=utf-8;base64,{queues}
          verification: {{}}
        filesystem: root
        mode: 448
        path: /usr/local/bin/fix-net-queues.sh
    systemd:
      units:
      - contents: |
          [Unit]
          Description=Sets network devices RPS mask

          [Service]
          Type=oneshot
          ExecStart=/usr/local/bin/set-rps-mask.sh %i {mask}
        name: update-rps@.service
      - name: fix-net-queues.service
        enabled: true
        contents: |
          [Unit]
          Description=Limit the net queues to 2 per housekeeping cpu
          Before=kubelet.service
          After=network.service

          [Service]
          Type=oneshot
          ExecStart=/usr/local/bin/fix-net-queues.sh

          [Install]
          WantedBy=multi-user.target
"""

QUEUES_SH = """#!/bin/bash
#!/bin/bash
queue_cnt=4 # 2x reserved cores (for RX/TX queues)

if [ ! -f /usr/local/bin/ethtool ]; then
    # find ethtool in local containers (e.g. tuned container)
    find_ethtool=$(find /var/lib/containers/storage/overlay -name "ethtool" | head -1)
    cp $find_ethtool /usr/local/bin/ethtool
fi

for n in /sys/class/net/*;
do
        syspth=$(realpath $n | grep -v '/sys/devices/virtual')
        if [ x$syspth == "x" ]; then continue; fi

        iface=$(basename $syspth)
        echo "Configuring $iface to have $queue_cnt queues"
        /usr/local/bin/ethtool -L $iface combined $queue_cnt
done
"""

def expand_cpus(acc, cpu):
    if "-" in cpu:
        first, last = cpu.split("-")
        return acc + list(range(int(first), int(last) + 1))
    else:
        return acc + [int(cpu)]

if __name__ == "__main__":
    cpus = functools.reduce(expand_cpus, sys.argv[1].split(","), [])
    cpumask = functools.reduce(lambda acc,x: acc + 2**x, cpus, 0)
    hexmaskraw = hex(cpumask)[2:] #strip 0x
    hexmasklist = []

    while hexmaskraw:
        partmask = hexmaskraw[-8:]
        partmask = "0" * (8 - len(partmask)) + partmask
        hexmaskraw = hexmaskraw[:-8]
        hexmasklist.insert(0, partmask)

    hexmask = ",".join(hexmasklist)

    hook_json = base64.b64encode(JSONTPL.format(
        mask=hexmask).encode('UTF-8')).decode('UTF-8')
    queues = base64.b64encode(QUEUES_SH.format(
        cpucount=len(cpus)).encode('UTF-8')).decode('UTF-8')
    llhooks = base64.b64encode(LLHOOKSSH.encode('UTF-8')).decode('UTF-8')
    runcwrapper = base64.b64encode(RUNCWRPR.format(
        mask=sys.argv[1]).encode('UTF-8')).decode('UTF-8')
    crioruntime = base64.b64encode(CRIORNTM.encode('UTF-8')).decode('UTF-8')
    setrpsmask = base64.b64encode(SETRPSMSK.encode('UTF-8')).decode('UTF-8')

    mc_yaml = TPL.format(json=hook_json, queues=queues, mask=hexmask, llhooks=llhooks,
                        runcwrapper=runcwrapper, crioruntime=crioruntime, setrpsmask=setrpsmask )
    print(mc_yaml)
