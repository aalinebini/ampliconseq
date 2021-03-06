#!/usr/bin/env python
from __future__ import print_function
from collections import OrderedDict
import re

# TODO nf-core: Add additional regexes for new tools in process get_software_versions
regexes = {
    "nf-core/ampliconseq": ["v_pipeline.txt", r"(\S+)"],
    "Nextflow": ["v_nextflow.txt", r"(\S+)"],
    "MultiQC": ["v_multiqc.txt", r"multiqc, version (\S+)"],
    "Trimmomatic": ['v_trimmomatic.txt', r"(\S+)"],
    "Flash": ['v_flash.txt', r"FLASH v(\d+.\d+.\d+)"],
    "Clustalo": ['v_clustalo.txt', r"(.+)"],

}
results = OrderedDict()
results["nf-core/ampliconseq"] = '<span style="color:#999999;">N/A</span>'
results["Nextflow"] = '<span style="color:#999999;">N/A</span>'
results["MultiQC"] = '<span style="color:#999999;">N/A</span>'
results["Trimmomatic"] = '<span style="color:#999999;">N/A</span>'


# Search each file using its regex
for k, v in regexes.items():
    try:
        with open(v[0]) as x:
            versions = x.read()
            match = re.search(v[1], versions)
            if match:
                results[k] = "v{}".format(match.group(1))
    except IOError:
        results[k] = False

# Remove software set to false in results
for k in list(results):
    if not results[k]:
        del results[k]

# Dump to YAML
print(
    """
id: 'software_versions'
section_name: 'nf-core/ampliconseq Software Versions'
section_href: 'https://github.com/nf-core/ampliconseq'
plot_type: 'html'
description: 'are collected at run time from the software output.'
data: |
    <dl class="dl-horizontal">
"""
)
for k, v in results.items():
    print("        <dt>{}</dt><dd><samp>{}</samp></dd>".format(k, v))
print("    </dl>")

# Write out regexes as csv file:
with open("software_versions.csv", "w") as f:
    for k, v in results.items():
        f.write("{}\t{}\n".format(k, v))
